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
    CREATE TABLE IF NOT EXISTS listings (
        listingid SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        num_bedrooms INTEGER NOT NULL,
        num_bathrooms INTEGER NOT NULL,
        location VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        price FLOAT NOT NULL,
        description TEXT NOT NULL,
        image_url VARCHAR(255) NOT NULL
    );
""")

conn.commit()

cur.close()
conn.close()
