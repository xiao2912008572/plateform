from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for)
from .forms import SignupForm, SigninForm
from utils import restful, safeutils
from .models import FrontUser
from exts import db
import config

# 蓝图 : 蓝图名字 - __name__ 前台页面的url后面不需要加前缀
bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    # return 'front index'
    return render_template('front/front_index.html')


'''
    测试验证码功能
'''


# @bp.route('/sms_captcha/')
# def sms_captcha():
#     result = alidayu.send_sms(telephone='15927678712', code='我是不语你是胡巴')
#     if result:
#         return '发送成功!'
#     else:
#         return '发送失败!'


# 🌟 Front：注册类视图
class SignupView(views.MethodView):
    def get(self):
        # ⚠️ referrer引用：可以知道上一个页面，本页面来源
        return_to = request.referrer

        # return_to 存在 并且不等于当前页面的url 并且
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
            # return render_template('front/login.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')
            # return render_template('front/login.html')

    # 注册流程
    def post(self):
        form = SignupForm(request.form)
        # 通过验证
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            # 插入数据
            try:
                # 1. ⚠️ 查询上传过来的telephone的唯一性校验
                user = db.session.query(FrontUser).filter_by(telephone=telephone).first()
                # 2. 如果没有重复的telephone
                if not user:
                    user = FrontUser(telephone=telephone, username=username, password=password)
                    db.session.add(user)
                    db.session.commit()
                else:
                    return restful.params_error(message='该手机号已经被使用')
            except Exception as e:
                print(e)
            return restful.success()
        # 未通过验证
        else:
            # 打印错误
            error_info = form.get_error()
            print('未通过验证，错误信息：', error_info)
            # 返回错误信息
            return restful.params_error(message=error_info)


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        # 如果return_to 存在 && 不等于当前的url && 不等于注册页面的url && 安全
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            # 如果用户存在，并且密码验证通过
            if user and user.check_password(password):
                # 存储session信息
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True  # 31天cookie
                    return restful.success()
            else:
                return restful.params_error(message='手机号码或密码错误')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
