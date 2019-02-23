from db import db
import json


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    role = db.Column(db.Integer, default=2)  # 1:admin, 2: seller, 3:promoter
    salary = db.Column(db.Float(precision=2), default=0.00)
    seller_commissions = db.Column(db.Float(precision=2), default=0.00)

    def __init__(self, email, password, first_name, last_name, role=None):

        if not(role and role != 1):
            role = UserModel.check_if_admin(email)
        self.role = role
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

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
        if self.salary is not None:
            user_to_update.salary = self.salary

        if not(self.role and self.role != 1):
            user_to_update.role = UserModel.check_if_admin(user_to_update.email)
        else:
            user_to_update.role = self.role

        user_to_update.save_to_db()

    @classmethod
    def check_if_admin(cls, email):
        role = 2
        with open('./config.json', 'r') as f:
            config = json.load(f)
            admins = config["admins"]

        for admin in admins:
            if email == admin["email"]:
                role = 1

        return role

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
    def delete_by_id(cls, _id):
        user = cls.find_by_id(_id)
        db.session.delete(user)
        db.session.commit()
        return

    @classmethod
    def find_all(cls):
        return cls.query.order_by(UserModel.last_name).all()

    @classmethod
    def find_promoters(cls):
        return cls.query.filter_by(role=3).all()

    @classmethod
    def find_sellers(cls):
        return cls.query.filter_by(role=2).all()

    def json(self):
        return {'user_id': self.user_id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'role': self.role}
