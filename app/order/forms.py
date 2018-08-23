from flask_wtf import FlaskForm
from wtforms import SelectField, validators
from app.subcontractor.models import Subcontractor
from app.product.models import Product
from app.costcenter.models import CostCenter

class SubcontractorIterable(object):
    def __iter__(self):
        subcons = Subcontractor.query.all()
        return map(lambda s: (s.id, s.company_name), subcons)

class ProductIterable(object):
    def __iter__(self):
        products = Product.query.all()

        product_list = [(-1, "--")]
        product_list.extend(map(lambda s: (s.id, "{} ({}€)"
                                           .format(s.description, s.price)), products))

        return iter(product_list)

class CostCenterIterable(object):
    def __iter__(self):
        cost_centers = CostCenter.query.all()
        return map(lambda s: (s.id, s.company_name), cost_centers)

class OrderForm(FlaskForm):
    cost_center = SelectField("Cost center", coerce=int, choices=CostCenterIterable())
    subcontractor = SelectField("Subcontractor", coerce=int, choices=SubcontractorIterable())
    product1 = SelectField("Product", coerce=int, choices=ProductIterable())
    product2 = SelectField("Product", coerce=int, choices=ProductIterable())
    product3 = SelectField("Product", coerce=int, choices=ProductIterable())
