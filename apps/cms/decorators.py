from flask import session, redirect, url_for, g
from functools import wraps
import config


# 装饰器1:必须登录 - 不带参数的装饰器
def login_required(func):
    # 用@wraps装饰func，可以保留func的属性，参数信息不会被丢失
    @wraps(func)
    def inner(*args, **kwargs):
        # 1.判断user
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            # 重定向到
            return redirect(url_for('cms.login'))

    return inner


# 装饰器2：权限判断 - 带参数的装饰器
def permission_required(permission):
    # 内层装饰器(实际装饰器) - 用于接收参数
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))

        return inner

    return outter
