from db import db
from datetime import datetime
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

    date = db.Column(db.DateTime, default=datetime.now())
    transfer = db.Column(db.Boolean, default=False)
    payment_pending = db.Column(db.Boolean, default=True)

    adults = db.Column(db.Integer)
    children = db.Column(db.Integer)
    babies = db.Column(db.Integer)

    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, price, product_id, date, transfer, sale_id, adults, children, babies, payment_pending,
                 deleted=None):
        self.price = price
        self.product_id = product_id
        self.transfer = transfer
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            self.date = formatted_date
        self.sale_id = sale_id
        self.adults = adults
        self.children = children
        self.babies = babies
        self.payment_pending = payment_pending
        if deleted:
            self.deleted = deleted

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls, sold_product_id):
        sold_product_to_delete = cls.find_by_id(sold_product_id)
        sold_product_to_delete.deleted = True
        sold_product_to_delete.save_to_db()

    def update_to_db(self):
        sold_product_to_update = SoldProductModel.find_by_id(self.sold_product_id)
        if self.payment_pending is not None:
            sold_product_to_update.payment_pending = self.payment_pending

        sold_product_to_update.save_to_db()

    @classmethod
    def find_by_sale_id(cls, sale_id):
        return cls.query.filter_by(sale_id=sale_id).all()

    @classmethod
    def find_by_id(cls, product_id):
        return cls.query.filter_by(sold_product_id=product_id).first()

    @classmethod
    def get_unpaid(cls):
        return cls.query.filter_by(payment_pending=True)

    def json(self):
        return {'sold_product_id': self.sold_product_id,
                'price': self.price,
                'date': str(self.date)[:19],
                'transfer': self.transfer,
                'product': self.product.json(),
                'adults': self.adults,
                'children': self.children,
                'babies': self.babies,
                'sale_id': self.sale_id,
                'payment_pending': self.payment_pending,
                'deleted': self.deleted}
