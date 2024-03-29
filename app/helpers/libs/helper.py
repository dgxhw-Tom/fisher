#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/14 下午9:24
    @Author xuhuawei
    @attention： 
'''

def is_isbn_or_key(word):
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    if '-' in word and len(word.replace('-', '')) == 10:
        # isbn10
        return 'isbn'
    return 'keyword'


def get_isbn(data_dict):
    isbn = data_dict.get('isbn')
    if not isbn:
        isbn = data_dict.get('isbn13')
        if not isbn:
            isbn = data_dict.get('isbn10')
    return isbn
