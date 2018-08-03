from db import db


class ClientModel(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(80))
    name = db.Column(db.String(200))
    nationality = db.Column(db.String(80))
    hotel = db.Column(db.String(200))
    address = db.Column(db.String(200))
    room_number = db.Column(db.String(10))
    contact_number = db.Column(db.String(80))

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
        if self.address is not None:
            user_to_update.address = self.address
        if self.room_number is not None:
            user_to_update.room_number = self.room_number
        if self.passport_number is not None:
            user_to_update.passport_number = self.passport_number
        if self.contact_number is not None:
            user_to_update.contact_number = self.contact_number

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
                'room_number': self.room_number,
                'address': self.address,
                'passport_number': self.passport_number,
                'contact_number': self.contact_number
                }
