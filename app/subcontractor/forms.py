from wtforms import validators
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from app.models import ADDRESS_FIELD_ARGS
from app.subcontractor.models import Subcontractor

FIELD_ARGS = {
    'vat_code' : {
        'validators' : [validators.Length(min=4, max=10)]
    }
}

SubcontractorForm = model_form(Subcontractor, 
                               FlaskForm, 
                               field_args=dict(FIELD_ARGS, **ADDRESS_FIELD_ARGS))
