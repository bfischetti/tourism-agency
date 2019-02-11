from db import db
from datetime import datetime
from models.client import ClientModel
from models.user import UserModel
from models.promoter import PromoterModel


class SaleModel(db.Model):
    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total = db.Column(db.Float(precision=2))
    discount = db.Column(db.Float(precision=2))
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    client = db.relationship('ClientModel')
    date = db.Column(db.DateTime, default=datetime.now())
    promoter_commission = db.Column(db.Float(precision=2))
    user_commission = db.Column(db.Float(precision=2))

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('UserModel', foreign_keys=[user_id])

    promoter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    promoter = db.relationship('UserModel', foreign_keys=[promoter_id])

    def __init__(self, total, user_id, date, sale_id, client_id, promoter_id, promoter_commission, user_commission,
                 discount):
        self.total = total
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            self.date = formatted_date
        self.user_id = user_id
        self.sale_id = sale_id
        self.client_id = client_id
        self.promoter_id = promoter_id
        self.promoter_commission = promoter_commission
        self.user_commission = user_commission
        self.discount = discount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(sale_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(SaleModel.date.desc()).all()

    def json(self):
        response = {'sale_id': self.sale_id,
                    'total': self.total,
                    'discount': self.discount,
                    'client': self.client.json(),
                    'seller': self.user.json(),
                    'promoter_commission': self.promoter_commission,
                    'user_commission': self.user_commission,
                    'date': str(self.date)[:19]}
        if self.promoter:
            response["promoter"] = self.promoter.json()

        return response
