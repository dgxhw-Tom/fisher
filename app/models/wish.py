#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/17 下午8:19
    @Author xuhuawei
    @attention：
'''
from collections import defaultdict

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, func
from sqlalchemy.orm import relationship

from app.helpers.spider.yushu_book import YuShuBook
from app.models.base import db, Base


class Wish(Base):
    id = Column(Integer, primary_key=True)

    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)

    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'), nullable=False)
    isbn = Column(String(15), nullable=False)

    launched = Column(Boolean, default=False)

    @staticmethod
    def get_gift_counts(wishes):
        # 解决循环导入的问题
        from app.models.gift import Gift
        book_isbn_list = [wish.isbn for wish in wishes]

        ret = defaultdict(int)
        temp_list = db.session.query(
            func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False, Gift.isbn.in_(book_isbn_list), Gift.status == 1).group_by(
            Gift.isbn).all()
        for temp in temp_list:
            ret[temp[1]] = temp[0]

        return ret

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
