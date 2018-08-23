# pylint: disable=C0413,C0411
import os
from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientview.db"  
    app.config["SQLALCHEMY_ECHO"] = False

db = SQLAlchemy(app)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login_form"
login_manager.login_message = "Please login to use this functionality."

from app import views

from os import urandom
app.config["SECRET_KEY"] = "fsdJVdfjgdfR5454"

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

from app.auth.models import User, Roles
if db.session().query(User).count() == 0:
    User.create_user("admin", "1", Roles.ADMIN)
    User.create_user("testco", "1", Roles.DEFAULT)
    User.create_user("acme", "1", Roles.DEFAULT)
