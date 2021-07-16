# 机密信息 和 生产环境开发环境不一样的配置

DEBUG = True

# 数据库配置（必须为SQLALCHEMY_DATABASE_URI） : 数据库类型+数据库驱动://用户名:密码@ip:port/database
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:33061/fisher'
