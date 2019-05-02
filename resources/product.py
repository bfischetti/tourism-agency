from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.product import ProductModel
from utils import str_to_bool


class ProductList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('deleted', type=str)

    @jwt_required
    def get(self):
        custom_filter = ProductList.parser.parse_args()

        if custom_filter.get('deleted'):
            return [transaction.json() for transaction
                    in ProductModel.filter_by_deleted(str_to_bool(custom_filter.get('deleted')))]
        else:
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
    parser.add_argument('selling_price_adult',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('stock_price_adult',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('selling_price_child',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('stock_price_child',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('selling_price_baby',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('stock_price_baby',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
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
    parser.add_argument('deleted',
                        type=str,
                        required=False,)

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


class ProductId(Resource):

    @jwt_required
    def delete(self, product_id):

        try:
            ProductModel.delete_from_db(product_id)
        except:
            return {"message": "An error occurred deleting the Product"}, 500

        return {"message": "Product deleted"}, 200
