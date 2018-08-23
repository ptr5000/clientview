from app import db
from app.invoice.models import Invoice
from sqlalchemy.sql import text

class Order(db.Model):
    __tablename__ = "orderinfo"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    subcontractor_id = db.Column(
        db.Integer, db.ForeignKey("subcontractor.id"), nullable=False)
    cost_center_id = db.Column(db.Integer,
                               db.ForeignKey("cost_center.id",
                                             onupdate="CASCADE",
                                             ondelete="CASCADE"),
                                nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    subcontractor = db.relationship("Subcontractor")
    cost_center = db.relationship("CostCenter")
    invoice = db.relationship(Invoice)

    def get_total_sum(self):
        stmt = text("SELECT SUM(product.price) "
                    "FROM product, product_order "
                        "WHERE product_order.order_id = :order_id "
                        "AND product_order.product_id = product.id").params(order_id=self.id)

        res = db.engine.execute(stmt)

        return res.fetchone()[0]

class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey("product.id",
                                         onupdate="CASCADE",
                                         ondelete="CASCADE"),
                           nullable=False)
    order_id = db.Column(db.Integer,
                         db.ForeignKey("orderinfo.id",
                                       onupdate="CASCADE",
                                       ondelete="CASCADE"),
                         nullable=False)
    product = db.relationship("Product", cascade="delete")
    order = db.relationship(Order)
