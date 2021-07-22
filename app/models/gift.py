#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/17 下午8:19
    @Author xuhuawei
    @attention： 
'''
from collections import defaultdict

from flask import current_app
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, desc, func
from sqlalchemy.orm import relationship

from app.helpers.spider.yushu_book import YuShuBook
from app.models.base import db, Base
from app.models.wish import Wish
from app.view_models.book import BookViewModel


class Gift(Base):
    id = Column(Integer, primary_key=True)

    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)

    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 把它不当做「实例方法」的原因是，该类的实例化对象 代表 一个礼物，这里是取最近的多个礼物，不适合作为实例化方法
    # 面向对象的一种理解 和 应用
    @staticmethod
    def recent():
        # 链式编程
        gift_list = Gift.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).all()

        books = [BookViewModel(gift.book) for gift in gift_list]
        return books

    @staticmethod
    def get_wish_counts(gifts):
        book_isbn_list = [gift.isbn for gift in gifts]

        ret = defaultdict(int)

        # group_by与funct.count统计联合使用；filter_by也是封装的filter，filter可以指定模型，并且做一些多表查询等复杂的查询
        temp_list = db.session.query(
            func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(book_isbn_list), Wish.status == 1).group_by(
            Wish.isbn).all()
        for temp in temp_list:
            ret[temp[1]] = temp[0]

        return ret

    def is_yourself_gift(self, uid):
        return uid == self.uid
