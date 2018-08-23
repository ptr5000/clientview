from enum import IntEnum
from app import db
from app.models import BaseAddressModel

class InvoiceStatus(IntEnum):
    pending = 0
    sent = 1


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("invoice_sender.id"), nullable=False)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orderinfo.id"), nullable=False, unique=True)
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
    sender = db.relationship("InvoiceSender", lazy=True)


    def is_sent(self):
        return self.status == InvoiceStatus.sent


    def send(self):
        self.status = int(InvoiceStatus.sent)
        db.session().commit()


    @staticmethod
    def create_invoice(order):
        from app.subcontractor.models import Subcontractor
        
        subcon = Subcontractor.query.filter_by(id=order.subcontractor_id).first()
        sender_details = InvoiceSender(subcon)

        db.session().add(sender_details)
        db.session().flush()

        invoice = Invoice()
        invoice.sender_id = sender_details.id
        invoice.subcontractor_id = subcon.id
        invoice.cost_center_id = order.cost_center_id
        invoice.order_id = order.id
        invoice.amount = order.get_total_sum()
        invoice.status = int(InvoiceStatus.pending)
        invoice.paypal_address = subcon.paypal_address

        db.session().add(invoice)
        db.session().commit()

        return invoice


class InvoiceSender(BaseAddressModel):
    """
    Invoice sender details at the time when invoice was sent.
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
