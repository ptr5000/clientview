from wtforms import ValidationError
from app.auth.models import User

class UsernameValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError(self.message)
