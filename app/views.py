import os, json
from app import app, db, login_manager
from flask import jsonify, Response, render_template, request, redirect, url_for, flash, session, abort, send_from_directory, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from reportlab.pdfgen import canvas
from sqlalchemy import func

from app.models import Participant, Administrator, CamQuestion, ImageQuestion, Quiz, Leaderboard, Administered, Enrol
from app.forms import LoginForm, SignUpForm, LessonPlan, ImageQuestionForm, TextQuestionForm, EnrolForm

# Realtime Tracking
from tensorflow.keras.models import load_model # type: ignore
import numpy as np
from collections import Counter

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'action_new.h5')
label_path = os.path.join(current_dir, 'labels.json')

# Load the model
model = load_model(model_path)

with open(label_path, 'r') as file:
    # Actions that we try to detect
    actions = json.load(file)

# List to store predictions
all_predictions = []

###
# Routing for your application.
###
@app.route('/')
@login_required
def dashboard():
    """Render website's dashboard page."""
    first_name = current_user.fname

    if isinstance(current_user, Administrator):
        # If the current user is an admin
        admin = Administrator.query.filter_by(administratorID=current_user.administratorID).first()
        room_code = admin.access_code
        is_admin = True
    else:
        # If the current user is a participant
        participant = Participant.query.filter_by(participantID=current_user.participantID).first()
        enrol = Enrol.query.filter_by(participantID=current_user.participantID).first()
        room_code = enrol.access_code if enrol else None
        is_admin = False

    return render_template('dashboard.html', fname=first_name, room_code=room_code, is_admin=is_admin)

@app.route('/signup', methods=['POST', 'GET'])
def register():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        fname = signup_form.fname.data
        lname = signup_form.lname.data
        email = signup_form.email.data            
        password = signup_form.password.data
        account_type = signup_form.account_type.data

        print(account_type)
        if account_type == 'participant':
            participant = Participant(
                fname=fname,
                lname=lname,
                email=email,
                password=password
            )
            db.session.add(participant)

        elif account_type.lower() == 'admin':
            admin = Administrator(
                fname=fname,
                lname=lname,
                email=email,
                password=password
            )
            db.session.add(admin)

        try:
            db.session.commit()
            flash('Registration Successful', 'success')

            if account_type == 'participant':
                user = db.session.query(Participant).filter_by(email=email).first()
                login_user(user)
                return redirect(url_for('enrol'))
            elif account_type == 'admin':
                user = db.session.query(Administrator).filter_by(email=email).first()
                login_user(user)
                return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration Failed: {str(e)}', 'error')
    return render_template("signup.html", form=signup_form)

