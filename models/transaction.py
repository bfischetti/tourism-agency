from db import db
from datetime import datetime
from models.sale import SaleModel
from models.category import CategoryModel
from models.currency import CurrencyModel


class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float(precision=2))
    exchange = db.Column(db.Float(precision=2))
    method = db.Column(db.String(20))
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now())
    is_expense = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean, default=False)

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.currency_id'), nullable=True)
    currency = db.relationship('CurrencyModel')

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship('CategoryModel')

    sale_id = db.Column(db.Integer, db.ForeignKey('sale.sale_id'), nullable=True)
    sale = db.relationship('SaleModel')

    def __init__(self, transaction_id, amount, description, date, is_expense, category_id, method, sale_id=None,
                 exchange=None, currency_id=None, deleted=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.description = description
        self.method = method
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            self.date = formatted_date
        self.is_expense = is_expense
        self.category_id = category_id
        self.sale_id = sale_id
        if exchange is not None:
            self.exchange = exchange
        if currency_id is not None:
            self.currency_id = currency_id
        if deleted is not None:
            self.deleted = deleted

    @classmethod
    def filter_by_deleted(cls, deleted):
        return cls.query.filter_by(deleted=deleted).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(transaction_id=_id).first()

    @classmethod
    def find_by_sale_id(cls, sale_id):
        return cls.query.filter_by(sale_id=sale_id).all()

    def update_to_db(self):
        transaction_to_update = TransactionModel.find_by_id(self.transaction_id)
        if self.category_id is not None:
            transaction_to_update.category_id = self.category_id
        if self.amount is not None:
            transaction_to_update.amount = self.amount
        if self.description is not None:
            transaction_to_update.description = self.description
        if self.date is not None:
            formatted_date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
            transaction_to_update.date = formatted_date
        if self.is_expense is not None:
            transaction_to_update.is_expense = self.is_expense
        if self.category_id is not None:
            transaction_to_update.category_id = self.category_id
        if self.method is not None:
            transaction_to_update.method = self.method

        transaction_to_update.save_to_db()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(TransactionModel.date.desc()).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls, transaction_id):
        transaction_to_delete = cls.find_by_id(transaction_id)
        transaction_to_delete.deleted = True
        transaction_to_delete.save_to_db()

    def json(self):
        return {'transaction_id': self.transaction_id,
                'amount': self.amount,
                'description': self.description,
                'currency_id': self.currency_id,
                'method': self.method,
                'date': str(self.date)[:19],
                'category_id': self.category_id,
                'is_expense': self.is_expense,
                'exchange': self.exchange,
                'sale_id': self.sale_id,
                'deleted': self.deleted}
