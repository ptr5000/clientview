from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)
