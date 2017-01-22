#default config

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY='something'
    SQLALCHEMY_DATABASE_URI='sqlite:///trinitymfgworkorder.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
