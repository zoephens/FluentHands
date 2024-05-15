import os, json
from app import app, db, login_manager
from flask import jsonify, Response, render_template, request, redirect, url_for, flash, session, abort, send_from_directory, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from flask import send_file
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image




from sqlalchemy.orm import joinedload
from sqlalchemy.sql import insert
from sqlalchemy import func

from app.models import quiz_camera_question, quiz_image_question, Participant, Administrator, CamQuestion, ImageQuestion, Quiz, Leaderboard, Administered, Enrol
from app.forms import LoginForm, SignUpForm, LessonPlan, EnrolForm

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
user_email = ''

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
        quizzes = fetch_prepared_quizzes(admin_id=current_user.administratorID)

        admin = Administrator.query.filter_by(administratorID=current_user.administratorID).first()
        room_code = admin.access_code
        is_admin = True
        id_num = current_user.administratorID
        return render_template('dashboard.html', quizzes=quizzes, fname=first_name, room_code=room_code, is_admin=is_admin, id_num=id_num)
    else:
        # If the current user is a participant
        participant = Participant.query.filter_by(participantID=current_user.participantID).first()
        enrol = Enrol.query.filter_by(participantID=current_user.participantID).first()
        room_code = enrol.access_code if enrol else None
        level = participant.level
        id_num = current_user.participantID
        is_admin = False

        admin = Administrator.query.filter_by(access_code=room_code).first()
        quizzes = fetch_prepared_quizzes(admin_id=admin.administratorID, difficulty=level)
        return render_template('dashboard.html', quizzes=quizzes, fname=first_name, room_code=room_code, is_admin=is_admin, level=level, id_num=id_num)

# --------------------- Validation and Authentication Endpoints ---------------------
@app.route('/signup', methods=['POST', 'GET'])
def register():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        fname = signup_form.fname.data
        lname = signup_form.lname.data
        email = signup_form.email.data            
        password = signup_form.password.data
        repeat_pass = signup_form.repeat_password.data
        account_type = signup_form.account_type.data

        if password != repeat_pass:
            # Find a way to flash fields red
            flash(f'Passwords Do not Match!', 'danger')
            return render_template("signup.html", form=signup_form)
        
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
                session['user_email'] = email

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
def enrol():
    form = EnrolForm()

    if form.validate_on_submit():
        code = form.room_code.data
        user_email = session.get('user_email') 

        try:
            user = db.session.query(Participant).filter_by(email=user_email).first()

            enrol = Enrol(
                accessCode = code,
                participantID = user.participantID
            )
            db.session.add(enrol)

            db.session.commit()
            login_user(user)

            flash('Enrolment Successful', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Invalid Code {e}', 'error')

    return render_template("roomcode.html", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        session['user_email'] = email

        # Query the database for the user
        user = db.session.query(Participant).filter_by(email=email).first()

        if user is None:
            user = db.session.query(Administrator).filter_by(email=email).first()

        if user is not None:
            print(email, password)
            if check_password_hash(user.password, password):

                # Check if Participant is enrolled
                if isinstance(user, Participant):
                    enrolment = db.session.query(Enrol).filter_by(participantID=user.participantID).first()
                    if not enrolment:
                        flash('No enrolment record found for participant.', 'danger')
                        return redirect(url_for('enrol'))
                    
                # Login successful, redirect to dashboard or other page
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        else:
            flash('User not found', 'danger')

    return render_template("login.html", form=form)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if current_user.is_authenticated:
        if isinstance(current_user, Administrator):
            user_id = current_user.administratorID
        else:
            user_id = current_user.participantID

        user = Administrator.query.get(user_id) if isinstance(current_user, Administrator) else Participant.query.get(user_id)

        if user:
            Enrol.query.filter_by(participantID=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            logout_user()
            return jsonify({'redirect': url_for('login')}), 200

    return jsonify({'error': 'Failed to delete your account. Please try again.'}), 400

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for("login"))
# -----------------------------------------------------------------------------------


# ------------------- Dashboard Endpoints For Students and Admins -------------------
# For an Admin there needs to be multiple leaderboards where they can see
# Students of all levels
@app.route('/leaderboard/<room_code>', methods=['GET'])
def leaderboard(room_code):
    leaderboard_data = db.session.query(
        Participant.participantID,
        Participant.fname, 
        Participant.lname,
        db.func.sum(Enrol.score).label('total_score')
    ).join(
        Enrol, Participant.participantID == Enrol.participantID
    ).filter(
        Enrol.access_code == room_code
    ).group_by(
        Participant.participantID
    ).order_by(
        db.func.sum(Enrol.score).desc()
    ).all()

    formatted_leaderboard_data = []
    for idx, data in enumerate(leaderboard_data):
        formatted_leaderboard_data.append({
            'rank': idx + 1,
            'participantID': data.participantID,
            'fname': data.fname,
            'lname': data.lname,
            'total_score': data.total_score,
            'quiz_count': 0  # Placeholder, will be updated later
        })

    return jsonify(formatted_leaderboard_data)

# --------- Progress Report ---------
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from flask import send_file
import os

# Function to generate the progress report PDF
def generate_progress_report(access_code, students_grades):
    # Create a new PDF file
    pdf_path = os.path.join(app.root_path, 'progress_report.pdf')  

    # Create canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Background image path
    background_path = os.path.join(app.root_path, 'pr-1.png')


    # Draw background design PNG onto the canvas
    c.drawImage(background_path, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=True)

    # Define table data
    table_data = [['Participant ID', 'First Name', 'Last Name', 'Score']]

    # Populate table data
    for participant_id, score, first_name, last_name in students_grades:
        table_data.append([participant_id, first_name, last_name, score])

    # Define column widths
    col_widths = [80, 100, 100, 50] 

    # Create table
    table = Table(table_data, colWidths=col_widths)

    # Table Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#657CD5')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
        ('GRID', (0, 0), (-1, -1), 2.5, colors.white) 
    ])

    table.setStyle(style)

    # Horizontal midpoint of canvas
    page_width = letter[0]  
    table_width = 400  
    midpoint = (page_width - table_width) / 2  


    # Position table on the canvas
    table.wrapOn(c, 400, 200)
    table.drawOn(c, midpoint + 25, 625) 

    # Save canvas
    c.save()

    # Return the PDF file path
    return pdf_path

