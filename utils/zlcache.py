'''
封装memcache缓存模块
'''
import memcache

# 连接memcached
cache = memcache.Client(['118.25.48.34:11211'], debug=True)


# 设置: 过期时间60秒
def set(key, value, timeout=60):
    '''
    设置键值对
    '''
    return cache.set(key, value, timeout)


# 获取
def get(key):
    return cache.get(key)


# 删除
def delete(key):
    return cache.delete(key)
