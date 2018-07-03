from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g


# 写表单验证器
class LoginForm(BaseForm):
    email = StringField(validators=[
        Email(message='请输入正确的邮箱格式'),
        InputRequired(message='请输入邮箱')
    ])

    password = StringField(validators=[
        Length(6, 20, message='请输入正确格式的密码'),
        InputRequired(message='请输入密码')
    ])

    remember = IntegerField()


# 重设密码验证器
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[
        Length(6, 20, message='请输入正确格式的新密码'),
    ])

    newpwd = StringField(validators=[
        Length(6, 20, message='请输入正确格式的旧密码'),
    ])

    newpwd2 = StringField(
        validators=[EqualTo("newpwd", message='确认密码必须和新的密码保持一致')])


# 修改邮箱验证器
class ResetEmailForm(BaseForm):
    email = StringField(validators=[
        Email(message='请输入正确格式的邮箱!'),
        InputRequired(message='请输入邮箱')
    ])

    captcha = StringField(validators=[
        Length(min=6, max=6, message='请输入正确长度的验证码!'),
        InputRequired(message='请输入验证码')
    ])

    def validate_captcha(self, field):
        '''
        验证输入的验证码和memcahced的验证码是否保持一致
        '''
        captcha = field.data  # 表单中传过来的验证码
        email = self.email.data  # 表单中传过来的邮箱
        # 1. 先拿到验证码
        captcha_cache = zlcache.get(email)  # memcached中存的验证码

        # 2. 判断memcached中存的验证码和表单传过来的验证码是否一致，如果一致就返回true
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self, filed):
        '''
        验证是否为相同的邮箱
        '''
        email = filed.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱!')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])


class AddProjectForm(BaseForm):
    projectName = StringField(validators=[InputRequired(message='请输入项目名称！')])
    projectType = StringField(validators=[InputRequired(message='请输入项目类型！')])
    projectVersion = StringField(validators=[InputRequired(message='请输入项目版本号！')])


class UpdateProjectForm(AddProjectForm):
    projectID = IntegerField(validators=[InputRequired(message='请输入项目id！')])