# Route to get the progress report
@app.route('/get_progress_report/<access_code>', methods=['GET'])
def get_progress_report(access_code):
    # Join Enrol and Participants tables
    students_grades = db.session.query(
            Enrol.participantID, 
            Enrol.score, 
            Participant.fname,
            Participant.lname
        ).join(
            Participant
        ).filter(
            Enrol.access_code == access_code).all()

    # Generate the progress report PDF
    pdf_path = generate_progress_report(access_code, students_grades)

    # Return the PDF
    try:
        return send_file(pdf_path, as_attachment=True)
    except FileNotFoundError:
        return "PDF file not found", 404

@app.route('/get_students/<room_code>', methods=['GET'])
def get_students(room_code):
    # Join Participant and Enrol tables, group by participantID, calculate total score
    students = db.session.query(
        Participant.participantID,
        Participant.fname, 
        Participant.lname,
        Participant.email,
        Participant.level
    ).join(
        Enrol, Participant.participantID == Enrol.participantID
    ).filter(
        Enrol.access_code == room_code
    ).group_by(
        Participant.participantID
    ).order_by(Participant.lname).all() # Ordering by lastname

    students_data = []
    for data in students:
        students_data.append({
            'student_id': data.participantID,
            'first_name': data.fname,
            'last_name': data.lname,
            'email': data.email,
            'level': data.level
        })
    return jsonify(students_data)

@app.route('/get_quiz_count/<userID>', methods=['GET'])
def get_quiz_count(userID):
    # First, determine if the ID belongs to a Participant or an Administrator
    participant = db.session.query(Participant).filter_by(participantID=userID).first()
    if participant:
        # If the ID belongs to a Participant, count quizzes taken by the participant
        count = db.session.query(Administered).filter(Administered.participantID == userID).count()
        return jsonify({'participantID': userID, 'quiz_count': count, 'role': 'Participant'})
    else:
        # If not a Participant, check if it is an Administrator
        admin = db.session.query(Administrator).filter_by(administratorID=userID).first()
        if admin:
            # Count quizzes administered by the admin
            count = db.session.query(Quiz).filter(Quiz.adminID == userID).count()
            return jsonify({'adminID': userID, 'quiz_count': count, 'role': 'Administrator'})
        else:
            # If neither, return an error message
            return jsonify({'error': 'No valid Participant or Administrator found with the provided ID'}), 404

