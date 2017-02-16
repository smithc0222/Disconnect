#create db and populate with data.
from app import db
from app.auth.models import User
from app.lockout.models import Lockout,Lockout_Line, Open_Table, Accepted_Table, Implemented_Table, Released_Table, Cleared_Table

db.drop_all()
db.create_all()

db.session.add(User(username='csmith',first_name='Chase',last_name='Smith',position='Dev'))
db.session.add(User(username='dlaflamme',first_name='Dave',last_name='LaFlamme',position='Maintenance Manager'))
db.session.add(User(username='bfurby', first_name='Belinda',last_name='Furby',position='Safety Manager'))

user1=db.session.query(User).first()
user2=db.session.query(User).filter_by(id=2).first()
user3=db.session.query(User).filter_by(id=3).first()
db.session.commit()

lockout1=Lockout(lockout_number='020217-1', lockout_description='Test lockout',
                lockout_status=1, goggles=0, faceshield=0, fullface=0, dustmask=0,
                leathergloves=0, saranax=0, nitrilegloves=0,
                chemicalsuit=0, chemicalgloves=0, tyrex=0,
                rubberboots=0, sar=0, ppe='' )
db.session.add(lockout1)
db.session.commit()

open1=Open_Table(open_status=1, created_by=user1, lockout=lockout1, date=None)
db.session.add(open1)
db.session.commit()

implemented1=Implemented_Table(1, user2, lockout1, None)
db.session.add(implemented1)
db.session.commit()

accepted1=Accepted_Table(accepted_status=1, accepted_by=user2, lockout=lockout1, date=None)
db.session.add(accepted1)
db.session.commit()

released1=Released_Table(released_status=1, released_by=user2, lockout=lockout1, date=None)
db.session.add(released1)
db.session.commit()

cleared1=Cleared_Table(cleared_status=1, cleared_by=user1, lockout=lockout1, date=None)
db.session.add(cleared1)
db.session.commit()

lockoutline1=Lockout_Line('V929-00','Test Valve','open','close',lockout1)
db.session.add(lockoutline1)

db.session.commit()
