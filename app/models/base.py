#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/17 下午8:11
    @Author xuhuawei
    @attention： 
'''
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from sqlalchemy import orm


class SQLAlchemy(_SQLAlchemy):

    # 使用contextmanager装饰器使 auto_commit 成为上下文管理器，yield上面代码对应__entet__，下面代码对应__exit__
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 重写 SQLAlchemy 的filter_by，flask_sqlalchemy 也是封装的 SQLAlchemy


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # 改写了自己的规则后，调用父类的filter_by
        return super().filter_by(**kwargs)


db = SQLAlchemy()
db.Query = Query

class Base(db.Model):
    # 添加 __abstract__ = True 可以让 sqlalchemy 不去创建表 Base，我们就可以使Base作为基类来创建所有表的公共字段了
    __abstract__ = True
    # Column等第一个参数可以重新设置数据库中的字段名
    create_time = Column('create_time', Integer)
    # status = 0 代表该记录被删除
    # status = 1 代表该记录存在
    status = Column(SmallInteger, default=1)

    # 这里使用 实例方法 初始化每个user记录 的创建时间
    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 为传过来的参数 对Model的字段进行赋值
    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
