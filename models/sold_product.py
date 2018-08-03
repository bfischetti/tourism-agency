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

    adults = db.Column(db.Integer)
    children = db.Column(db.Integer)
    babies = db.Column(db.Integer)

    def __init__(self, price, product_id, sale_id, adults, children, babies):
        self.price = price
        self.product_id = product_id
        self.sale_id = sale_id
        self.adults = adults
        self.children = children
        self.babies = babies

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_sale_id(cls, sale_id):
        return cls.query.filter_by(sale_id=sale_id).all()

    def json(self):
        return {'sold_product_id': self.sold_product_id,
                'price': self.price,
                'product': self.product.json(),
                'adults': self.adults,
                'children': self.children,
                'babies': self.babies,
                'sale_id': self.sale_id}
