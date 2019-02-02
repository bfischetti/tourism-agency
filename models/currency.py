from db import db
from datetime import datetime


class CurrencyModel(db.Model):
    __tablename__ = 'currency'

    currency_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(5))
    date = db.Column(db.DateTime, default=datetime.now())
    exchange = db.Column(db.Float(precision=20))

    def __init__(self, currency_id, code, date, exchange):
        self.currency_id = currency_id
        self.code = code
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            self.date = formatted_date
        self.exchange = exchange

    @classmethod
    def find_by_code(cls, code):
        return cls.query.order_by(CurrencyModel.date.desc()).filter_by(code=code).first()

    @classmethod
    def find_by_id(cls, currency_id):
        return cls.query.filter_by(currency_id=currency_id).first()

    @classmethod
    def find_latest_by_code(cls, code):
        return cls.query.filter_by(code=code).order_by(CurrencyModel.date.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'currency_id': self.currency_id,
                'code': self.code,
                'date': str(self.date)[:19],
                'exchange': self.exchange}
