#create db and populate with data.
from app import db
from models import *


db.drop_all()
db.create_all()

db.session.add(User(username='csmith',first_name='Chase',last_name='Smith',position='Dev'))
db.session.add(User(username='dlaflamme',first_name='Dave',last_name='LaFlamme',position='Maintenance Manager'))
db.session.commit()

user1=db.session.query(User).first()
db.session.add(Lockout(description='Lockout P856 for internal inspection', lockout_author=user1, ppe='Need some extra something'))
db.session.add(Lockout(description='Lockout HCL Burner to change flame arrestor', lockout_author=user1, ppe='None'))
db.session.commit()

lockouts=db.session.query(Lockout).all()
lockout1=lockouts[0]
lockout2=lockouts[1]
db.session.add(Lockout_Line(valve_number='V844-10', description='Stripper discharge line',lock_position='Open',removal_position='Close', lockout=lockout1))
db.session.add(Lockout_Line(valve_number='V844-23', description='',lock_position='Close',removal_position='Open', lockout=lockout1))
db.session.add(Lockout_Line(valve_number='V553-11',description='East side of burner skid',lock_position='Close',removal_position='Open', lockout=lockout2))

db.session.commit()
