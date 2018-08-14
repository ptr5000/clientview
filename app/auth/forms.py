from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from app.auth.validators import UsernameValidator

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class RegistrationForm(FlaskForm):
    username = StringField("Username", [
        validators.Length(min=4, max=25),
        UsernameValidator(message="Username is already taken")])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password_again', message="Passwords must match")
    ])

    password_again = PasswordField("Password Again")
