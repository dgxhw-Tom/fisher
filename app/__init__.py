from flask import Flask
from app.models.book import db


def create_app():
    # 实例化一个flask app 对象
    app = Flask(__name__)

    # 加载配置
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    # 初始化数据库
    db.init_app(app)
    db.create_all(app=app)
    # with app.app_context():
    #     db.create_all()

    return app


# 注册蓝图
def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
