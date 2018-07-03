import os

# 指定secret_key:用于解析session数据
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'asdfjqip1i3p4ksnfjdfal'

DEBUG = True

# 数据库配置信息
HOSTNAME = '118.25.48.34'
PORT = '3306'
DATABASE = 'test_platform'
USERNAME = 'root'
PASSWORD = '123456'

# PERMANENT_SESSION_LIFETIME = 31 # 设置cookie的保存时间

# DB_URI 连接数据库的配置字符串
DB_URI = 'mysql+pymysql://{username}:{password}@{host}: \
{port}/{db}?charset=utf8'.format(
    username=USERNAME,
    password=PASSWORD,
    host=HOSTNAME,
    port=PORT,
    db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 设置跟踪：否，如果设置为true，sqlalchemy中的模型一旦更改，就要发送信号
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义一个常量:用来存cms模块的用户id
CMS_USER_ID = 'ASDFSDFASD'

# 定义一个常量：用来存front模块得意哦那个户id
FRONT_USER_ID = 'ASDGHSJKGDAHKJSGHDK'

# flask-email
# 🌟 发送者邮箱的服务器地址
# ⚠️ QQ邮箱不支持非加密方式发送邮件
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True  # 如果使用TLS加密协议，使用端口号：587
# MAIL_USE_SSL = False # 如果使用SSL加密协议，使用端口号：465
# MAIL_DEBUG = 默认为 app.debug # 默认是根据app上的debug来打印日志
MAIL_USERNAME = "291008572@qq.com"  # QQ邮箱
MAIL_PASSWORD = "brlrqdotgkcicbbh"  # 授权码
MAIL_DEFAULT_SENDER = "291008572@qq.com"  # 默认发送者

# 🌟 阿里大于[短信验证码服务]相关配置
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'
