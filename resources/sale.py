from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.sale import SaleModel
from models.sold_product import SoldProductModel
from models.transaction import TransactionModel
from models.category import CategoryModel
import math
from resources.email_dispatcher import send_email, prepare_sale_email, prepare_provider_email


from utils import str_to_bool


class Sale(Resource):

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)

        total = 0
        sold_products = []

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
            sold_product = SoldProductModel(product_id=product.get('product_id'),
                                            price=product.get('price'), adults=product.get('adults'),
                                            children=product.get('children'), date=product.get('date'),
                                            babies=product.get('babies'),
                                            transfer=product.get('transfer'),
                                            sale_id=sale.sale_id, payment_pending=True)
            sold_product.save_to_db()
            sold_products.append(sold_product)
            prod_sold_msg = prepare_provider_email(product, sale)
            result = send_email(sold_product.product.provider.email, prod_sold_msg)

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

        sale_msg = prepare_sale_email(sale, sold_products)
        result = send_email(sale.client.email, sale_msg)
        json_sale = sale.json()
        json_sale['email_sent'] = result
        return json_sale, 201

    @classmethod
    def are_equal(cls, total_sum, total_sale):
        return not math.fabs(total_sum - total_sale) >= 1


class SaleList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('deleted', type=str)

    @jwt_required
    def get(self):
        custom_filter = SaleList.parser.parse_args()
        response = []

        if custom_filter.get('deleted'):
            sales =  SaleModel.filter_by_deleted(str_to_bool(custom_filter.get('deleted')))
        else:
            sales = SaleModel.find_all()

        for sale in sales:
            products_from_sale = SoldProductModel.find_by_sale_id(sale.sale_id)
            # payments_from_sale = TransactionModel.find_by_sale_id(sale.sale_id)

            sale_element = {"sale_id": sale.sale_id,
                            "date": str(sale.date)[:19],
                            "client": sale.client.json(),
                            "total": sale.total,
                            "discount": sale.discount,
                            "user_commission": sale.user_commission,
                            "promoter_commission": sale.promoter_commission,
                            "deleted": sale.deleted,
                            # "payments": [payment.json() for payment in payments_from_sale],
                            "products": [product.json() for product in products_from_sale]}

            if sale.promoter:
                sale_element["promoter"] = sale.promoter.json()
            if sale.user:
                sale_element["seller"] = sale.user.json()

            response.append(sale_element)

        return response


class SaleId(Resource):

    #Test to avoid 422 without authentication @jwt_required
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
                "products": [product.json() for product in products_from_sale],
                "deleted": sale.deleted}, 200

    @jwt_required
    def delete(self, sale_id):

        try:
            products_from_sale = SoldProductModel.find_by_sale_id(sale_id)
            payments_from_sale = TransactionModel.find_by_sale_id(sale_id)

            for sold_product in products_from_sale:
                SoldProductModel.delete_from_db(sold_product.sold_product_id)

            for payment in payments_from_sale:
                TransactionModel.delete_from_db(payment.transaction_id)

            SaleModel.delete_from_db(sale_id)

        except:
            return {"message": "An error occurred deleting the sale"}, 500

        return {"message": "Sale deleted"}, 200
