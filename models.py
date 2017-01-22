from app import db
from datetime import datetime, date
class User(db.Model):

    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True)
    first_name=db.Column(db.String(20), nullable=False)
    last_name=db.Column(db.String(20), nullable=False)
    position=db.Column(db.String(50), nullable=False)


    def __init__(self, username, first_name, last_name, position):
        self.username=username
        self.first_name=first_name
        self.last_name=last_name
        self.position=position

    def __repr__(self):
        return '{}'.format(self.username)

class Lockout(db.Model):

    __tablename__="lockout"
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(200), nullable=False)
    lockout_author = db.relationship('User', backref=db.backref('lockout_author', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    #associated_workorder_number= db.relationship('Workorder', backref=db.backref('associated_workorder_number', lazy='dynamic'))
    #workorder_id=db.Column('workorder_id', db.Integer, db.ForeignKey('workorder.id'))
    date=db.Column(db.DateTime)
    #ppe=db.Column(db.String(50), nullable=True)
    #lockbox=db.Column(db.String(50), nullable=False)
    #valve_number=db.Column(db.String(10), nullable=False)
    #lock_position=db.Column(db.String(10), nullable=F)
    def __init__(self, description, lockout_author, date=None):
        self.description=description
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.lockout_author=lockout_author

    def __repr__(self):
        return 'Lockout: {}'.format(self.lockout_author)
