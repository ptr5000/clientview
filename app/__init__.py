# pylint: disable=C0413
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientview.db"
app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

from app import views

db.create_all()
