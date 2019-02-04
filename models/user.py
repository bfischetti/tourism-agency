from db import db
import json

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    role = db.Column(db.Integer, default=2)  # 1:admin, 2: seller/promoter

    def __init__(self, email, password, first_name, last_name, role):
        with open('./config.json', 'r') as f:
            config = json.load(f)
            admins = config["admins"]
        for admin in admins:
            if email == admin["email"]:
                role = 1
                break
            else:
                role = 2
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

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
        if self.role is not None:
            user_to_update.role = self.role

        user_to_update.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_mail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    def json(self):
        return {'user_id': self.user_id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'role': self.role}
