from . import db
from werkzeug.security import generate_password_hash

# Student Schema Model
class Participant(db.Model):
    __tablename__ = 'participant'

    participant_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.participant_id)  # python 2 support
        except NameError:
            return str(self.participant_id)  # python 3 support

    def __repr__(self):
        return '<Participant %r>' % (self.fname)
    
# Teacher Schema Model
class Administrator(db.Model):
    __tablename__ = 'administrator'

    admin_id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(10), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, access_code, fname, lname, email, password):
        self.access_code = access_code
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.admin_id)  # python 2 support
        except NameError:
            return str(self.admin_id)  # python 3 support

    def __repr__(self):
        return '<Admin %r>' % (self.fname)