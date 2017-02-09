from app import db
from datetime import datetime

class Lockout(db.Model):

    __tablename__="lockout"
    id=db.Column(db.Integer, primary_key=True)
    lockout_number=db.Column(db.String(10), nullable=False)
    lockout_description=db.Column(db.String(200), nullable=False)
    lockout_file=db.Column(db.String(20), nullable=True)
    pid_file=db.Column(db.String(20), nullable=True)
    goggles=db.Column(db.Boolean(), default=False)
    faceshield=db.Column(db.Boolean(),default=False)
    fullface=db.Column(db.Boolean(), default=False)
    dustmask=db.Column(db.Boolean(), default=False)
    leathergloves=db.Column(db.Boolean(), default=False)
    saranax=db.Column(db.Boolean(), default=False)
    nitrilegloves=db.Column(db.Boolean(), default=False)
    chemicalgloves=db.Column(db.Boolean(), default=False)
    chemicalsuit=db.Column(db.Boolean(),default=False)
    tyrex=db.Column(db.Boolean(),default=False)
    rubberboots=db.Column(db.Boolean(),default=False)
    sar=db.Column(db.Boolean(),default=False)
    ppe=db.Column(db.String(50))

    def __init__(self, lockout_number, lockout_description, goggles, faceshield,
        fullface, dustmask, leathergloves, saranax, nitrilegloves, chemicalsuit, chemicalgloves,
        tyrex, rubberboots, sar, ppe):
        self.lockout_number=lockout_number
        self.lockout_description=lockout_description
        self.goggles=goggles
        self.faceshield=faceshield
        self.fullface=fullface
        self.dustmask=dustmask
        self.leathergloves=leathergloves
        self.saranax=saranax
        self.nitrilegloves=nitrilegloves
        self.chemicalsuit=chemicalsuit
        self.chemicalgloves=chemicalgloves
        self.tyrex=tyrex
        self.rubberboots=rubberboots
        self.sar=sar
        self.ppe=ppe

    def __repr__(self):
        return 'Lockout: {}'.format(self.lockout_number)

class Open_Table(db.Model):

    __tablename__="open_table"
    id=db.Column(db.Integer, primary_key=True)
    open_status=db.Column(db.Boolean(), default=True)
    created_by = db.relationship('User', backref=db.backref('created_by', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout=db.relationship('Lockout', backref=db.backref('open_lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))
    date=db.Column(db.DateTime)

    def __init__(self, open_status, created_by, lockout, date=None):
        self.open_status=open_status
        self.created_by=created_by
        self.lockout=lockout
        if date is None:
            date = datetime.utcnow()
        self.date=date

    def __repr__(self):
        return 'Open by: {} | Lockout Desc: {}'.format(self.created_by, self.lockout.lockout_description)

class Implemented_Table(db.Model):

    __tablename__="implemented_table"
    id=db.Column(db.Integer, primary_key=True)
    implemented_status=db.Column(db.Boolean(), default=True)
    implemented_by= db.relationship('User', backref=db.backref('implemented_by', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout=db.relationship('Lockout', backref=db.backref('implemented_lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))
    date=db.Column(db.DateTime)

    def __init__(self, implemented_status, implemented_by, lockout, date=None):
        self.implemented_status=implemented_status
        self.implemented_by=implemented_by
        self.lockout=lockout
        if date is None:
            date = datetime.utcnow()
        self.date=date

    def __repr__(self):
        return 'Implemented by: {} | Lockout Desc: {}'.format(self.implemented_by, self.lockout.lockout_description)

class Accepted_Table(db.Model):

    __tablename__="accepted_table"
    id=db.Column(db.Integer, primary_key=True)
    accepted_status=db.Column(db.Boolean(), default=True)
    accepted_by = db.relationship('User', backref=db.backref('accepted_by', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout=db.relationship('Lockout', backref=db.backref('accepted_lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))
    date=db.Column(db.DateTime)

    def __init__(self, accepted_status, accepted_by, lockout, date=None):
        self.accepted_status=accepted_status
        self.accepted_by=accepted_by
        self.lockout=lockout
        if date is None:
            date = datetime.utcnow()
        self.date=date

    def __repr__(self):
        return 'Accepted by: {} | Lockout Desc: {}'.format(self.accepted_by, self.lockout.lockout_description)

class Released_Table(db.Model):

    __tablename__="released_table"
    id=db.Column(db.Integer, primary_key=True)
    released_status=db.Column(db.Boolean(), default=True)
    released_by = db.relationship('User', backref=db.backref('released_by', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout=db.relationship('Lockout', backref=db.backref('released_lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))
    date=db.Column(db.DateTime)

    def __init__(self, released_status, released_by, lockout, date=None):
        self.released_status=released_status
        self.released_by=released_by
        self.lockout=lockout
        if date is None:
            date = datetime.utcnow()
        self.date=date

    def __repr__(self):
        return 'Released by: {} | Lockout Desc: {}'.format(self.released_by, self.lockout.lockout_description)

class Cleared_Table(db.Model):

    __tablename__="cleared_table"
    id=db.Column(db.Integer, primary_key=True)
    cleared_status=db.Column(db.Boolean(), default=True)
    cleared_by = db.relationship('User', backref=db.backref('cleared_by', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout=db.relationship('Lockout', backref=db.backref('cleared_lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))
    date=db.Column(db.DateTime)

    def __init__(self, cleared_status, cleared_by, lockout, date=None):
        self.cleared_status=cleared_status
        self.cleared_by=cleared_by
        self.lockout=lockout
        if date is None:
            date = datetime.utcnow()
        self.date=date

    def __repr__(self):
        return 'Cleared by: {} | Lockout Desc: {}'.format(self.cleared_status, self.lockout.lockout_description)

class Lockout_Line(db.Model):

    __tablename__="lockout_line"
    id=db.Column(db.Integer, primary_key=True)
    valve_number=db.Column(db.String(10), nullable=False)
    line_description=db.Column(db.String(50), nullable=True)
    lock_position=db.Column(db.String(10), nullable=False)
    removal_position=db.Column(db.String(10), nullable=False)
    lockout=db.relationship('Lockout', backref=db.backref('lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))

    def __init__(self, valve_number, line_description,lock_position, removal_position, lockout):
        self.valve_number=valve_number
        self.line_description=line_description
        self.lock_position=lock_position
        self.removal_position=removal_position
        self.lockout=lockout

    def __repr__(self):
        return 'Valve #: {} | Lockout ID: {}'.format(self.valve_number, self.lockout.id)
