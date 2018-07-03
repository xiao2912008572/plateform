from wtforms import StringField
from ..forms import BaseForm
from wtforms.validators import Regexp, EqualTo, ValidationError
from utils import zlcache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式的手机号码！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式的验证码！')])
    username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1", message='两次输入的密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式的验证码！')])

    # 短信验证码验证器
    def validate_sms_captcha(self, field):
        sms_captcha = field.data  # 拿到短信验证码的值
        telephone = self.telephone.data  # 拿到手机号的值

        # TODO 测试用
        '''
            判断短信验证码是否不等于1111，如果不等于，再去做验证
        '''
        if sms_captcha != '1111':
            print('短信验证码不等于1111')
            # 从memcached中取telephone
            sms_captcha_mem = zlcache.get(telephone)
            # 如果没有填写短信验证码或者是不相等
            # print('sms_captcha_mem = ', sms_captcha_mem)
            # print('sms_captcha = ', sms_captcha)
            if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
                raise ValidationError(message='短信验证码错误！')

    # 图形验证码
    def validate_graph_captcha(self, field):
        graph_captcha = field.data

        # TODO 测试用
        if graph_captcha != '1111':
            print('图形验证码不等于1111')
            # 从memcached中取graph_captcha
            graph_captcha_mem = zlcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValidationError(message='图形验证码错误！')

class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    remember = StringField()