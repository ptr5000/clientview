from app import db


class BaseAddressModel(db.Model):
    __abstract__ = True
    company_name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)