@app.route('/get_ques_contributed/<adminID>', methods=['GET'])
def get_ques_contributed(adminID):
    try:
        cam_count = CamQuestion.query.filter_by(adminID=adminID).count()
        image_count = ImageQuestion.query.filter_by(adminID=adminID).count()
        total_contributed = cam_count + image_count
    except Exception as e:
        # Log the error and return a 500 server error
        app.logger.error(f"Database error: {e}")
        abort(500, description="Database error")

    return jsonify({
        'adminID': adminID,
        'total_contributed': total_contributed,
        'details': {
            'cam_questions': cam_count,
            'image_questions': image_count
        }
    })

@app.route('/top_scorer/<room_code>', methods=['GET'])
def top_scorer(room_code):
    # Query to find the highest score and associated participantID
    top_score = db.session.query(
        Enrol.participantID,
        db.func.max(Enrol.score).label('max_score')
    ).filter(Enrol.access_code == room_code
    ).group_by(Enrol.participantID
    ).order_by(db.desc('max_score')).first()

    if top_score:
        # Query to get participant details
        participant = Participant.query.filter_by(participantID=top_score.participantID).first()
        if participant:
            return jsonify({
                'participantID': participant.participantID,
                'name': f"{participant.fname} {participant.lname}",
                'score': top_score.max_score
            })
    return jsonify({'error': 'No scores found'}), 404
# -----------------------------------------------------------------------------------


# ----------------------- Quiz Generation and Model Handling ------------------------
@app.route('/add_lesson', methods=['GET', 'POST'])
def add_lesson():
    lesson_form = LessonPlan()

    if request.method == 'GET':
        if isinstance(current_user, Administrator):
            admin = Administrator.query.filter_by(administratorID=current_user.administratorID).first()
            return render_template('lesson_plan.html', fname=admin.fname, room_code=admin.access_code, is_admin=True, id_num=admin.administratorID, lesson_form=lesson_form)
    
    elif request.method == 'POST':
        print(request.form)

        if lesson_form.validate_on_submit():
            adminID = current_user.administratorID

            # Create and save the quiz
            quiz = Quiz(
                topic=lesson_form.topic.data,
                numQuestions=lesson_form.num_questions.data,
                due_date=lesson_form.due_date.data,
                adminID=adminID
            )
            db.session.add(quiz)
            db.session.flush()  # To get the quiz ID

            questions_summary = []

            # Handling text (camera) questions
            for i in range(lesson_form.num_text_questions.data):
                question = request.form.get(f'text_questions-{i}-question') #('text_questions-0-question', 'How do you say hello in JSL?')
                difficulty = request.form.get(f'text_questions-{i}-difficulty') #('text_questions-0-difficulty', 'Beginner')
                marks = request.form.get(f'text_questions-{i}-marks') #('text_questions-0-marks', '1')
                answer = request.form.get(f'text_questions-{i}-answer') #('text_questions-0-answer', 'Hello')
                
                if question:
                    new_cam_question = CamQuestion(
                        topic=lesson_form.topic.data,
                        question=question,
                        level=difficulty,
                        marks=marks,
                        label=answer,
                        adminID=adminID
                    )

                    db.session.add(new_cam_question)
                    db.session.flush()

                    # Associate question with quiz
                    association = insert(quiz_camera_question).values(
                        quiz_id=quiz.quizID,
                        cam_question_id=new_cam_question.camQuestionID
                    )
                    db.session.execute(association)

                    questions_summary.append({
                        'type': 'text',
                        'question': question,
                        'level': difficulty,
                        'marks': marks,
                        'answer': answer
                    })

            # Handling image questions
            for i in range(lesson_form.num_image_questions.data):
                question = request.form.get(f'image_questions-{i}-question') #('image_questions-0-question', 'What JSL sign is this gesture showing?')
                difficulty = request.form.get(f'image_questions-{i}-difficulty') #('image_questions-0-difficulty', 'Beginner')
                marks = request.form.get(f'image_questions-{i}-marks') #('image_questions-0-marks', '1')
                answer = request.form.get(f'image_questions-{i}-answer') #('image_questions-0-answer', 'Hello')
                file_field = request.files.get(f'image_questions-{i}-photo') #'image_questions-0-photo'

                if file_field:
                    filename = secure_filename(file_field.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file_field.save(file_path)

                new_image_question = ImageQuestion(
                    topic= lesson_form.topic.data,
                    question=question,
                    level=difficulty,
                    marks=marks,
                    label=answer,
                    filename=filename if file_field else None,
                    adminID=adminID
                )

                db.session.add(new_image_question)
                db.session.flush()

                # Associate question with quiz
                association = insert(quiz_image_question).values(
                    quiz_id=quiz.quizID,
                    image_question_id=new_image_question.imgQuestionID
                )
                db.session.execute(association)

                questions_summary.append({
                    'type': 'image',
                    'question': question,
                    'level': difficulty,
                    'marks': marks,
                    'answer': answer,
                    'photo': filename if file_field else None
                })

            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Quiz Created Successfully',
                'questions': questions_summary,
                'redirect_url': url_for('add_lesson')
            })
        else:
            print("Form Errors:", lesson_form.errors)
    else:
        return jsonify({
            'success': False,
            'message': 'Form validation failed',
            'errors': lesson_form.errors
        }), 400

    return jsonify({'message': 'Invalid method or not logged in as administrator'}), 400

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
        
            # predictions = np.argmax(predictions, axis=1)  # if your model outputs one-hot encoded predictions
            # y_true = np.argmax(y_test, axis=1)            # if your labels are also one-hot encoded

            # # Calculate the accuracy
            # accuracy = accuracy_score(y_true, predictions)
            # print("Accuracy: {:.2f}%".format(accuracy * 100))

            # Once we have 10 predictions, find the most frequent one
            if len(all_predictions) == 20:
                most_common_prediction = Counter(all_predictions).most_common(1)[0][0]
                print("-------------------------Most frequent prediction after 10 attempts:", most_common_prediction)
                all_predictions = []  # Reset predictions for the next set
                
        return jsonify({'message': 'Keypoint Received', 'data': keypoints_data, 'predicted_label': most_common_prediction}), 200
    except Exception as e:
        print("Error processing keypoints:", e)
        return jsonify({'message': 'Error processing keypoints'}), 500

