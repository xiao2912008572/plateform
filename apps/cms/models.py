from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 🌟 权限类
class CMSPersmission(object):
    # 255的二进制方式来表示 1111 1111
    # 0. 所有权限
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子权限
    POSTER = 0b00000010
    # 3. 管理评论的权限
    COMMENTER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6. 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7. 管理后台管理员的权限
    ADMINER = 0b01000000


# 🌟 1. 用户和角色是多对多关系，先定义第三方中间表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column(
        'cms_role_id',
        db.Integer,
        db.ForeignKey('cms_role.id'),
        primary_key=True),
    db.Column(
        'cms_user_id',
        db.Integer,
        db.ForeignKey('cms_user.id'),
        primary_key=True),
)


# 🌟 2. 角色表
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(
        db.Integer, default=CMSPersmission.VISITOR)  # 默认是访问者权限

    # 将角色表和中间表绑定
    # CMSUser：建立关系的表
    # secodary：中间表
    # backref：反向引用
    users = db.relationship(
        'CMSUser', secondary=cms_role_user, backref='roles')


# 🌟 3. 后台用户
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # 加入_后，变成受保护属性
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username

        # 这里self.password等于调用下面的password这是密码属性方法，将传进来的password进行加密
        self.password = password

        self.email = email

    # 使用property装饰器：将类中的方法定义成一个属性，虽然是方法， 但是外界再访问这个方法的时候，就和访问属性一模一样
    # 获取密码
    @property
    def password(self):
        '''
            useage:
            user = CMSUser() # 定义对象
            print(user.password) # 访问对象的方法属性
        '''
        return self._password

    # 设置密码：重新定义一个设置方法
    @password.setter
    def password(self, raw_password):
        '''
            useage：
            user.password = 'abc'
        '''
        # 1. 对原生密码进行加密
        self._password = generate_password_hash(raw_password)

    # 检查密码
    def check_password(self, raw_password):
        # self.password -> 访问的还是self._password(经过加密的密码)
        result = check_password_hash(self.password, raw_password)
        return result

    # 拿到该用户的所有权限 ———— 利用'或运算'实现
    @property
    def permissions(self):
        '''
            user = CMSUser()    # 定义对象
            print(user.permissions)     # 当作对象.属性的方式访问
        '''
        # 1. 判断用户是否拥有角色
        if not self.roles:
            return 0  # 0代表不拥有任何权限
        # 2. 遍历用户权限，用all_permissions存储权限
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions  # 获取权限
            all_permissions |= permissions  # 或操作
        return all_permissions

    # 判断用户有没有权限 ———— 利用'与运算'实现
    def has_permission(self, permission):
        # # 1. 先拿到用户的所有权限
        # all_permissions = self.permissions
        # # 2. 将传入的permission和all_permissions进行与运算
        # result = all_permissions & permission == permission
        return self.permissions & permission == permission

    @property
    # 判断是否是开发者
    def is_developer(self):
        return self.has_permission(permission=CMSPersmission.ALL_PERMISSION)


# 密码：对外的字段名叫做password
# 密码：对内的字段名叫做_password

# 🌟 4. 项目表:用于存储项目的相关信息
class EoProject(db.Model):
    __tablename__ = 'eo_project'

    # 项目ID
    projectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 项目类型
    projectType = db.Column(db.Integer, nullable=False)
    # 项目名
    projectName = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    # 项目创建时间
    projectCreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 项目更新时间
    projectUpdateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 项目版本
    projectVersion = db.Column(db.String(6, 'utf8_bin'), nullable=False)


# CREATE TABLE `eo_api_env` (
#   `envID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envName` varchar(255) NOT NULL,
#   `projectID` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`envID`,`projectID`)
# ) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8

# 🌟 5. 环境管理 - 环境表1 - eo_api_env
'''
关系图：
4.项目表 和 5.环境表 : 一对多关系 
'''


