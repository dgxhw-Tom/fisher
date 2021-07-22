from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from . import web
from .. import db
from ..helpers.libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from ..view_models.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    view_model = MyGifts(current_user.id)
    return render_template('my_gifts.html', gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 既不在赠送清单，也不在心愿清单才能添加
        with db.auto_commit():
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            # gift.book_id = yushu_book.data.id
            db.session.add(gift)
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']

        '''
            建议所有db.commit 都要捕获异常并rollback
        '''
        # try:
        #     # 事务
        #     gift = Gift()
        #     gift.uid = current_user.id
        #     gift.isbn = isbn
        #     ###############
        #     current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        #     db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(uid=current_user.id, id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting
    ).first()

    if drift:
        flash('这个礼物还在交易状态，请先处理掉再来撤销你的礼物')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
