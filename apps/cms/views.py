from flask import Blueprint, views, g, jsonify  # 所有模板中都可以访问g对象
from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for
)
from .forms import (
    LoginForm,
    ResetPwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddProjectForm,
    UpdateProjectForm
)
from .models import (
    CMSUser,
    CMSPersmission,
    EoProject,
    EoApiEnv,
    EoApiEnvFrontUri,
    EoApiEnvHeader,
    EoApiEnvParam,
    EoApiEnvAdditionalParam
)
from ..models import BannerModel
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message  # 导入Message类
from utils import restful, zlcache, safeutils
import string
import random
from datetime import datetime

# 蓝图 (全局的): 蓝图名字 - __name__ - url前缀
bp = Blueprint("cms", __name__, url_prefix='/cms')


# 🌟 cms后台管理系统的首页 - 查看项目
@bp.route('/')
@login_required
def index():
    # 1. 从数据库中查找所有的project，指定排序，创建时间倒序排序
    projects = EoProject.query.order_by(EoProject.projectUpdateTime.desc()).all()
    return render_template('cms/cms_parent_base.html', projects=projects)  # 父根模板


# 🌟 cms后新增新项目
@bp.route('/aproject/', methods=['POST'])
@login_required
def aproject():
    # 1. 验证器
    form = AddProjectForm(request.form)
    # 验证通过
    if form.validate():
        projectName = form.projectName.data
        projectType = form.projectType.data
        projectVersion = form.projectVersion.data
        project = EoProject(projectType=projectType, projectName=projectName, projectVersion=projectVersion, projectCreateTime=datetime.now())
        db.session.add(project)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# 🌟 cms后台更新项目
@bp.route('/uproject/', methods=['POST'])
@login_required
def uproject():
    # 1. 验证起
    form = UpdateProjectForm(request.form)
    if form.validate():
        projectID = form.projectID.data
        projectName = form.projectName.data
        projectType = form.projectType.data
        projectVersion = form.projectVersion.data

        # 2. 获取project_id的project
        project = EoProject.query.get(projectID)
        if project:
            project.projectType = projectType
            project.projectVersion = projectVersion
            project.projectName = projectName
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个项目！')
    else:
        return restful.params_error(message=form.get_error())


# 🌟 cms后台删除项目
@bp.route('/dproject/', methods=['POST'])
@login_required
def dproject():
    # 1. 获取projectID
    project_id = request.form.get("projectID")

    # 2. 如果没有project_id
    if not project_id:
        return restful.params_error(message='请输入项目id！')

    # 3. 根据传过来的project_id没有找到project信息
    project = EoProject.query.get(project_id)
    if not project:
        return restful.params_error(message='没有这个项目！')
    db.session.delete(project)
    db.session.commit()
    return restful.success()


# 🌟 cms后台管理项目的首页
@bp.route('/project_index')
@login_required
def project_index():
    # 将projectID存到session中
    print(request.args.get('projectID'))
    print(type(request.args.get('projectID')))
    session[config.CMS_PROJECT_ID] = request.args.get('projectID')
    return render_template('cms/cms_project.html')


