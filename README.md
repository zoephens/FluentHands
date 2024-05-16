![FluentHands Logo](https://i.ibb.co/VSR5ZHz/fh-blue-logo.png)

## 🫂Team Members
- Zoe Stephens
- Tiffany Parkinson
- Nicholas Smith
- Aybarinee Campbell-Mendez 

## 🤟About the Project
The primary focus of this project is to enable educators to define learning outcomes for quizzes administered to their students. The system must accurately identify various Jamaican Sign Language (JSL) signs from images and gestures performed by students to assist educators in evaluating performance and providing real-time feedback. As well as the system must organize each student's performance data in a constructive manner for teachers to easily overview and make informed inferences about student progress. 

## 🏃‍♀️How to Run
**Please Note:** `Python 3.8.10` is the virtual environment that is supported for this project

```sh
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
```

**PostgreSQL Database Setup**
1. Install PostgreSQL: [PostgreSQL](https://www.postgresql.org/)
2. Sign up and create database with the following specifications:

```sql
CREATE DATABASE "fluenthands";
CREATE USER "fluent_user";
\password "password123";
ALTER DATABASE "fluenthands" OWNER TO "fluent_user"
```

**You then need to upgrade the database**
```sh
$flask db upgrade
```

**Now you can run the server!**
```sh
$flask --app app --debug run
```

## 🩷Credited Resources
- Nicholas Renotte: https://www.youtube.com/watch?v=doDUihpj6ro
- Github: https://github.com/nicknochnack/ActionDetectionforSignLanguage/tree/main

## 💻Tech Stack Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)  ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) ![Canva](https://img.shields.io/badge/Canva-%2300C4CC.svg?style=for-the-badge&logo=Canva&logoColor=white)

