import os
from app import app, db, login_manager
from flask import jsonify, Response, render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Participant, Administrator
from app.forms import LoginForm, SignUpForm

# Realtime Tracking
from tensorflow.keras.models import load_model # type: ignore
# from .camera import generate_frames
import numpy as np

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'action.h5')

# Load the model
model = load_model(model_path)
actions = ['A', 'J', 'Z']

###
# Routing for your application.
###

@app.route('/')
@login_required
def dashboard():
    """Render website's dashboard page."""
    return render_template('dashboard.html')

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
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration Failed: {str(e)}', 'error')
    return render_template("signup.html", form=signup_form)
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        # Query the database for the user
        user = db.session.query(Participant).filter_by(email=email).first()

        if user is not None:
            if check_password_hash(user.password, password):
                # Login successful, redirect to dashboard or other page
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                print("Incorrect password")
                flash('Invalid email or password', 'error')
        else:
            print("User not found")
            flash('User not found', 'error')

    return render_template("login.html", login_form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('dashboard'))

# Model Related Routes
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/keypoints', methods=['POST'])
def keypoints():
    try:
        keypoints_data = request.json
        sequence = keypoints_data

        if len(sequence) == 30:
            prediction = model.predict(np.expand_dims(sequence, axis=0))[0]
            action = actions[np.argmax(prediction)]
            print(action)

        # sequence = sequence[-30:]

        # if len(sequence) == 30:
            # res = model.predict(np.expand_dims(sequence, axis=0))[0]
            # action = actions[np.argmax(res)]
            # print("Predicted action:", actions)
        
        return jsonify({'message': 'Keypoint Received', 'data': keypoints_data}), 200
    except Exception as e:
        print("Error processing keypoints:", e)
        return jsonify({'message': 'Error processing keypoints'}), 500

@app.route('/quiz')
def takequiz():
    """Render website's quiz page."""
    return render_template('quiz.html')

###
# The functions below should be applicable to all Flask apps.
###

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    # Attempt to load a student
    student = db.session.query(Participant).filter_by(participant_id=id).first()
    if student:
        return student
    
    # If no student found, attempt to load a teacher
    teacher = db.session.query(Administrator).filter_by(participant_id=id).first()
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