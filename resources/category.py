from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.category import CategoryModel

_category_parser = reqparse.RequestParser()
_category_parser.add_argument('name',
                              type=str,
                              required=True,
                              help="This field cannot be left blank!"
                              )
_category_parser.add_argument('description',
                              type=str,
                              required=False
                              )
_category_parser.add_argument('category_id',
                              type=int,
                              required=False)
_category_parser.add_argument('label',
                              type=str,
                              required=True,
                              help="This field cannot be left blank!")


class CategoryList(Resource):

    @jwt_required
    def get(self):
        categories = CategoryModel.find_all()
        if categories:
            return [category.json() for category in categories]
        return {'message': 'no categories for user'}, 404


class Category(Resource):

    @jwt_required
    def post(self):
        data = _category_parser.parse_args()

        category = CategoryModel(**data)

        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the category"}, 500

        return category.json(), 201

    @jwt_required
    def put(self):
        data = _category_parser.parse_args()

        category = CategoryModel(**data)

        try:
            category.update_to_db()
        except:
            return {"message": "An error occurred updating the category"}, 500

        return category.json(), 200
