import json

from flask import jsonify, request

from app.forms.book import SearchForm
from app.helpers.libs.helper import is_isbn_or_key
from app.helpers.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from app.web import web


# @web.route('/book/search/<q>/<page>')
# def search(q, page):
@web.route('/book/search')
def search():
    """
    :param q: 普通关键字 或 isbn
    :param page:
    :return:
    """
    # 获取参数
    # q = request.args.get('q')
    # page = request.args.get('page')

    # 验证层，使用wtforms传入参数进行校验
    form = SearchForm(request.args)

    # MVC中将视图函数中的「业务逻辑」解藕出去放到 Model 层
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)

        # 获取API得到的数据
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        # 将API得到的数据经过model层进行业务处理
        books.fill(yushu_book, q)

        # books 为object，使用 default=lambda x: x.__dict__ 将object的属性进行 序列化
        return json.dumps(books, default=lambda x: x.__dict__)
        # return jsonify(result)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        return jsonify(form.errors)
