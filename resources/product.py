from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.product import ProductModel


class ProductList(Resource):

    @jwt_required
    def get(self):
        return [product.json() for product in ProductModel.find_all()]


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=int,
                        required=False)
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('selling_price',
                        type=float,
                        required=False
                        )
    parser.add_argument('stock_price',
                        type=float,
                        required=False
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('provider_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('billable',
                        type=bool,
                        required=False)

    @jwt_required
    def post(self):
        data = Product.parser.parse_args()

        product = ProductModel(**data)

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred creating the operation"}, 500

        return product.json(), 201

    @jwt_required
    def put(self):
        data = Product.parser.parse_args()

        product = ProductModel(**data)

        try:
            product.update_to_db()
        except:
            return {"message": "An error occurred updating the operation"}, 500

        return {"message": "update OK"}, 200
