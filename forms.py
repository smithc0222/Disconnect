from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class RegisterForm(Form):
    username=StringField('Trinity Email', validators=[InputRequired(), Email(message='I don\'t recognize your email')])
    password=PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), AnyOf(['secret','password'])])

class LoginForm(Form):
    username=StringField('Trinity Email', validators=[InputRequired(), Email(message='I don\'t recognize your email')])
    password=PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), AnyOf(['secret','password'])])

class LockoutForm(Form):
    lockout_description=StringField('Description', validators=[InputRequired(), Length(min=2, max=300)])
    goggles=BooleanField('Goggles')
    faceshield=BooleanField('Face Shield')
    fullface=BooleanField('Full Face Respirator')
    dustmask=BooleanField('Dust Mask')
    leathergloves=BooleanField('Leather Gloves')
    saranax=BooleanField('Saranax Suit')
    nitrilegloves=BooleanField('Nitrile Gloves')
    chemicalgloves=BooleanField('Chemical Gloves')
    chemicalsuit=BooleanField('Chemical Suit')
    tyrex=BooleanField('Tyrex Suit')
    rubberboots=BooleanField('Rubber Boots')
    sar=BooleanField('SAR')
    ppe=StringField('Other PPE:')

class LockoutLineForm(Form):
    valve_number=StringField(u'',validators=[InputRequired(), Length(max=10)])
    line_description=StringField(u'',validators=[Length(max=50)])
    lock_position=SelectField(u'', choices=[('open','Open'),('close','Close')])
    removal_position=SelectField(u'', choices=[('open','Open'),('close','Close')])
