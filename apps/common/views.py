from flask import Blueprint, request
from exts import alidayu
from utils import restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import zlcache
from flask import (
    Blueprint,
    make_response
)
from utils.captcha import Captcha
from io import BytesIO
from exts import alidayu

# 蓝图 : 蓝图名字 - __name__ - url前缀
bp = Blueprint("common", __name__, url_prefix='/c')

'''
v1.0 未加密版本发送短信验证码
'''
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # 传递参数两种方式
#     # 1. ?telephone=xxx
#     # 2. /c/sms_captcha/xxx
#     '''
#     采用第一种传参方式
#     :return:
#     '''
#     # 1. 拿到手机号
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码!')
#
#     # 2. 生成验证码
#     captcha = Captcha.gene_text(number=4)
#
#     # 3. 发送验证码
#     if alidayu.send_sms(telephone=telephone, code=captcha):
#         return restful.success()
#     else:
#         return restful.success()
#         # return restful.params_error(message='短信验证码发送失败！')

'''
v1.1 短信验证码加密版本实现
'''


# 传递参数两种方式
# 1. ?telephone=xxx
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    '''
    实现：
    1. telephone
    2. timestamp
    3. md5(ts+telephone+salt)
    :return:
    '''
    # 1. 申明验证表单验证对象
    form = SMSCaptchaForm(request.form)
    # 2. 通过验证
    if form.validate():
        # 2.1 拿到手机号
        telephone = form.telephone.data
        # 2.2 生成验证码
        captcha = Captcha.gene_text(number=4)
        print('发送的短信验证码是:', captcha)
        # 2.3 发送验证码,成功时：
        if alidayu.send_sms(telephone, code=captcha):

            # ⚠️：这里将验证码保存在缓存服务器中
            zlcache.set(telephone, captcha, timeout=60)

            return restful.success()
        # 发送验证码，失败时：
        else:
            return restful.params_error()
    else:
        return restful.params_error(message='参数错误！')


# 🌟 Front：获取图像验证码视图
@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()

    # ⚠️ 利用memcached保存图形验证码
    zlcache.set(text.lower(), text.lower())

    # BytesIO:字节流 - out:声明二进制流对象
    out = BytesIO()
    # 将图片保存到image对象，指定图片格式png
    image.save(out, 'png')
    # 将指针指定在0位置
    out.seek(0)
    # 读取并返回
    resp = make_response(out.read())
    # 指定类型
    resp.content_type = 'image/png'
    # 返回图片
    return resp
