from functools import wraps
from flask_login import current_user
from app import login_manager
from app.auth.models import Roles

def login_required(role=Roles.DEFAULT):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return login_manager.unauthorized()

            unauthorized = False

            if role != Roles.DEFAULT:
                unauthorized = True
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper