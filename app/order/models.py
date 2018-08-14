from app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)

class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False)
    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id"), nullable=False)
