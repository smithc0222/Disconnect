#default config

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY='xf9xa6Xbx9xecyxae0>z%xf2m'
    SQLALCHEMY_DATABASE_URI='sqlite:///lockout.db'
    UPLOAD_FOLDER = '/home/chasesmith/mysite/lockout/static/lockout'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class DevelopmentConfig(BaseConfig):
    DEBUG = True
class PythonAnywhereConfig(BaseConfig):
    UPLOAD_FOLDER='/home/chasesmith/mysite/lockout/static/lockout'

