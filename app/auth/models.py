from enum import Enum
from app import db
from app import bcrypt

class Roles(Enum):
    DEFAULT = 0
    ADMIN = 1000

class User(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=True)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password, 8)


    def validate_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def get_id(self):
        return self.id


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def is_authenticated(self):
        return True


    def is_admin(self):
        return Roles.ADMIN in self.roles()
    

    def roles(self):
        return [Roles.ADMIN]
