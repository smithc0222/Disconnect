#default config
import os, pdfkit
class BaseConfig(object):
    DEBUG = True
    SECRET_KEY='xf9xa6Xbx9xecyxae0>z%xf2m'
    SQLALCHEMY_DATABASE_URI='sqlite:///lockout.db'
    UPLOAD_FOLDER = '/home/chasesmith/mysite/lockout/static/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class TrinityDevelopmentConfig(BaseConfig):
    DEBUG = True
    UPLOAD_FOLDER='C:\\users\\csmith\\desktop\\lockoutproto\\lockout\\static\\uploads'
class PythonAnywhereConfig(BaseConfig):
    UPLOAD_FOLDER='/home/chasesmith/mysite/lockout/static/uploads'
