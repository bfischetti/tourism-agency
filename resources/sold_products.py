from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.sold_product import SoldProductModel
from models.transaction import TransactionModel
from models.category import CategoryModel


class Product(object):
    def __init__(self, id):
        self.id = id


class PendingProducts(Resource):

    @jwt_required
    def get(self):
        return [sold_product.json() for sold_product in SoldProductModel.get_unpaid()]


class PayProducts(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('products',
                        type=Product,
                        location='json',
                        action='append',
                        required=False)
    parser.add_argument('total',
                        type=float,
                        required=True)
    parser.add_argument('date',
                        type=str,
                        required=True)

    @jwt_required
    def post(self):
        data = PayProducts.parser.parse_args()

        try:

            for payed_product in data['products']:
                sold_product = SoldProductModel.find_by_id(payed_product.id['id'])
                sold_product.payment_pending = False
                sold_product.update_to_db()

        except:
            return {"message": "an error occurred while updating the sales"}, 500

        category = CategoryModel.find_by_name('pago_provedor')

        if not category:
            category = CategoryModel.create_category('pago_provedor')

        transaction = TransactionModel(transaction_id=None, amount=data['total'], date=str(data['date'])[:19],
                                       description=None, is_expense=True,
                                       category_id=category.category_id)
        transaction.save_to_db()

        return transaction.json(), 201
