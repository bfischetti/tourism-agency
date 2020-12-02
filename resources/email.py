from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.sale import SaleModel
from models.sold_product import SoldProductModel
from resources.email_dispatcher import send_email, prepare_sale_email

class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                       type=str,
                       required=True)
    parser.add_argument('sale_id',
                       type=int,
                       required=True)
    @jwt_required
    def post(self):
        data = Email.parser.parse_args()
        sale = SaleModel.find_by_id(data.sale_id)
        if not sale:
            return { "message": "no sale with that id" }, 404
        sold_products = SoldProductModel.find_by_sale_id(sale.sale_id)
        msg = prepare_sale_email(sale, sold_products)
        result = send_email(data.email, msg)
        return  { "success": result }


