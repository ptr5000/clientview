from app import db
from wtforms import validators


class BaseAddressModel(db.Model):
    __abstract__ = True
    company_name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)


ADDRESS_FIELD_ARGS = {
    'company_name' : {
        'validators' : [validators.Length(min=3, max=255)]
    },
    'street' : {
        'validators' : [validators.Length(min=3, max=255)]
    },
    'city' : {
        'validators' : [validators.Length(min=1, max=255)]
    },
    'state' : {
        'validators' : [validators.Length(min=0, max=255)]
    },
    'country' : {
        'validators' : [validators.Length(min=2, max=255)]
    },
    'zip_code' : {
        'validators' : [validators.Length(min=4, max=255)]
    }
}