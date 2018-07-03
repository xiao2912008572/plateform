#encoding: utf-8

from urllib.parse import urlparse,urljoin
from flask import request

# 判断url是否安全
def is_safe_url(target):
    # urlparse对url进行解析，url path parameter 三个部分
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc