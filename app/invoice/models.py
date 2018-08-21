from enum import IntEnum
from app import db
from app.models import BaseAddressModel

class InvoiceStatus(IntEnum):
    pending = 0
    sent = 1

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_sender_details_id = db.Column(
        db.Integer, db.ForeignKey("invoice_sender_details.id"), nullable=False)
    product_order_id = db.Column(
        db.Integer, db.ForeignKey("product_order.id"), nullable=False, unique=True)
    cost_center_id = db.Column(
        db.Integer, db.ForeignKey("cost_center.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255), nullable=True)
    sent_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    paid_date = db.Column(db.DateTime, nullable=True)
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())
    paypal_address = db.Column(db.String(255), nullable=False)
    cost_center = db.relationship("CostCenter", lazy=True)
    invoice_sender = db.relationship("InvoiceSenderDetails", lazy=True)

    def is_sent(self):
        return self.status == InvoiceStatus.sent
    
    @staticmethod
    def create_invoice_from_product_order(product_order):
        from app.subcontractor.models import Subcontractor

        subcon = Subcontractor.query.filter_by(id=product_order.order.subcontractor_id).first()
        sender_details = InvoiceSenderDetails(subcon)

        db.session().add(sender_details)
        db.session().flush()

        invoice = Invoice()
        invoice.invoice_sender_details_id = sender_details.id
        invoice.cost_center_id = product_order.order.cost_center_id
        invoice.product_order_id = product_order.id
        invoice.amount = product_order.product.price
        invoice.status = InvoiceStatus.pending
        invoice.note = product_order.product.description
        invoice.paypal_address = "test@example.com"

        db.session().add(invoice)
        db.session().commit()

        return invoice


class InvoiceSenderDetails(BaseAddressModel):
    """
    Invoice sender details at the time when invoice is sent.
    """
    id = db.Column(db.Integer, primary_key=True)
    vat_code = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, subcontractor):
        self.company_name = subcontractor.company_name
        self.street = subcontractor.street
        self.city = subcontractor.city
        self.state = subcontractor.state
        self.country = subcontractor.country
        self.zip_code = subcontractor.zip_code
        self.vat_code = subcontractor.vat_code
