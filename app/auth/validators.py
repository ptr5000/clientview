from wtforms import ValidationError, validators
from app.auth.models import User

USERNAME_VALIDATOR = validators.Length(min=4, max=25)
PASSWORD_VALIDATOR = validators.Length(min=1, max=255)

class UsernameTakenValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError(self.message)
