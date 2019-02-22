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
                        required=False
                        )
    parser.add_argument('code',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
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


class CurrencyId(Resource):

    @jwt_required
    def get(self, currency_id):
        currency = CurrencyModel.find_by_id(currency_id)

        if not currency:
            return {"message": "no currency with that id"}, 404

        return currency.json(), 200


class CurrencyList(Resource):

    @jwt_required
    def get(self):

        currencies = []

        usd = CurrencyModel.find_latest_by_code('USD')
        brl = CurrencyModel.find_latest_by_code('BRL')
        eur = CurrencyModel.find_latest_by_code('EUR')
        ars = CurrencyModel.find_latest_by_code('ARS')
        brt = CurrencyModel.find_latest_by_code('BRT')

        if usd:
            currencies.append(usd.json())
        if brl:
            currencies.append(brl.json())
        if eur:
            currencies.append(eur.json())
        if ars:
            currencies.append(ars.json())
        if brt:
            currencies.append(brt.json())

        return currencies

