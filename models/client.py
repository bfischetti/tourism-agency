from db import db


class ClientModel(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200))
    nationality = db.Column(db.String(80))
    hotel = db.Column(db.String(200))
    adults = db.Column(db.Integer)
    children = db.Column(db.Integer)
    babies = db.Column(db.Integer)

    def update_to_db(self):
        user_to_update = ClientModel.find_by_id(self.client_id)
        if self.email is not None:
            user_to_update.email = self.email
        if self.name is not None:
            user_to_update.name = self.name
        if self.nationality is not None:
            user_to_update.nationality = self.nationality
        if self.hotel is not None:
            user_to_update.hotel = self.hotel
        if self.adults is not None:
            user_to_update.adults = self.adults
        if self.children is not None:
            user_to_update.children = self.children
        if self.babies is not None:
            user_to_update.babies = self.babies

        user_to_update.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(ClientModel.name).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(client_id=_id).first()

    def json(self):
        return {'client_id': self.client_id,
                'email': self.email,
                'name': self.name,
                'nationality': self.nationality,
                'hotel': self.hotel,
                'adults': self.adults,
                'children': self.children,
                'babies': self.babies}
