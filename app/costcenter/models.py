from app import db
from app.models import BaseAddressModel


class CostCenter(BaseAddressModel):
    id = db.Column(db.Integer, primary_key=True)
    vat_code = db.Column(db.String(255), nullable=False)
