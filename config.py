#default config

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY='something'
    SQLALCHEMY_DATABASE_URI='sqlite:///lockout.db'
    UPLOAD_FOLDER = '/Users/Chase/Desktop/TrinityLockout/static/lockout'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class DevelopmentConfig(BaseConfig):
    DEBUG = True
