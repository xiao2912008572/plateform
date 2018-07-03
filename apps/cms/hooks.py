from .views import bp
import config
from flask import session, g
from .models import CMSUser, CMSPersmission


# ⚠️ 这个钩子函数的目的是，发起当前页面的请求之前，就检查函数中的内容
# 在请求当前页面之前判断：来到视图函数之前会执行定义的钩子函数
@bp.before_request
def before_request():
    # 1. 判断是否登录
    # 🌟 因为在视图中，登录之后就讲CMS_USER_ID保存在了session中，所以可以用下面这个健是否在session中来确定是否登录
    if config.CMS_USER_ID in session:
        # 2. 如果登录，拿到用户ID
        user_id = session.get(config.CMS_USER_ID)  # 从session中拿到用户id
        user = CMSUser.query.get(user_id)  # 再去数据库中通过user_id查询到user对象
        # 如果user存在
        if user:
            # 通过flask.g对象，拿到user，然后这个g.cms_user可以在`模板`和`视图`中直接使用
            g.cms_user = user


# ⚠️  上下文钩子：这个钩子函数的目的是，只要是bp蓝图返回的模板，都会将这个添加到上下文(也就是这个变量)当中，那么所有的模板都可以使用这个变量
@bp.context_processor
def cms_context_processor():
    return {"CMSPermission": CMSPersmission}
