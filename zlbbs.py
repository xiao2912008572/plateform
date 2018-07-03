from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
import config
from exts import db, mail, alidayu
from flask_wtf import CSRFProtect  # 添加csrf保护模块


# from utils.captcha import Captcha


# 工厂函数：用于注册
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 注册蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)

    # 分别用db、mail、alidayu对象初始化app
    db.init_app(app)
    mail.init_app(app)
    alidayu.init_app(app)

    CSRFProtect(app)  # 这样就可以拥有CSRF保护了

    return app


# 生成验证码
# Captcha.gene_graph_captcha()

# config.py / exts.py / models.py / manage.py
# 前台 、 后台 、 公共部分

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
