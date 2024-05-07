from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, RadioField, DateField, FieldList, FormField, BooleanField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
# from werkzeug.utils import secure_filename

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired(message='First name is required')])
    lname = StringField('Last Name', validators=[InputRequired(message='Last name is required')])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(message='Password is required')])
    account_type = SelectField('Account Type', choices=[('participant', 'Student'), ('admin', 'Administrator')], validators=[InputRequired(message='Please select user type')])
class TextQuestionForm(FlaskForm):
    question = StringField('Question', validators=[InputRequired()])
    difficulty = IntegerField('Difficulty', validators=[InputRequired()])
    marks = IntegerField('Marks', validators=[InputRequired()])
    answer = StringField('Answer', validators=[InputRequired()])

class ImageQuestionForm(FlaskForm):
    question = StringField('Question', validators=[InputRequired()])
    difficulty = IntegerField('Difficulty', validators=[InputRequired()])
    marks = IntegerField('Marks', validators=[InputRequired()])
    answer = StringField('Answer', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[
        FileRequired(message='Please upload a photo'),
        FileAllowed(['jpg', 'png'], message='Only JPEG and PNG images are allowed.')
    ])

class LessonPlan(FlaskForm):
    topic = StringField('Topic', validators=[InputRequired()])
    NoQues = IntegerField('# of Questions', validators=[InputRequired()])
    due_date = DateField('Due Date', validators=[InputRequired()])
    overall_difficulty = overall_difficulty = SelectField('Overall Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[InputRequired()])
    make_custom_questions = BooleanField('Custom Questions')

    text_questions = FieldList(FormField(TextQuestionForm))
    image_questions = FieldList(FormField(ImageQuestionForm))
