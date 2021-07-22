# 机密信息 和 生产环境开发环境不一样的配置

# 用于 session 加密
SECRET_KEY = 'cba5a076-85ad-4438-a064-c605eeb068cc'
# 数据库配置（必须为SQLALCHEMY_DATABASE_URI） : 数据库类型+数据库驱动://用户名:密码@ip:port/database
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:33061/fisher'

# 注意 MAIL_USERNAME 和 MAIL_SENDER 中使用的邮箱必须相同，qq邮箱才接受你这个发送请求
MAIL_USERNAME = 'xhw15313528396@163.com'
MAIL_PASSWORD = 'OKRVORGTMUUBVDNT'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SERVER = 'smtp.163.com'
MAIL_DEFAULT_SENDER = 'xhw15313528396@163.com'
# MAIL_PORT = '25'
# MAIL_USE_SSL = True
