from db import db
from datetime import datetime


class SaleModel(db.Model):
    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total = db.Column(db.Float(precision=2))
    billable = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('UserModel')
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, total, billable, user_id, date, sale_id):
        self.total = total
        self.billable = billable
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            self.date = formatted_date
        self.user_id = user_id
        self.sale_id = sale_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(sale_id=_id).first()

    def json(self):
        return {'sale_id': self.sale_id,
                'total': self.total,
                'billable': self.billable,
                'user_id': self.user_id}
