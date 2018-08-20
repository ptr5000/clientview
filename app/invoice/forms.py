from flask_wtf import FlaskForm
from wtforms import SelectField, validators
from app.invoice.models import Invoice

class OrderIterable(object):
    def __iter__(self):
        invoices = Invoice.query.all()
        return map(lambda s: (s.id, "{} ({}€)"
                              .format(s.description, s.price)), invoices)

class InvoiceForm(FlaskForm):
    orders = SelectField("Order", coerce=int, choices=OrderIterable())
