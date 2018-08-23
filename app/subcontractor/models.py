from app import db
from app.models import BaseAddressModel
from sqlalchemy.sql import text

class Subcontractor(BaseAddressModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), index=True, nullable=False)
    vat_code = db.Column(db.String(255), nullable=False)
    paypal_address = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_details(id):
        stmt = text("SELECT subcontractor.company_name, subcontractor.street, "
                            "subcontractor.city, subcontractor.state, "
                            "subcontractor.country, subcontractor.zip_code, "
                            "account.username, SUM(invoice.amount) "
                    "FROM subcontractor, invoice, account "
                    "WHERE subcontractor.id=:subcontractor_id "
                        "AND invoice.subcontractor_id=subcontractor.id "
                        "AND account.id = subcontractor.user_id").params(subcontractor_id=id)

        res = db.engine.execute(stmt)
        row = res.fetchone()

        return {"company_name": row[0], 
                "street": row[1],
                "city": row[2],
                "state": row[3],
                "country": row[4],
                "zip_code": row[5],
                "username": row[6],
                "total_invoiced_amount": row[7]}
