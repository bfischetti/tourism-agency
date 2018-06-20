from db import db
from models.user import UserModel


class CategoryModel(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def __init__(self, name, description, category_id):
        self.name = name
        self.description = description
        self.category_id = category_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(category_id=_id).first()

    def update_to_db(self):
        category_to_update = CategoryModel.find_by_id(self.category_id)
        if self.name is not None:
            category_to_update.name = self.name
        if self.description is not None:
            category_to_update.description = self.description

        category_to_update.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(CategoryModel.name).all()

    @classmethod
    def category_already_exists(cls, name):
        if cls.query.filter_by(name=name).first():
            return True
        else:
            return False

    def json(self):
        return {'category_id': self.category_id,
                'name': self.name,
                'description': self.description}
