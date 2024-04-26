# import os
from app import app, db, login_manager
from flask import Response, render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Student, Teacher
from app.forms import LoginForm

from .camera import generate_frames
from flask_socketio import SocketIO

###
# Routing for your application.
###

@app.route('/')
@login_required
def home():
    """Render website's dashboard page."""
    return render_template('dashboard.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        student = db.session.query(Student).filter_by(email=email).first()
        if student is not None and student.check_password_hash(student.password, password):
            # Login successful, redirect to dashboard or other page
            login_user(student)
            flash('Login Successful', 'success')

            return redirect(url_for('home'))
        else:
            # If student not found, check teacher table
            teacher = db.session.query(Teacher).filter_by(email=email).first()
            if teacher is not None and teacher.check_password_hash(teacher.password, password):
                # Login successful, redirect to teacher dashboard or other page
                login_user(teacher)
                flash('Login Successful', 'success')

                return redirect(url_for('teacher_dashboard'))

        # If no user or teacher found, show error message
        flash('Invalid email or password', 'error')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('home'))

# Model Related Routes
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/keypoints', methods=['POST'])
def keypoints():
    # Process the keypoints data received from the frontend
    keypoints_data = request.json
    # Process the data as needed
    print(keypoints_data)
    return '', 200

@app.route('/quiz')
def takequiz():
    """Render website's quiz page."""
    return render_template('quiz.html')

# ------------------------------------ socket handeling

@socketio.on('connect')
def handle_connect():
    print('Client connected')


###
# The functions below should be applicable to all Flask apps.
###

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(email):
    # Attempt to load a student
    student = db.session.query(Student).filter_by(email=email).first()
    if student:
        return student
    
    # If no student found, attempt to load a teacher
    teacher = db.session.query(Teacher).filter_by(email=email).first()
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