from db import db
from models.provider import ProviderModel


class ProductModel(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    stock_price_adult = db.Column(db.Float(precision=2))
    stock_price_child = db.Column(db.Float(precision=2))
    stock_price_baby = db.Column(db.Float(precision=2))
    selling_price_adult = db.Column(db.Float(precision=2))
    selling_price_child = db.Column(db.Float(precision=2))
    selling_price_baby = db.Column(db.Float(precision=2))
    description = db.Column(db.String(200))
    billable = db.Column(db.Boolean, default=False)

    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'))
    provider = db.relationship('ProviderModel')

    def __init__(self, product_id, billable, name, stock_price_adult, selling_price_adult, stock_price_child,
                 selling_price_child, stock_price_baby, selling_price_baby, description, provider_id):
        self.product_id = product_id
        self.billable = billable
        self.name = name
        self.stock_price_adult = stock_price_adult
        self.selling_price_adult = selling_price_adult
        self.stock_price_child = stock_price_child
        self.selling_price_child = selling_price_child
        self.stock_price_baby = stock_price_baby
        self.selling_price_baby = selling_price_baby
        self.description = description
        self.provider_id = provider_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(product_id=_id).first()

    def update_to_db(self):
        product_to_update = ProductModel.find_by_id(self.product_id)
        if self.name is not None:
            product_to_update.name = self.name
        if self.stock_price_adult is not None:
            product_to_update.stock_price_adult = self.stock_price_adult
        if self.selling_price_adult is not None:
            product_to_update.selling_price_adult = self.selling_price_adult
        if self.stock_price_child is not None:
            product_to_update.stock_price_child = self.stock_price_child
        if self.selling_price_child is not None:
            product_to_update.selling_price_child = self.selling_price_child
        if self.stock_price_baby is not None:
            product_to_update.stock_price_baby = self.stock_price_baby
        if self.selling_price_baby is not None:
            product_to_update.selling_price_baby = self.selling_price_baby
        if self.description is not None:
            product_to_update.description = self.description
        if self.provider_id is not None:
            product_to_update.provider_id = self.provider_id

        product_to_update.save_to_db()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(ProductModel.name).all()

    @classmethod
    def find_by_provider(cls, provider_id):
        return cls.query.filter_by(provider_id=provider_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'product_id': self.product_id,
                'name': self.name,
                'stock_price_adult': self.stock_price_adult,
                'stock_price_child': self.stock_price_child,
                'stock_price_baby': self.stock_price_baby,
                'selling_price_adult': self.selling_price_adult,
                'selling_price_child': self.selling_price_child,
                'selling_price_baby': self.selling_price_baby,
                'description': self.description,
                'provider': self.provider.json()}
