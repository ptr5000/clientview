from enum import IntEnum
from app import db
from app import bcrypt

class Roles(IntEnum):
    DEFAULT = 0
    ADMIN = 1000

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=Roles.DEFAULT)

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = int(role)

class User(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=True)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)

    @staticmethod
    def create_user(username, password, role=Roles.DEFAULT):
        user = User(username, password)
        db.session().add(user)
        db.session().flush()

        db.session().add(Role(user.id, role))
        db.session().commit()

        return user

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
        return map(lambda r: r.role, Role.query.filter_by(user_id=self.id).all())
