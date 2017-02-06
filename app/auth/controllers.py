from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash, send_from_directory
from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#Blueprint Module Creation
mod = Blueprint('auth', __name__, template_folder='templates')

#login manager flask-login
from app import app
from app import db

#from app.lockout.controllers import index

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
# login required decorator

@mod.route('/login', methods = ['POST', 'GET'])
def login():
    login_form=LoginForm(request.form)
    if login_form.validate_on_submit():
        user=db.session.query(User).filter_by(username=login_form.username.data).first()
        if user is not None:
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('lockout.index'))
        flash('Invalid Username or Password')
    return render_template('login.html', login_form=login_form)

@mod.route('/register', methods=['POST', 'GET'])
def register():
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        new_user=User(username=register_form.username.data, first_name=register_form.first_name.data,
                last_name=register_form.last_name.data, position=register_form.position.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You were registered. Please Login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', register_form=register_form)

@mod.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('auth.login'))
