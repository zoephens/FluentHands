from . import db
from datetime import datetime
from sqlalchemy import Table, Column
from werkzeug.security import generate_password_hash
import random, string

# Define association tables
quiz_image_question = Table('quiz_image_question', db.Model.metadata,
    Column('quiz_id', db.Integer, db.ForeignKey('quiz.quizID')),
    Column('image_question_id', db.Integer, db.ForeignKey('image_question.imgQuestionID'))
)

quiz_camera_question = Table('quiz_camera_question', db.Model.metadata,
    Column('quiz_id', db.Integer, db.ForeignKey('quiz.quizID')),
    Column('cam_question_id', db.Integer, db.ForeignKey('cam_question.camQuestionID'))
)

# Student Schema Model
class Participant(db.Model):
    __tablename__ = 'participant'

    participantID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    level = db.Column(db.String(50), default='Beginner') 

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
            return unicode(self.participantID)  # python 2 support
        except NameError:
            return str(self.participantID)  # python 3 support
        
    def is_admin(self):
        return False
    
    def __repr__(self):
        return '<Participant %r>' % (self.fname)
    
# Teacher Schema Model
class Administrator(db.Model):
    __tablename__ = 'administrator'

    administratorID = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(10), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, fname, lname, email, password):
        self.access_code = self.generate_access_code()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
    def generate_access_code(self):
        code_first_part = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=3))
        code_second_part = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=3))
        return f"{code_first_part}-{code_second_part}"
    
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

    def is_admin(self):
        return True
    
    def __repr__(self):
        return '<Admin %r>' % (self.fname)

# Enrol Schema Model 
class Enrol(db.Model):
    __tablename__ = 'enrol'

    enrolID = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(10), db.ForeignKey('administrator.access_code'), nullable=False)
    participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'), nullable=False)
    score = db.Column(db.Integer, default=0) #Initializes Score to 0

    def __init__(self, accessCode, participantID):
        self.access_code = accessCode
        self.participantID = participantID

# ImageQuestion Schema Model
class ImageQuestion(db.Model):
    __tablename__ = 'image_question'

    imgQuestionID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255))
    label = db.Column(db.String(255)) # Answer to the question
    question = db.Column(db.String(1024))
    marks = db.Column(db.Integer)
    level = db.Column(db.String(255)) # Difficulty
    filename = db.Column(db.Text)
    adminID = db.Column(db.Integer, db.ForeignKey('administrator.administratorID'))

    def __init__(self, topic, label, marks, level, filename, question, adminID):
        self.topic = topic
        self.label = label
        self.question = question
        self.marks = marks
        self.level = level
        self.filename = filename
        self.adminID = adminID

# CamQuestion Schema Model
class CamQuestion(db.Model):
    __tablename__ = 'cam_question'

    camQuestionID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255))
    label = db.Column(db.String(255))
    question = db.Column(db.String(1024))
    marks = db.Column(db.Integer)
    level = db.Column(db.String(255))
    adminID = db.Column(db.Integer, db.ForeignKey('administrator.administratorID'))

    def __init__(self, topic, label, marks, level, question, adminID):
        self.topic = topic
        self.label = label
        self.question = question
        self.marks = marks
        self.level = level
        self.adminID = adminID

# Quiz Schema Model
class Quiz(db.Model):
    __tablename__ = 'quiz'

    quizID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255))
    numQuestions = db.Column(db.Integer)
    date = db.Column(db.Date, default=datetime.now) #Date it was created
    due_date = db.Column(db.Date)
    adminID = db.Column(db.Integer, db.ForeignKey('administrator.administratorID'))
    level = db.Column(db.String(64))
    
    # Relationship with ImageQuestion table
    image_questions = db.relationship('ImageQuestion', secondary=quiz_image_question, backref='quizzes')

    # Relationship with CameraQuestion table
    camera_questions = db.relationship('CamQuestion', secondary=quiz_camera_question, backref='quizzes')

    def __init__(self, topic, level, numQuestions, due_date, adminID):
        self.topic = topic
        self.level = level
        self.numQuestions = numQuestions
        self.due_date = due_date
        self.adminID = adminID

# Scores for each participant in each quiz
class Administered(db.Model):
    __tablename__ = 'administered'

    participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'), primary_key=True)
    quizID = db.Column(db.Integer, db.ForeignKey('quiz.quizID'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)

    participant = db.relationship('Participant', backref='administered')
    quiz = db.relationship('Quiz', backref='administered')

    def __init__(self, participantID, quizID, score, feedback=None):
        self.participantID = participantID
        self.quizID = quizID
        self.score = score
        self.feedback = feedback
# ---------------------------------------------------------------------------------------

# Leaderboard Schema Model
class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    lboardID = db.Column(db.Integer, primary_key=True)
    # score = db.Column(db.Integer)
    participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'))
    adminID = db.Column(db.Integer, db.ForeignKey('administrator.administratorID')) 

    def __init__(self, participantID, adminID):
        # self.score = score
        self.participantID = participantID
        self.adminID = adminID