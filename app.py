from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


#create app object
app = Flask(__name__)


#config
import os
app.config.from_object('config.DevelopmentConfig')


#create sqlalchemy object
db = SQLAlchemy(app)


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

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error=''
    user_lookup=db.session.query(User).all()
    if request.method == 'POST':
        if db.session.query(User).filter(User.username == request.form['username']).count() == 0:
            error = 'Invalid credentials. Please try again or Register.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/lockout', methods=['POST', 'GET'])
@login_required
def lockout():
    lockout=db.session.query(Lockout).first()
    return render_template('lockout.html', lockout=lockout)
@app.route('/')
def index():
    lockout=db.session.query(Lockout).first()
    return render_template('index.html', lockout=lockout)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
