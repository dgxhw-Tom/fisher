import json

from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.helpers.libs.helper import is_isbn_or_key
from app.helpers.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
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
        # return json.dumps(books, default=lambda x: x.__dict__)
        # return jsonify(result)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 获取数据信息
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    # 默认该书都不在礼物、心愿清单
    has_in_gifts = False
    has_in_wishes = False
    # 判断是否是登录状态
    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    # 显示关于本书的相关 gift 和 wish，并根据书处于当前用户 gift 列表 或者 wish 列表，进行显示
    # 默认显示所有想要赠送这本书的用户信息    # 这里从 model 中拿到数据，然后到 viewmodel 中进行裁剪
    wishes = TradeInfo(Wish.query.filter_by(isbn=isbn, launched=False).all())
    gifts = TradeInfo(Gift.query.filter_by(isbn=isbn, launched=False).all())

    return render_template('book_detail.html', book=book,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes,
                           wishes=wishes, gifts=gifts)
