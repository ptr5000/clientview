from app import db
from app.models import BaseAddressModel

class Subcontractor(BaseAddressModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), index=True, nullable=False)
    vat_code = db.Column(db.String(255), nullable=False)
    paypal_address = db.Column(db.String(255), nullable=False)