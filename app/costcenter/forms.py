from wtforms import validators
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from app.costcenter.models import CostCenter
from app.models import ADDRESS_FIELD_ARGS

FIELD_ARGS = {
    'vat_code' : {
        'validators' : [validators.Length(min=6, max=10)]
    }
}

CostCenterForm = model_form(CostCenter,
                            FlaskForm,
                            field_args=dict(FIELD_ARGS, **ADDRESS_FIELD_ARGS))
