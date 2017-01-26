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
    filename=db.Column(db.String(300), nullable=True)

    data=db.column(db.LargeBinary)
    date=db.Column(db.DateTime)
    ppe=db.Column(db.String(50), nullable=True)


    def __init__(self, description, lockout_author, ppe, date=None):
        self.description=description
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.lockout_author=lockout_author
        self.ppe=ppe

    def __repr__(self):
        return 'Lockout: {}'.format(self.id)

class Lockout_Line(db.Model):

    __tablename__="lockout_line"
    id=db.Column(db.Integer, primary_key=True)
    valve_number=db.Column(db.String(10), nullable=False)
    description=db.Column(db.String(50), nullable=True)
    lock_position=db.Column(db.String(10), nullable=False)
    removal_position=db.Column(db.String(10), nullable=False)
    lockout=db.relationship('Lockout', backref=db.backref('lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))

    def __init__(self, description, valve_number, lock_position, removal_position, lockout):
        self.valve_number=valve_number
        self.description=description
        self.lock_position=lock_position
        self.removal_position=removal_position
        self.lockout=lockout

    def __repr__(self):
        return 'Valve #: {} | Lockout ID: {}'.format(self.valve_number, self.lockout.id)
