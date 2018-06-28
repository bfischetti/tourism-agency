from db import db


class PromoterModel(db.Model):
    __tablename__ = 'promoter'

    promoter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def update_to_db(self):
        promoter_to_update = PromoterModel.find_by_id(self.promoter_id)
        if self.first_name is not None:
            promoter_to_update.first_name = self.first_name
        if self.last_name is not None:
            promoter_to_update.last_name = self.last_name
        if self.email is not None:
            promoter_to_update.email = self.email

        promoter_to_update.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_mail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(promoter_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(PromoterModel.first_name).all()

    def json(self):
        return {'promoter_id': self.promoter_id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name}
