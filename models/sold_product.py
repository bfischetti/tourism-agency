from db import db
from models.product import ProductModel
from models.sale import SaleModel

class SoldProductModel(db.Model):
    __tablename__ = 'sold_product'

    sold_product_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(precision=2))

    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    product = db.relationship('ProductModel')

    sale_id = db.Column(db.Integer, db.ForeignKey('sale.sale_id'))
    sale = db.relationship('SaleModel')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'sold_product_id': self.sold_product_id,
                'price': self.price,
                'product': self.product,
                'sale': self.sale }


