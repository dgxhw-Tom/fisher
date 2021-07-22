#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail

from app.models.book import db
from flask_login import LoginManager

login_manager = LoginManager()
mail = Mail()


def create_app():
    # 实例化一个flask app 对象
    app = Flask(__name__)

    # 加载配置
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    # 注册flask-login插件
    login_manager.init_app(app=app)
    # 设置默认跳转到的login界面；指定视图函数 web.login
    login_manager.login_view = 'web.login'
    # 设置提示未登录用户的 提示语
    login_manager.login_message = '请先登录或注册'

    # 注册 flask-mail
    mail.init_app(app)

    # 注册 SQLAlchemy
    db.init_app(app)
    # db.create_all(app=app)
    with app.app_context():
        db.create_all()

    return app


# 注册蓝图
def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