# 🌟 cms后台管理系统的注销
@bp.route('/logout/')
@login_required
def logout():
    # 方式一：清空session:略显暴力
    # session.clear()

    # 方式二：删除session中的config.CMS_USER_ID
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 🌟 cms后台管理系统的个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 🌟 cms后台管理系统的修改邮箱获取验证码
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    # 0. 邮箱验证:正则校验
    # 通过验证：
    email = request.args.get('email')
    import re
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}| \
            [0-9]{1,3})(\\]?)$", email) is not None:
        # /email_capicha/?email=xxx@qq.com - 通过查询字符串的形式将邮箱传递到后台
        # 1. 查询字符串
        email = request.args.get('email')
        if not email:
            return restful.params_error('请传递邮箱参数！')

        # 2. 产生验证码
        # 2.1 a-zA-Z的字符串
        source = list(string.ascii_letters)

        # 2.2 将一个列表的值更新到另一个列表中，利用list.extend()
        # 方法1
        # source.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

        # 方法2
        # map(func,obj) 将obj(需要可迭代的对象)的数据传递到函数中，然后处理后再返回
        # lambda函数：匿名函数
        # lambda x:str(x) 定义一个匿名函数，变量为x,处理方式为将x传入到str()中，进行字符串转义
        source.extend(map(lambda x: str(x), (range(0, 10))))

        # 2.3 随机采样
        # sample 采样器，从source中随机选择6个，返回值为列表
        list_captcha = random.sample(source, 6)

        # 将字符串转换成列表
        captcha = "".join(list_captcha)

        # 3.给这个邮箱发送邮件
        message = Message(
            '武汉柠檬班论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
        try:
            mail.send(message)
        except Exception as e:
            return restful.server_error()
        # 4. 存验证码,key=email,value=captcha
        zlcache.set(email, captcha)

        return restful.success()
    else:
        return restful.params_error(message='请输入正确的邮箱格式！')


# '''
#     测试邮箱发送邮件
# '''

# @bp.route('/email/')
# def send_email():
#     message = Message('邮件发送', recipients=['1668319858@qq.com'], body='测试')
#     mail.send(message)
#     return '邮件发送成功！'


# 🌟 帖子管理
# @bp.route('/posts/')
# @login_required
# @permission_required(CMSPersmission.POSTER)
# def posts():
#     return render_template('cms/cms_posts.html')  #


# 🌟 项目概况
@bp.route('/projectOverview/')
@login_required
@permission_required(CMSPersmission.POSTER)
def projectOverview():
    return render_template('cms/cms_projectOverview.html')


# # 🌟 评论管理
# @bp.route('/comments')
# @login_required
# @permission_required(CMSPersmission.COMMENTER)
# def comments():
#     return render_template('cms/cms_comments.html')

# 🌟 API接口-快速测试
@bp.route('/projectApiQuickTest')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def projectApiQuickTest():
    return render_template('cms/cms_projectApiQuickTest.html')


# 🌟 API接口-所有接口
@bp.route('/projectAllApi')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def projectApiAll():
    return render_template('cms/cms_projectAllApi.html')


# TODO:测试iframe
@bp.route('/projectEnv_iframe/')
@login_required
def projectEnv_iframe():
    # 1. 拿到项目ID
    projectID = g.cms_project_id  # str类型

    # 2. 拿到环境ID
    envID = request.args.get('envID')
    print('evnID = ', envID)

    # 如果没有拿到环境ID，默认显示第一个
    if envID == None:
        # # 3. 查询各参数
        envs = EoApiEnv.query.filter_by(projectID=int(projectID)).all()
        print(envs[0].envName)
        env = EoApiEnv.query.filter_by(envID=envID).first()
        env_uri = EoApiEnvFrontUri.query.filter_by(envID=envID).first()
        env_headers = EoApiEnvHeader.query.filter_by(envID=envID).all()
        env_addtionalparams = EoApiEnvAdditionalParam.query.filter_by(envID=envID).all()
        env_params = EoApiEnvParam.query.filter_by(envID=envID).all()

        return render_template(
            'cms/cms_projectEnv_iframe.html',
            envs=envs,
            env=env,
            env_uri=env_uri,
            env_headers=env_headers,
            env_addtionalparams=env_addtionalparams,
            env_params=env_params
        )
    else:
        envID = request.args.get('envID')

        # 3. 查询各参数
        envs = EoApiEnv.query.filter_by(projectID=int(projectID)).all()
        env = EoApiEnv.query.filter_by(envID=envID).first()
        env_uri = EoApiEnvFrontUri.query.filter_by(envID=envID).first()
        env_headers = EoApiEnvHeader.query.filter_by(envID=envID).all()
        env_addtionalparams = EoApiEnvAdditionalParam.query.filter_by(envID=envID).all()
        env_params = EoApiEnvParam.query.filter_by(envID=envID).all()

        return jsonify(
            {
                # 'envs': envs,
                'envName': env.envName,
                'envDesc': env.envDesc,
                'envUri': env_uri.uri,
                # 'env_headers': env_headers,
                # 'env_addtionalparams': env_addtionalparams,
                # 'env_params': env_params
            })


# 🌟 API接口-新增环境
@bp.route('/aprojectEnv/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def aprojectEnv():
    # 1. 声明对象
    env = EoApiEnv(envName='测试环境', envDesc='application/x-www-form-urlencoded')
    project = EoProject(projectType=1, projectName='测试项目111', projectVersion='1.1')
    uri = EoApiEnvFrontUri(uri='giant.dev.yunlu6.com')
    header1 = EoApiEnvHeader(headerName='Accept-Encoding1', headerValue='gzip')
    header2 = EoApiEnvHeader(headerName='Accept-Encoding2', headerValue='gzip')
    header3 = EoApiEnvHeader(headerName='Accept-Encoding3', headerValue='gzip')

    param = EoApiEnvParam(paramKey='token', paramValue='asdfjkj123kjdfjskdsadf')
    additionalparam = EoApiEnvAdditionalParam(paramKey='addtional_token', paramValue='13849sdf87a8d09fqherjhadf')

    # 2. 分别添加
    # 正向添加：一对多关系
    project.apienv.append(env)

    # 正向添加：一对一关系
    env.uri = uri

    # 正向添加：一对多关系
    env.header.append(header1)
    env.header.append(header2)
    env.header.append(header3)
    env.param.append(param)
    env.additionalparam.append(additionalparam)

    # 3.提交插入
    db.session.add(project)
    db.session.add(env)

    # 4.提交执行
    db.session.commit()
    return restful.success()


# 🌟 板块管理
@bp.route('/boards')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')


# 🌟 前台用户管理
@bp.route('/fusers')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


# 🌟 后台用户管理
@bp.route('/cusers')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


# 🌟 CMS角色管理
@bp.route('/croles')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


# 🌟 CMS轮播图管理
@bp.route('/banners/')
@login_required
def banners():
    # 从数据库中：查找所有的banner,指定排序，priority的从大到小排序
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


# 🌟 CMS添加轮播图
@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    # 通过验证
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# 🌟 CMS编辑(更新)轮播图
@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    # 1. 验证器
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        # 2. 获取banner_id的banner
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


# 🌟 CMS删除轮播图
@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    # 1. 获取传过来的banner_id
    banner_id = request.form.get('banner_id')

    # 2. 如果没有banner_id
    if not banner_id:
        return restful.params_error(message='请输入轮播图id！')

    # 3. 根据传过来的banner_id没有找到banner信息
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


# 🌟 类视图:登录类视图
class LoginView(views.MethodView):
    def get(self, message=None):
        # 🌟 cms后台管理系统登录页
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            # 1. 先通过email的唯一性查询到CMSUser表中的user对象
            user = CMSUser.query.filter_by(email=email).first()

            # 2. 验证密码：如果user存在，并且检查了密码之后
            if user and user.check_password(password):
                # 保存用户登录信息，保存在session中，session是用字典存取CMS_USER_ID
                session[config.CMS_USER_ID] = user.id
                # 如果用户点了记住我
                if remember:
                    # 如果设置session.permanent = True
                    # 那么过期时间是31天
                    # session持久化，默认是31天
                    session.permanent = True
                # ⚠️ 这里url_for()进行反转的时候，必须先写：蓝图名.index
                # 🌟 跳转到cms后台管理首页
                # return redirect(url_for('cms.index'))
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误!')
        else:
            # 返回 ('password',['请输入正确格式的密码']) [1][0]
            message = form.errors.popitem()[1][0]  # forms.errors.popitem返回字典的任意一项
            return self.get(message=message)


# 🌟 修改密码类视图
class ResetPwdView(views.MethodView):
    # 在类视图中调用装饰器
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        # 表单验证通过
        if form.validate():
            # 1. 拿到oldpwd
            oldpwd = form.oldpwd.data
            # 2. 拿到newpwd
            newpwd = form.newpwd.data
            # 从`g`对象上先拿到user
            user = g.cms_user
            # 验证密码：
            if user.check_password(oldpwd):
                # 验证成功之后，将新密码设置到user.passwrod中
                user.password = newpwd
                db.session.commit()
                # 因为请求是通过ajax发送过来的，所以返回给前端的数据也要用json数据来返回
                '''
                返回的格式一般采用：
                    :params code: 代表状态返回码
                    :params mssage: 代表返回信息
                Example usage::
                    {'code' : 200 , 'message' : 'xxxxx'}
                '''
                # return jsonify({'code': 200, 'message': '密码修改成功'})
                return restful.success()
            else:
                # return jsonify({'code': 400, 'message': '旧密码错误！'})
                return restful.params_error(message='旧密码错误！')
        else:
            # 获取错误信息
            # message = form.get_error()
            # return message
            return restful.params_error(message=form.get_error())


# 🌟 重设邮箱类视图
class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        # 1. 验证表单
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


# 将类视图`LoginView`注册到路由规则中,并且命名为login，在url_for反转时，填写login
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

# 将类视图`ResetPwdView`注册到路由规则中,并且命名为login，在url_for反转时，填写resetpwd
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))

bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
