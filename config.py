#default config

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY='something'
    SQLALCHEMY_DATABASE_URI='sqlite:///lockout.db'
    UPLOAD_FOLDER = '/home/OhmsFlas/mysite/trinitylockout/static/lockout'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class DevelopmentConfig(BaseConfig):
    DEBUG = True
class PythonAnywhereConfig(BaseConfig):
    UPLOAD_FOLDER='/home/OhmsFlaw/mysite/trinitylockout/static/lockout'
