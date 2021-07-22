#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/17 下午8:13
    @Author xuhuawei
    @attention： 
'''
from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import login_manager
from app.helpers.libs.enums import PendingStatus
from app.helpers.libs.helper import is_isbn_or_key
from app.helpers.spider.yushu_book import YuShuBook
from app.models.base import db, Base

# User Model 需要继承 flask-login 的 UserMixin 类，继承插件的许多内置函数和属性，不然很多内置的功能无法使用
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish


class User(UserMixin, Base):
    # 可 __tablename__ 重新定义表名称
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 服务器端存储 用户原始密码的哈希值
    _password = Column('password', String(100))

    # 使用Python的「属性描述符」实现 属性的 get 和 set，可以自定义预/后处理代码
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 此处代码用于重置密码
    # 用户发起重置代码请求后，服务器端向客户邮箱发送一个token
    # 用户通过邮箱内url，持有这个token来服务器端修改密码
    def generate_token(self, expiration=600):
        # itsdangerous.TimedJSONWebSignatureSerializer 该类可以对「序列化数据」进行「加密」和「有效期」的设置，输出加密后的「token字符串」
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # s.dumps 生成 bytes
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        # 解析token，拿到要重设密码的 用户id
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        user = User.query.get(data.get('id'))
        if user is None:
            return False
        with db.auto_commit():
            user.password = new_password
        return True

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        # 没有这本书，则用户不能选择「赠送此书」
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 不允许一个用户同时赠送多本相同的图书 (该书已经在赠送列表)
        # 不允许一个用户同时是同一本图书的捐赠者和索要者（该书在赠送列表 或者 心愿列表）
        # 不允许一个用户对同一个本不停添加心愿（该书已经在心愿列表）
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    # 判断是否可以索要书籍
    def can_send_drifts(self):
        if self.beans < 1:
            return False

        success_gift_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return floor(success_receive_count / 2) <= success_gift_count

    @property
    def summary(self):
        return dict(
            nikename=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


# 为flask-login插件 注册根据用户id获取用户信息的函数
@login_manager.user_loader
def get_user(uid):
    # 根据id（主键）获取直接 get 即可，不用filter
    return User.query.get(int(uid))