class EoApiEnv(db.Model):
    __tablename__ = 'eo_api_env'

    # 环境ID
    envID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 环境名称
    envName = db.Column(db.String(255), nullable=False)
    # 环境说明
    envDesc = db.Column(db.String(255), nullable=True)
    # 项目ID - 外键
    projectID = db.Column(db.Integer, db.ForeignKey("eo_project.projectID"))

    # 一对多关系映射
    project = db.relationship("EoProject", backref='apienv')

    def __repr__(self):
        return "<Article(envName:%s)>" % self.envName


# CREATE TABLE `eo_api_env_front_uri` (
#   `envID` int(10) unsigned NOT NULL,
#   `uri` varchar(255) NOT NULL,
#   `uriID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `applyProtocol` varchar(4) NOT NULL DEFAULT '-1',
#   PRIMARY KEY (`uriID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 6. 环境管理 - 环境表2 - eo_api_env_front_uri
'''
关系图：
5.项目表 和 6.环境uri表 : 一对一关系 
'''


class EoApiEnvFrontUri(db.Model):
    __tablename__ = 'eo_api_env_front_uri'

    # uriID
    uriID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 前置uri
    uri = db.Column(db.String(255), nullable=False)
    # 鉴权信息
    applyProtocol = db.Column(db.String(4), nullable=True)
    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对一关系映射
    env = db.relationship("EoApiEnv", backref=db.backref('uri', uselist=False))


# CREATE TABLE `eo_api_env_header` (
#   `headerID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(11) NOT NULL,
#   `applyProtocol` varchar(255) DEFAULT NULL,
#   `headerName` varchar(255) NOT NULL,
#   `headerValue` text NOT NULL,
#   PRIMARY KEY (`headerID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 7. 环境管理 - 请求头表 - eo_api_env_front_uri
'''
关系图：
5.项目表 和 7.请求头表 : 一对多关系 
'''


class EoApiEnvHeader(db.Model):
    __tablename__ = 'eo_api_env_header'

    # headerID
    headerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 请求头名称
    headerName = db.Column(db.String(255), nullable=False)
    # 请求头值
    headerValue = db.Column(db.String(255), nullable=False)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="header")


# CREATE TABLE `eo_api_env_param` (
#   `paramID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(10) unsigned NOT NULL,
#   `paramKey` varchar(255) NOT NULL,
#   `paramValue` text NOT NULL,
#   PRIMARY KEY (`paramID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 8. 环境管理 - 全局参数表 - eo_api_env_param
'''
关系图：
5.项目表 和 8.全局参数 : 一对多关系 
'''


class EoApiEnvParam(db.Model):
    __tablename__ = 'eo_api_env_param'

    # paramID
    paramID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 参数键
    paramKey = db.Column(db.String(255), nullable=False)
    # 参数值
    paramValue = db.Column(db.String(255), nullable=False)
    # 参数描述
    paramDesc = db.Column(db.String(255), nullable=True)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="param")


# CREATE TABLE `eo_api_env_param_additional` (
#   `paramID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `envID` int(10) unsigned NOT NULL,
#   `paramKey` varchar(255) NOT NULL,
#   `paramValue` text NOT NULL,
#   PRIMARY KEY (`paramID`,`envID`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8

# 🌟 9. 环境管理 - 额外参数表 - eo_api_env_param_additional
'''
关系图：
5.项目表 和 8.全局参数 : 一对多关系 
'''


class EoApiEnvAdditionalParam(db.Model):
    __tablename__ = 'eo_api_env_param_additional'

    # paramID
    paramID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 参数键
    paramKey = db.Column(db.String(255), nullable=False)
    # 参数值
    paramValue = db.Column(db.String(255), nullable=False)
    # 参数描述
    paramDesc = db.Column(db.String(255), nullable=True)

    # envID
    envID = db.Column(db.Integer, db.ForeignKey("eo_api_env.envID"))

    # 一对多关系映射
    env = db.relationship("EoApiEnv", backref="additionalparam")
