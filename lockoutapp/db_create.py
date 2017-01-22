#create db and populate with data.
from app import db
from models import User


db.drop_all()
db.create_all()

db.session.add(User('csmith','Chase','Smith','Dev'))
db.session.add(User('dlaflamme','Dave','LaFlamme','Maintenance Manager'))

db.session.commit()
