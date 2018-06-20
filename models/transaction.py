from db import db
from models.sale import SaleModel


class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    description = db.Column(db.String(200))

    sale_id = db.Column(db.Integer, db.ForeignKey('sale.sale_id'), nullable=True)
    sale = db.relationship('SaleModel')

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(operation_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'transaction_id': self.transaction_id,
                'name': self.name,
                'price': self.price,
                'description': self.description,
                'sale': self.sale}
