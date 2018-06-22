from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.sale import SaleModel
from models.sold_product import SoldProductModel
from models.transaction import TransactionModel


class Product(object):
    def __init__(self, product_id, price):
        self.product_id = product_id
        self.price = price


class Sale(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('products',
                        type=Product,
                        location='json',
                        action='append',
                        required=False
                        )
    parser.add_argument('total',
                        type=float,
                        required=True)
    parser.add_argument('user_id',
                        type=int,
                        required=False
                        )
    parser.add_argument('date',
                        type=str,
                        required=False)
    parser.add_argument('sale_id',
                        type=int,
                        required=False)

    @jwt_required
    def post(self):
        data = Sale.parser.parse_args()

        if data['user_id']:
            user_id = data['user_id']
        else:
            user_id = get_jwt_identity()

        sale = SaleModel(total=data['total'], user_id=user_id, date=data['date'],
                         sale_id=data['sale_id'])

        sale.save_to_db()

        for product in data['products']:
            sold_product = SoldProductModel(product_id=product.product_id['product_id'],
                                            price=product.product_id['price'],
                                            sale_id=sale.sale_id)

            sold_product.save_to_db()

        transaction = TransactionModel(transaction_id=None, amount=sale.total, date=str(sale.date)[:19],
                                       description=None, is_expense=False,
                                       category_id=1, sale_id=sale.sale_id)
        transaction.save_to_db()

        return transaction.json(), 201