@app.route('/get_questions', methods=['GET'])
def get_questions():
    topic = request.args.get('topic', '')  # Get the topic from the query string
    difficulty = request.args.get('difficulty', '')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    # Query your database for questions related to the topic
    camera_questions = CamQuestion.query.filter_by(topic=topic, level=difficulty).all()
    image_questions = ImageQuestion.query.filter_by(topic=topic, level=difficulty).all()

    # Format the data to send back to the frontend
    questions = []
    for question in camera_questions + image_questions:
        questions.append({
            'id': question.imgQuestionID if isinstance(question, ImageQuestion) else question.camQuestionID,
            'topic': question.topic,
            'marks': question.marks,
            'answer': question.label,
            'text': question.question,
            'type': 'Camera' if isinstance(question, CamQuestion) else 'Image'
        })

    return jsonify(questions)

@app.route('/quiz')
@login_required
def takequiz():
    """Render website's quiz page."""
    if isinstance(current_user, Participant):
        # If the current user is an admin
        enrol = Enrol.query.filter_by(participantID=current_user.participantID).first()
        participant = Participant.query.filter_by(participantID=current_user.participantID).first()

        room_code = enrol.access_code
        is_admin = False
        id_num = current_user.participantID

    return render_template('quiz.html', fname=participant.fname, room_code=room_code, is_admin=is_admin, id_num=id_num, level=participant.level)

@app.route('/update_user_level', methods=['POST'])
def update_user_level():
    data = request.json
    user = current_user.participantID
    points = data.get('points')
    
    return jsonify({'user_id': user.user_id, 'new_level': user.level, 'points': user.points}), 200

# -----------------------------------------------------------------------------------


# --------------------------------------------------Functionality to implement

@app.route('/get_student/<participantID>', methods=['GET'])
def get_student(participantID):
    pass

@app.route('/get_quizzes', methods=['GET'])
def get_quizzes():
    pass


# Get quizzes for a specific administrator with ID 1
# quizzes_for_admin1 = fetch_prepared_quizzes(admin_id=1)

