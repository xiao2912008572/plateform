from .views import bp  # . 代表上层目录，当前为apps.cms

# 这里必须导入，因为在主app目录：zlbbs.py文件中
import apps.cms.hooks
