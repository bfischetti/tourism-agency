from db import db


class ProviderModel(db.Model):
    __tablename__ = 'provider'

    provider_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(80))

    def __init__(self, provider_id, name, url, email, phone):
        self.provider_id = provider_id
        self.name = name
        self.url = url
        self.email = email
        self.phone = phone

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(provider_id=_id).first()

    def update_to_db(self):
        provider_to_update = ProviderModel.find_by_id(self.provider_id)
        if self.name is not None:
            provider_to_update.name = self.name
        if self.url is not None:
            provider_to_update.url = self.url
        if self.category_id is not None:
            provider_to_update.email = self.email
        if self.phone is not None:
            provider_to_update.phone = self.phone

        provider_to_update.save_to_db()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(ProviderModel.name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'provider_id': self.provider_id,
                'name': self.name,
                'url': self.url,
                'email': self.email,
                'phone': self.phone}