from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.email

    def update_to_db(self, user_id):
        user_to_update = UserModel.find_by_id(user_id)
        if self.first_name is not None:
            user_to_update.first_name = self.first_name
        if self.last_name is not None:
            user_to_update.last_name = self.last_name
        if self.password is not None:
            user_to_update.password = self.password

        user_to_update.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    def json(self):
        return {'user_id': self.user_id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name}
