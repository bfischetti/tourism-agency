from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.currency import CurrencyModel


class Currency(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('currency_id',
                        type=int,
                        required=False)
    parser.add_argument('date',
                        type=str,
                        required=True
                        )
    parser.add_argument('code',
                        type=str,
                        required=True
                        )
    parser.add_argument('exchange',
                        type=float,
                        required=True
                        )

    @jwt_required
    def post(self):
        data = Currency.parser.parse_args()

        currency = CurrencyModel(**data)

        try:
            currency.save_to_db()
        except Exception as e:
            return {"message": "An error occurred creating the currency exchange " + e}, 500

        return currency.json(), 201


class CurrencyList(Resource):

    @jwt_required
    def get(self):
        return [product.json() for product in CurrencyModel.find_all()]