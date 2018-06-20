from db import db


class SaleModel(db.Model):
    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total = db.Column(db.Float(precision=2))
