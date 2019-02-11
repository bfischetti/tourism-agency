from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.sale import SaleModel
from models.sold_product import SoldProductModel
from models.transaction import TransactionModel
from models.category import CategoryModel
import math


class Sale(Resource):

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)

        total = 0

        for payment in json_data.get('payments'):

            if json_data.get('credit_charge'):
                charge = json_data.get('credit_charge')
            else:
                charge = 1

            total += payment.get('amount') * payment.get('exchange') * charge

        if not Sale.are_equal(total, json_data.get('total')):
            return {'message': 'Amounts are not correct'}

        if json_data.get('seller_id'):
            user_id = json_data.get('seller_id')
        else:
            user_id = get_jwt_identity()

        sale = SaleModel(total=json_data.get('total'), user_id=user_id, date=json_data.get('date'),
                         sale_id=json_data.get('sale_id'), client_id=json_data.get('client_id'),
                         promoter_id=json_data.get('promoter_id'),
                         promoter_commission=json_data.get('promoter_commission'),
                         user_commission=json_data.get('seller_commission'), discount=json_data.get('discount'))

        sale.save_to_db()

        for product in json_data.get('products'):
            print(product)
            sold_product = SoldProductModel(product_id=product.get('product_id'),
                                            price=product.get('price'), adults=product.get('adults'),
                                            children=product.get('children'), date=product.get('date'),
                                            babies=product.get('babies'),
                                            transfer=product.get('transfer'),
                                            sale_id=sale.sale_id, payment_pending=True)
            sold_product.save_to_db()

        category = CategoryModel.find_by_name('venta')

        if not category:
            category = CategoryModel.create_category('venta')

        for payment in json_data.get('payments'):
            transaction = TransactionModel(transaction_id=None, amount=payment.get('amount'), date=str(sale.date)[:19],
                                           description=payment.get('description'), is_expense=False,
                                           category_id=category.category_id,
                                           sale_id=sale.sale_id, exchange=payment.get('exchange'),
                                           method=payment.get('method'), currency_id=payment.get('currency_id'))
            transaction.save_to_db()

        return sale.json(), 201

    @classmethod
    def are_equal(cls, total_sum, total_sale):
        return not math.fabs(total_sum - total_sale) >= 1


class Sales(Resource):

    @jwt_required
    def get(self):
        return [sale.json() for sale in SaleModel.find_all()]


class Voucher(Resource):

    @jwt_required
    def get(self, sale_id):
        sale = SaleModel.find_by_id(sale_id)

        if not sale:
            return {"message": "no sale with that id"}, 404

        products_from_sale = SoldProductModel.find_by_sale_id(sale_id)
        payments_from_sale = TransactionModel.find_by_sale_id(sale_id)

        return {"sale_id": sale.sale_id,
                "date": str(sale.date)[:19],
                "client": sale.client.json(),
                "total": sale.total,
                "discount": sale.discount,
                "user_commission": sale.user_commission,
                "promoter_commission": sale.promoter_commission,
                "payments": [payment.json() for payment in payments_from_sale],
                "products": [product.json() for product in products_from_sale]}, 200
