from flask_wtf import FlaskForm
from wtforms import SelectField, validators
from app.subcontractor.models import Subcontractor
from app.product.models import Product

class SubcontractorIterable(object):
    def __iter__(self):
        subcons = Subcontractor.query.all()
        return map(lambda s: (s.id, s.company_name), subcons)

class ProductIterable(object):
    def __iter__(self):
        products = Product.query.all()
        return map(lambda s: (s.id, "{} ({}€)"
                              .format(s.description, s.price)), products)

class OrderForm(FlaskForm):
    subcontractor = SelectField("Subcontractor", coerce=int, choices=SubcontractorIterable())
    product = SelectField("Product", coerce=int, choices=ProductIterable())

