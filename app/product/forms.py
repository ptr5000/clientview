from wtforms import validators
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from app.product.models import Product

FIELD_ARGS = {
    'description' : {
        'validators' : [validators.Length(min=1, max=255)]
    },
    'price' : {
        'validators' : [validators.DataRequired()]
    }
}

ProductForm = model_form(Product,
                         FlaskForm,
                         field_args=FIELD_ARGS)
                        
