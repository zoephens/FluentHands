from flask import Flask
import psycopg2
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate =   Migrate(app,db)


from app import views

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database="PropertiesDB",
    user=os.environ.get('DATABASE_USERNAME', 'postgres'),
    password= os.environ.get('DATABASE_PASSWORD')
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS User (
        userID SERIAL PRIMARY KEY,
        fname VARCHAR(255) NOT NULL,
        lname VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        pw VARCHAR(255) NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Student (
        studentID SERIAL PRIMARY KEY,
        level INTEGER NOT NULL,
        score INTEGER NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Lecturer (
        teacherID SERIAL PRIMARY KEY,
        accessCOODE SERIAL PRIMARY KEY,
    );
""")

conn.commit()

cur.close()
conn.close()
