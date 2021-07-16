from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=8181, threaded=True)













# current_app(代理模式) --> 应用上下文（AppContext）的 app属性 -- Flask(有配置信息、蓝图等属性)对象的封装 -- 外加一些额外的属性
# request（代理模式） --> 请求上下文（RequestContext）的request属性 -- Request对象的封装 -- 外加一些额外的属性
'''
1、API的难点在于第一步：API的设计
2、试图函数最终 return 的都是 Response封装后的 对象，包括了http_code、header等等信息（content-type、location等是在header里的）
3、
'''

'''
1、代码封装函数，不仅仅是取决于代码量
'''

'''
1、数据库 表的创建方式：
    1、Database First
    2、Model First
    *3、Code First 专注业务模型的设计，而不是数据库的设计（先从SQLAlchemy设计类，再映射生成表）

2、「业务逻辑」最合理的地方是编写在 Model 层（MVC），而不是 Controller 层
    Model 层不止是表结构的设计
'''