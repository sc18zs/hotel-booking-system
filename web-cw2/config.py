import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hotel.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASKY_ORDERS_PER_PAGE=2

WTF_CSRT_ENABLE = True
SECRET_KEY = 'a-very-secret-secret'

# 服务器ip地址
MAIL_SERVER = "smtp.qq.com"

# 端口号:TLS对应587,SSL对应465
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_USE_SSL : 默认为 False
# 发送者邮箱
MAIL_USERNAME = "1349049995@qq.com"
# 发送者QQ邮箱授权码(进入邮箱发送短信申请即可，具体参照下图)
MAIL_PASSWORD = "istlvawgvmbphcca"
# 默认发送者
MAIL_DEFAULT_SENDER = "1349049995@qq.com"