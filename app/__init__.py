# pylint: disable=C0413,C0411
from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientview.db"
app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

from app import views

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from app.auth.models import User
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)

db.create_all()
