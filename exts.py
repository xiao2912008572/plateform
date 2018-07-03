# @Author: xiaojingyuan
# @Date: 2018-06-08 16:36:56
# @Last Modified by:   xiaojingyuan
# @Last Modified time: 2018-06-08 16:36:56

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayu import AlidayuAPI

db = SQLAlchemy()
mail = Mail()
alidayu = AlidayuAPI()