@app.route('/enrol', methods=['POST', 'GET'])
@login_required
def enrol():
    form = EnrolForm()

    if form.validate_on_submit():
        code = form.room_code.data
        # Check if code is in database

        enrol = Enrol(
            accessCode = code,
            participantID = current_user.participantID
        )
        db.session.add(enrol)

        try:
            db.session.commit()
            flash('Enrolment Successful', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            # flash(f'Enrolment Failed: {str(e)}', 'error')
            flash(f'Invalid Code', 'error')

    return render_template("roomcode.html", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Query the database for the user
        user = db.session.query(Participant).filter_by(email=email).first()

        if user is None:
            user = db.session.query(Administrator).filter_by(email=email).first()

        if user is not None:
            if check_password_hash(user.password, password):
                # Login successful, redirect to dashboard or other page
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        else:
            flash('User not found', 'error')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for("login"))

@app.route('/add_lesson', methods=['POST', 'GET'])
def add_lesson():
    """Render lesson plan page."""
    lesson_form = LessonPlan()
    image_form = ImageQuestionForm()
    text_form = TextQuestionForm()

    if lesson_form.validate_on_submit():
        adminID = current_user.id
        file = text_form.photo.data
    
        new_cam_question = CamQuestion(
            topic = lesson_form.topic.data,
            label = text_form.label.data,
            marks = text_form.marks.data,
            difficulty = text_form.level.data,
            adminID = adminID
        )

        new_image_question = ImageQuestion(
            topic = lesson_form.topic.data,
            label = text_form.label.data,
            marks = text_form.marks.data,
            difficulty = text_form.level.data,
            filename = secure_filename(file.filename),
            adminID = adminID
        )

        quiz = Quiz(
            topic = lesson_form.topic.data,
            noQues =lesson_form.numQuestions.data,
            due_date = lesson_form.due_date.data,
            adminID = adminID
        )

        db.session.add(quiz)
        db.session.commit()

        # if :
        db.session.add(new_cam_question)
        db.session.commit()
        # else:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        
        db.session.add(new_image_question)
        db.session.commit()

        flash('Lesson Created Successfully', 'success')
        return redirect(url_for('/'))

    return render_template('lesson_plan.html', lesson_form=lesson_form, image_form=image_form, text_form=text_form)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if current_user.is_authenticated:
        if isinstance(current_user, Administrator):
            # Delete admin account
            user_id = current_user.administratorID
            user = Administrator.query.get(user_id)
        else:
            # Delete participant account
            user_id = current_user.participantID
            user = Participant.query.get(user_id)

        if user:
            # Delete enrol records associated with the user
            Enrol.query.filter_by(participantID=user_id).delete()
            db.session.commit()

            # Delete the user account
            db.session.delete(user)
            db.session.commit()
            
            # Logout the user
            logout_user()

            flash('Your account has been successfully deleted.', 'success')
            return redirect(url_for('login'))

    flash('Failed to delete your account. Please try again.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/get_progress_report/<access_code>', methods=['GET'])
def get_progress_report(access_code):
    students_grades = Enrol.query.with_entities(Enrol.participantID, Enrol.score).filter(Enrol.access_code == access_code).all()

    # Create a new PDF file
    pdf_path = os.path.join(app.root_path, 'progress_report.pdf')  # Use app.root_path to get the root directory of your Flask app
    c = canvas.Canvas(pdf_path)
    y_position = 800

    # Write the grades to the PDF
    for student, grade in students_grades:
        c.drawString(100, y_position, f"{student}: {grade}")
        y_position -= 20  # Move the y position for the next line

    c.save()

    # Return the PDF file
    try:
        return send_file(pdf_path, as_attachment=True)
    except FileNotFoundError:
        return "PDF file not found", 404

@app.route('/keypoints', methods=['POST'])
def keypoints():
    global all_predictions
    try:
        keypoints_data = request.json
        sequence = keypoints_data
        most_common_prediction = ''

        if len(sequence) == 30:
            prediction = model.predict(np.expand_dims(sequence, axis=0))[0]
            action = actions[np.argmax(prediction)]
            all_predictions.append(action)
            # print(action)
        
            # Once we have 10 predictions, find the most frequent one
            if len(all_predictions) == 20:
                most_common_prediction = Counter(all_predictions).most_common(1)[0][0]
                print("-------------------------Most frequent prediction after 10 attempts:", most_common_prediction)
                all_predictions = []  # Reset predictions for the next set
                
        return jsonify({'message': 'Keypoint Received', 'data': keypoints_data, 'predicted_label': most_common_prediction}), 200
    except Exception as e:
        print("Error processing keypoints:", e)
        return jsonify({'message': 'Error processing keypoints'}), 500

@app.route('/quiz')
@login_required
def takequiz():
    """Render website's quiz page."""
    return render_template('quiz.html')

# --------------------------------------------------Functionality to implement

@app.route('/leaderboard<room_code>', methods=['GET'])
def leaderboard(room_code):
    # Join Participant and Enrol tables, group by participantID, calculate total score
    leaderboard_data = db.session.query(
        Participant.participantID,
        Participant.fname, 
        Participant.lname,
        func.sum(Enrol.score).label('total_score')
    ).join(
        Enrol, Participant.participantID == Enrol.participantID
    ).filter(
        Enrol.access_code == room_code
    ).group_by(
        Participant.participantID, Participant.fname
    ).order_by(
        func.sum(Enrol.score).desc()
    ).all()

    # Calculate rank based on total score
    rank = 1
    prev_score = None
    formatted_leaderboard_data = []
    for data in leaderboard_data:
        if prev_score is not None and data.total_score < prev_score:
            rank += 1
        formatted_leaderboard_data.append({
            'rank': rank,
            'fname': data.fname,
            'lname': data.lname,
            'total_score': data.total_score
        })
        prev_score = data.total_score

    return render_template('leaderboard.html', leaderboard_data=formatted_leaderboard_data)

@app.route('/get_students', methods=['GET'])
def get_students():
    pass

@app.route('/get_student', methods=['GET'])
def get_student(studentID):
    pass

@app.route('/get_quizzes', methods=['GET'])
def get_quizzes():
    pass

@app.route('/get_quizzes_contributed', methods=['GET'])
def get_quizzes_contributed():
    pass


###
# The functions below should be applicable to all Flask apps.
###

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    # Attempt to load a student
    student = db.session.query(Participant).filter_by(participantID=id).first()
    if student:
        return student
    
    # If no student found, attempt to load a teacher
    teacher = db.session.query(Administrator).filter_by(administratorID=id).first()
    if teacher:
        return teacher

    # If neither student nor teacher found, return None
    return None

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404