# Get quizzes that include 'Algebra' in their topic
# algebra_quizzes = fetch_prepared_quizzes(topic='Algebra')

# Get quizzes that are of 'Intermediate' difficulty
# intermediate_quizzes = fetch_prepared_quizzes(difficulty='Intermediate')
def fetch_prepared_quizzes(admin_id=None, topic=None, difficulty=None, quiz_id=None):
    # Start with a base query
    query = Quiz.query.options(
        joinedload(Quiz.camera_questions),
        joinedload(Quiz.image_questions)
    )
    
    print(quiz_id)
    # Apply filters based on the presence of optional parameters
    if admin_id:
        query = query.filter(Quiz.adminID == admin_id)
    if topic:
        query = query.filter(Quiz.topic.ilike(f'%{topic}%'))  # Use ilike for case-insensitive matching
    if difficulty:
        query = query.join(Quiz.camera_questions).filter(CamQuestion.level.ilike(f'%{difficulty}%'))
        query = query.join(Quiz.image_questions).filter(ImageQuestion.level.ilike(f'%{difficulty}%'))
    if quiz_id:
        query = query.filter(Quiz.quizID == quiz_id)

    # Fetch all quizzes matching the filters
    quizzes = query.all()

    quizzes_data = []
    for quiz in quizzes:
        total_marks = sum(q.marks for q in quiz.camera_questions) + sum(q.marks for q in quiz.image_questions)
        quiz_data = {
            'quiz_id': quiz.quizID,
            'topic': quiz.topic,
            'total_marks': total_marks,
            'level': quiz.level,
            'due_date': quiz.due_date if quiz.due_date else None,
            'created_date': quiz.date,
            'camera_questions': [{
                'question_id': q.camQuestionID,
                'text': q.question,
                'marks': q.marks,
                'type': 'Camera'
            } for q in quiz.camera_questions],
            'image_questions': [{
                'question_id': q.imgQuestionID,
                'text': q.question,
                'marks': q.marks,
                'image_url': q.filename,
                'type': 'Image'
            } for q in quiz.image_questions]
        }
        quizzes_data.append(quiz_data)
        print(quiz_data)
    return quizzes_data

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_quiz/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    # Fetch the quiz with preloaded questions from both question banks
    quizzes = fetch_prepared_quizzes(quiz_id=quiz_id)

    if not quizzes:
        abort(404, description="Quiz not found")  # Send a 404 if not found

    # Assuming questions are loaded correctly in the quiz object
    # questions = [{
    #     'question_id': q.id,
    #     'text': q.text,
    #     'options': q.options,  # Assuming multiple choice for simplicity
    #     'answer': q.answer
    # } for q in quiz.questions]

    participant = Participant.query.filter_by(participantID=current_user.participantID).first()
    enrol = Enrol.query.filter_by(participantID=current_user.participantID).first()
    room_code = enrol.access_code if enrol else None
    level = participant.level
    id_num = current_user.participantID
    is_admin = False

    return render_template('quiz.html', quizzes=quizzes, fname=participant.fname, room_code=room_code, is_admin=is_admin, level=level, id_num=id_num)



# @app.route('/create_quiz', methods=['GET', 'POST'])
# def create_quizzes():
#     form = LessonPlan()
#     if form.validate_on_submit():
#         topic = form.topic.data
#         num_questions = form.num_questions.data

#         choose_from_bank = form.choose_from_bank.data #checkbox boolean
#         use_custom_questions = form.use_custom_questions.data #checkbox boolean

#         if(choose_from_bank):
#             pass
#         if(use_custom_questions):
#             pass

#         if(choose_from_bank == 'False' & use_custom_questions == False)
        # default option is randomly selecting questions based on number and topic

# Dummy random question list generator
def select_random_questions(topic, num_questions):
    # This function will fetch half from each type of question bank
    num_each_type = num_questions // 2

    cam_questions = CamQuestion.query.filter_by(topic=topic).order_by(func.random()).limit(num_each_type).all()
    img_questions = ImageQuestion.query.filter_by(topic=topic).order_by(func.random()).limit(num_each_type).all()

    question_ids = [q.id for q in cam_questions + img_questions]
    return question_ids

# -------------------------- General Flask App Functions ----------------------------
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