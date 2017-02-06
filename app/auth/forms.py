from flask_wtf import Form
from app.auth.models import User
from wtforms import StringField, BooleanField, PasswordField, SelectField, validators, ValidationError

class LoginForm(Form):
    username=StringField('Username', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.AnyOf(message='Wrong Password. Maybe a secret', values=['secret', 'password', 'admin'])])

class RegisterForm(Form):
    username=StringField('Username', [validators.Length(min=6, max=15)])
    first_name=StringField('First Names', [validators.Length(min=2, max=15)])
    last_name=StringField('Last Name', [validators.Length(min=2, max=15)])
    position=StringField('Position', [validators.Length(min=2, max=20)])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
