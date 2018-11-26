class Config(object):
    debug = True
    async_mode = None # 'eventlet' # may be gevent, not important
    SECRET_KEY="powerful secretkey"
    # WTF_CSRF_SECRET_KEY="a csrf secret key"
    names = ['dima', 'matvey', 'leva', 'ira', 'valia']