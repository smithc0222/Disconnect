#create db and populate with data.
from app import db
from models import *


db.drop_all()
db.create_all()

db.session.add(User(username='csmith',first_name='Chase',last_name='Smith',position='Dev'))
db.session.add(User(username='dlaflamme',first_name='Dave',last_name='LaFlamme',position='Maintenance Manager'))
db.session.commit()
