from app import db
from sqlalchemy.sql import text

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    def get_all_suppliers(self):
        stmt = text("SELECT id, company_name FROM subcontractor")
        res = db.engine.execute(stmt)
        
        return map(lambda row: {"id": row[0], "company_name": row[1]}, res)
