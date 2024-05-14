from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField, IntegerField, DateField, FieldList, FormField, BooleanField
from wtforms.validators import InputRequired, DataRequired
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
    repeat_password = PasswordField('Repeat Password', validators=[InputRequired(message='Password does not match!')])
    account_type = RadioField('Account Type', choices=[('participant', 'Student'), ('admin', 'Administrator')], validators=[InputRequired(message='Please select user type')])
class EnrolForm(FlaskForm):
    room_code = StringField('Access Code', validators=[InputRequired(message='Enter Access Code')])

class TextQuestionForm(FlaskForm):
    question = StringField('Question', validators=[InputRequired()])
    difficulty = SelectField('Question Difficulty', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Pro', 'Advanced')], validators=[InputRequired()])
    marks = IntegerField('Marks', validators=[InputRequired()])
    answer = StringField('Answer', validators=[InputRequired()])

class ImageQuestionForm(FlaskForm):
    question = StringField('Question', validators=[InputRequired()])
    difficulty = SelectField('Question Difficulty', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Pro', 'Advanced')], validators=[InputRequired()])
    marks = IntegerField('Marks', validators=[InputRequired()])
    answer = StringField('Answer', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[
        FileRequired(message='Please upload a photo'),
        FileAllowed(['jpg', 'png'], message='Only JPEG and PNG images are allowed.')
    ])

class LessonPlan(FlaskForm):
    topic = SelectField('Topic', choices=[('Alphabet', 'Alphabet'), ('Greetings', 'Greetings'), ('Polite Words', 'Polite Words')], validators=[InputRequired(message='Please select a topic')])
    num_questions = IntegerField('# of Questions', validators=[InputRequired()])
    due_date = DateField('Due Date', validators=[InputRequired()])
    overall_difficulty = SelectField('Quiz Difficulty', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Pro', 'Advanced')], validators=[InputRequired()])
    choose_from_bank = BooleanField('Would you like to Choose Existing Questions from Bank?')
    make_custom_questions = BooleanField('Would you like to add Custom Questions?')

    num_text_questions = IntegerField('Number of Text Questions')
    num_image_questions = IntegerField('Number of Image Questions')

    text_questions = FieldList(FormField(TextQuestionForm), min_entries=0)
    image_questions = FieldList(FormField(ImageQuestionForm), min_entries=0)