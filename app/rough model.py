from . import db
from werkzeug.security import generate_password_hash

# participant Schema Model (evaluated)
class participant(db.Model):
    __tablename__ = 'participant'   # new ---------  

    participantID = db.Column(db.Integer, primary_key=True)   # new ---------  
    level = db.Column(db.String(50))   # new ---------  
    score = db.Column(db.Integer)   # new ---------  
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, level, score, fname, lname, email, password):
        self.level = level   # new ---------
        self.score = score   # new --------- ommm im not sure bc i thought og this as the 
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
            return unicode(self.participantID)  # python 2 support
        except NameError:
            return str(self.participantID)  # python 3 support

    def __repr__(self):
        return '<participant %r>' % (self.fname)
    
# administrator Schema Model (evaluated)
class administrator(db.Model):
    __tablename__ = 'administrator'

    administratorID= db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(10), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, fname, lname, email, password):
        # self.access_code = access_code  # Going to need to modify control to call GenerateAccessCode
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
            return unicode(self.administratorID)  # python 2 support
        except NameError:
            return str(self.administratorID)  # python 3 support

    def __repr__(self):
        return '<administrator %r>' % (self.fname)
    
# NOTICE: NEEDS TO BE REVISITED AND RETHOUGHT ABOUT --- WHAT ADMINS WILL SEE AND CHOOSE FROM
# ImageBank Schema Model
# class ImageBank(db.Model):
#     __tablename__ = 'imagebank'

#     bankID = db.Column(db.Integer, primary_key=True)

#     def __init__(self):
#         pass


# class View(db.Model):
#     __tablename__ = 'view'

#     participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'), primary_key=True)
#     lboardID = db.Column(db.Integer, db.ForeignKey('leaderboard.lboardID'), primary_key=True)

#     participant = db.relationship('Participant', backref='views')
#     leaderboard = db.relationship('Leaderboard', backref='views')

#     def __init__(self, participantID, lboardID):
#         self.participantID = participantID
#         self.lboardID = lboardID

# class Cache(db.Model):
#     __tablename__ = 'cache'

#     imgQuestionID = db.Column(db.Integer, db.ForeignKey('imagequestion.imgQuestionID'), primary_key=True)
#     bankID = db.Column(db.Integer, db.ForeignKey('imagebank.bankID'), primary_key=True)

#     image_question = db.relationship('ImageQuestion', backref='cache')
#     image_bank = db.relationship('ImageBank', backref='cache')

#     def __init__(self, imgQuestionID, bankID):
#         self.imgQuestionID = imgQuestionID
#         self.bankID = bankID

# class LinkedTo(db.Model):
# __tablename__ = 'linkedto'

#     quizID = db.Column(db.Integer, db.ForeignKey('quiz.quizID'), primary_key=True)
#     bankID = db.Column(db.Integer, db.ForeignKey('imagebank.bankID'), primary_key=True)

#     quiz = db.relationship('Quiz', backref='linked_banks')
#     image_bank = db.relationship('ImageBank', backref='linked_quizzes')

#     def __init__(self, quizID, bankID):
#         self.quizID = quizID
#         self.bankID = bankID

# Model Related Routes
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
