from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from app.auth.validators import UsernameValidator

USERNAME_VALIDATOR = validators.Length(min=4, max=25)
PASSWORD_VALIDATOR = validators.Length(min=8, max=255)

class LoginForm(FlaskForm):
    username = StringField("Username", [USERNAME_VALIDATOR])
    password = PasswordField("Password", [PASSWORD_VALIDATOR])

class RegistrationForm(FlaskForm):
    username = StringField("Username", [
        USERNAME_VALIDATOR,
        UsernameValidator(message="Username is already taken")])

    password = PasswordField('Password', [
        PASSWORD_VALIDATOR,
        validators.EqualTo('password_again', message="Passwords must match")
    ])

    password_again = PasswordField("Password Again")
