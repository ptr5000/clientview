from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from app.auth.validators import UsernameTakenValidator, USERNAME_VALIDATOR, PASSWORD_VALIDATOR

class LoginForm(FlaskForm):
    username = StringField("Username", [USERNAME_VALIDATOR])
    password = PasswordField("Password", [PASSWORD_VALIDATOR])

class RegistrationForm(FlaskForm):
    username = StringField("Username", [
        USERNAME_VALIDATOR,
        UsernameTakenValidator(message="Username is already taken")])

    password = PasswordField('Password', [
        PASSWORD_VALIDATOR,
        validators.EqualTo('password_again', message="Passwords must match")
    ])

    password_again = PasswordField("Password Again")
