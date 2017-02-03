#create db and populate with data.
from app import db
from models import *


db.drop_all()
db.create_all()

db.session.add(User(username='csmith',first_name='Chase',last_name='Smith',position='Dev'))
db.session.add(User(username='dlaflamme',first_name='Dave',last_name='LaFlamme',position='Maintenance Manager'))
db.session.add(User(username='bfurby', first_name='Belinda',last_name='Furby',position='Safety Manager'))

user1=db.session.query(User).first()
db.session.commit()
lockout1=Lockout(lockout_number='02022017-1', lockout_description='Test lockout', lockout_author=user1,
                goggles=0, faceshield=0, fullface=0, dustmask=0,
                leathergloves=0, saranax=0, nitrilegloves=0,
                chemicalsuit=0, chemicalgloves=0, tyrex=0,
                rubberboots=0, sar=0, ppe='' )
db.session.add(lockout1)
db.session.commit()


lockoutline1=Lockout_Line('V929-00','Test Valve','open','close',lockout1)
db.session.add(lockoutline1)

db.session.commit()
