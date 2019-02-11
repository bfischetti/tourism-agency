from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.transaction import TransactionModel


class TransactionList(Resource):

    @jwt_required
    def get(self):
        return [transaction.json() for transaction in TransactionModel.find_all()]


class Transaction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('transaction_id',
                        type=int,
                        required=False)
    parser.add_argument('amount',
                        type=float,
                        required=False
                        )
    parser.add_argument('is_expense',
                        type=bool,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date',
                        type=str,
                        required=False)
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('sale_id',
                        type=int,
                        required=False)
    parser.add_argument('method',
                        type=str,
                        required=False)
    parser.add_argument('exchange',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('currency_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required
    def post(self):
        data = Transaction.parser.parse_args()

        transaction = TransactionModel(**data)

        try:
            transaction.save_to_db()
        except:
            return {"message": "An error occurred creating the transaction"}, 500

        return transaction.json(), 201

    @jwt_required
    def put(self):
        data = Transaction.parser.parse_args()

        transaction = TransactionModel(**data)

        try:
            transaction.update_to_db()
        except:
            return {"message": "An error occurred updating the transaction"}, 500

        return transaction.json(), 200
