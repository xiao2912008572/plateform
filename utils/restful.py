from flask import jsonify


# http状态码 - 转code码
class HttpCode(object):
    ok = 200
    unautherror = 401
    paramerror = 400
    servererror = 500


# 对jsonify进行封装，传入code，message，data
def restful_result(code, message, data):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return jsonify(
        {
            'code': code,
            'message': message,
            'data': data or {}
        }
    )


def success(message=None, data=None):
    '''
    成功 200
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message=''):
    '''
    未授权 401
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.unautherror, message=message, data=None)


def params_error(message=''):
    '''
    参数错误 400
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.paramerror, message=message, data=None)


def server_error(message=''):
    '''
    服务器错误 500
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None)
