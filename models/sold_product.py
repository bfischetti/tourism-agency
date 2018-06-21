from db import db
from models.product import ProductModel
from models.sale import SaleModel


class SoldProductModel(db.Model):
    __tablename__ = 'sold_product'

    sold_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float(precision=2))

    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    product = db.relationship('ProductModel')

    sale_id = db.Column(db.Integer, db.ForeignKey('sale.sale_id'))
    sale = db.relationship('SaleModel')

    def __init__(self, price, product_id, sale_id):
        self.price = price
        self.product_id = product_id
        self.sale_id = sale_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'sold_product_id': self.sold_product_id,
                'price': self.price,
                'product_id': self.product_id,
                'sale_id': self.sale_id}
