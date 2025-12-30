from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'tmd1603'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/managecf?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='dsjytfvdz',
    api_key='841864179767685',
    api_secret='HSKtnNsA6UtWZvlI-w24ef99UD4',
)

login = LoginManager(app=app)