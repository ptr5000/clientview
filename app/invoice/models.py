from app import db
from app.models import BaseAddressModel


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)
    invoice_sender_details_id = db.Column(
        db.Integer, db.ForeignKey("invoicesenderdetails.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    note = street = db.Column(db.String(255), nullable=True)
    sent_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    paid_date = db.Column(db.DateTime, nullable=True)
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())
    paypal_address = db.Column(db.String(255), nullable=False)


class InvoiceSenderDetails(BaseAddressModel):
    """
    Invoice sender details at the time when invoice is sent.
    """
    id = db.Column(db.Integer, primary_key=True)
    vat_code = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
