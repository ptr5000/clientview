from app import db
from app.models import BaseAddressModel

class Subcontractor(BaseAddressModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), index=True, nullable=False)
    vat_code = db.Column(db.String(255), nullable=False)
    is_freelancer = db.Column(db.Boolean(), nullable=True, default=False)

class Freelancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.String(255), nullable=False)
    