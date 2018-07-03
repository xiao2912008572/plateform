# Author:Xiaojingyuan
from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired
import hashlib


# 🌟 短信验证码表单
class SMSCaptchaForm(BaseForm):
    salt = 'qewr234234werjk;adsfkd;sfka'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    # 时间戳：ms单位，一共有13位
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    # 重写验证函数
    def validate(self):
        # result = super(SMSCaptchaForm, self).validate()
        result = super().validate()
        # 1. 先执行父类的验证器
        if not result:
            return False

        # 2. 拿到表单的telephone、timestamp、sign值
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(timestamp+telephone+salt)
        # md5函数必须要传一个bytes类型的字符串进去
        # unicode转bytes用encode('utf-8')
        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()  # hexdigest反函数，获取对象中的字符串
        # print('客户端提交的sign：', sign)
        # print('服务器生成的sign2：', sign2)
        if sign == sign2:
            return True
        else:
            return False
