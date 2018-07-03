from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime


# 定义性别枚举
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOWN = 4


# 🌟 前台用户
class FrontUser(db.Model):
    __tablename__ = 'front_user'

    # id不能为自增长，因为存在商业风险，特别是id关联的url
    id = db.Column(
        db.String(100), primary_key=True, default=shortuuid.uuid
    )  # 这里uuid不加()，如果给了就是每次都是把执行结果当作id，而现在的需求是每次执行产生一个
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # 加入_后，变成受保护属性
    email = db.Column(db.String(50), nullable=True, unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOWN)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 初始化
    def __init__(self, *args, **kwargs):
        # kwargs是关键字参数，等同于字典
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')

        # 其他参数可以用父类去处理
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)
