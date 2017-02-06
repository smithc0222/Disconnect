from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#create sqlalchemy object
db = SQLAlchemy(app)

#import blueprint from lockout module
from app.lockout.controllers import mod
from app.auth.controllers import mod

#register blueprint from lockout module
app.register_blueprint(lockout.controllers.mod)
app.register_blueprint(auth.controllers.mod)

#instantiate bootstrap
Bootstrap(app)

#app config
app.config.from_object('config.TrinityDevelopmentConfig')
