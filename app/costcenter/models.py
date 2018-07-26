from app import db


class CostCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)
    vat_code = db.Column(db.String(255), nullable=False)
