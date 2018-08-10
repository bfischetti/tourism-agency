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
                        required=False)
    parser.add_argument('total',
                        type=float,
                        required=True)
    parser.add_argument('seller_id',
                        type=int,
                        required=False)
    parser.add_argument('date',
                        type=str,
                        required=False)
    parser.add_argument('sale_id',
                        type=int,
                        required=False)
    parser.add_argument('client_id',
                        type=int,
                        required=False)
    parser.add_argument('promoter_id',
                        type=int,
                        required=False)
    parser.add_argument('promoter_commission',
                        type=float,
                        required=False)
    parser.add_argument('seller_commission',
                        type=float,
                        required=False)

    @jwt_required
    def post(self):
        data = Sale.parser.parse_args()

        if data['seller_id']:
            user_id = data['seller_id']
        else:
            user_id = get_jwt_identity()

        sale = SaleModel(total=data['total'], user_id=user_id, date=data['date'],
                         sale_id=data['sale_id'], client_id=data['client_id'], promoter_id=data['promoter_id'],
                         promoter_commission=data['promoter_commission'], user_commission=data['seller_commission'])

        sale.save_to_db()

        for product in data['products']:
            sold_product = SoldProductModel(product_id=product.product_id['product_id'],
                                            price=product.product_id['price'], adults=product.product_id['adults'],
                                            children=product.product_id['children'], date=product.product_id['date'],
                                            babies=product.product_id['babies'],
                                            transfer=product.product_id['transfer'],
                                            sale_id=sale.sale_id)
            sold_product.save_to_db()

        transaction = TransactionModel(transaction_id=None, amount=sale.total, date=str(sale.date)[:19],
                                       description=None, is_expense=False,
                                       category_id=1, sale_id=sale.sale_id)
        transaction.save_to_db()

        return transaction.json(), 201


class Voucher(Resource):

    @jwt_required
    def get(self, sale_id):
        sale = SaleModel.find_by_id(sale_id)

        if not sale:
            return {"message": "no sale with that id"}, 404

        products_from_sale = SoldProductModel.find_by_sale_id(sale_id)

        return {"sale_id": sale.sale_id,
                "client": sale.client.json(),
                "total": sale.total,
                "user_commission": sale.user_commission,
                "promoter_commission": sale.promoter_commission,
                "products": [product.json() for product in products_from_sale]}, 200
