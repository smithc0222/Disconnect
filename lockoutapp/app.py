from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_bootstrap import Bootstrap
from io import BytesIO


#create app object
app = Flask(__name__)


#config
import os
app.config.from_object('config.DevelopmentConfig')

#create sqlalchemy object
db = SQLAlchemy(app)

#instantiate bootstrap
Bootstrap(app)

from models import *
# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

class LockoutForm(Form):
    description=StringField('Description', validators=[InputRequired()])


class LoginForm(Form):
    username=StringField('Trinity Email', validators=[InputRequired(), Email(message='I don\'t recognize your email')])
    password=PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), AnyOf(['secret','password'])])

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/upload', methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files['inputFile']
        this_file=db.session.query(Lockout).first()
        this_file.filename=filename=files.filename
        this_file.data=files.read()
        db.session.commit()
        return 'file uploaded'
    return render_template('upload.html')


@app.route('/lockout', methods=['POST', 'GET'])

def lockout():
    lockout=db.session.query(Lockout).first()
    return render_template('lockout.html', lockout=lockout)

@app.route('/')
def index():
    lockout=db.session.query(Lockout).first()
    return render_template('index.html', lockout=lockout)


class RegisterForm(Form):
    username=StringField('Trinity Email', validators=[InputRequired(), Email(message='I don\'t recognize your email')])
    password=PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), AnyOf(['secret','password'])])

@app.route('/register', methods=['POST', 'GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
