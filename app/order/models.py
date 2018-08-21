from app import db
from app.invoice.models import Invoice

class Order(db.Model):
    __tablename__ = "orderinfo"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)
    cost_center_id = db.Column(
        db.Integer, db.ForeignKey("cost_center.id"), nullable=False)
    subcontractor = db.relationship("Subcontractor")
    cost_center = db.relationship("CostCenter")
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orderinfo.id"), nullable=False)
    product = db.relationship("Product")
    order = db.relationship(Order)
    invoice = db.relationship(Invoice)
