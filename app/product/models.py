from app import db
from sqlalchemy.sql import text

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    def get_all_suppliers(self):
        stmt = text("SELECT subcontractor.id, "
                            "subcontractor.company_name, "
                            "SUM(product.price) "
                                    "FROM product_order, orderinfo, product, subcontractor "
                                    "WHERE product_order.product_id = :product_id AND "
                                        "product_order.order_id = orderinfo.id AND "
                                        "product.id = product_order.product_id AND "
                                        "subcontractor.id = orderinfo.subcontractor_id "
                                        "GROUP BY subcontractor.id").params(product_id=self.id)

        res = db.engine.execute(stmt)

        return map(lambda row: {"id": row[0], "company_name": row[1], "total": row[2]}, res)
