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
    ppe=StringField('Additional PPE')

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
        return render_template('upload.html')
    else:
        lockout=db.session.query(Lockout).first()
        lockout_line=db.session.query(Lockout_Line).all()
    return render_template('upload.html', lockout=lockout, lockout_line=lockout_line)


@app.route('/lockout', methods=['POST', 'GET'])
def lockout():
    user=db.session.query(User).first()
    lockout_form=LockoutForm()
    today=date.today()
    user=db.session.query(User).first()
    lockout=db.session.query(Lockout).all()
    last_lockout=lockout[-1]
    if request.method == "POST":
        new_lockout=db.session.add(Lockout(description=lockout_form.description.data,lockout_author=user,ppe=lockout_form.ppe.data))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('lockout.html', lockout=lockout, user=user, today=today, last_lockout=last_lockout, lockout_form=lockout_form)

@app.route('/lockout/<int:this_lockout_id>', methods=['GET'])
def this_lockout(this_lockout_id):
    this_lockout_id-=1
    lockout=db.session.query(Lockout).all()
    this_lockout=lockout[this_lockout_id]
    lockout_line=db.session.query(Lockout_Line).filter_by(lockout_id=this_lockout_id).all()
    return render_template('upload.html', this_lockout=this_lockout, lockout_line=lockout_line)


@app.route('/')
def index():
    today=date.today()
    user=db.session.query(User).first()
    lockout=db.session.query(Lockout).all()
    return render_template('index.html', lockout=lockout, user=user, today=today)


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
