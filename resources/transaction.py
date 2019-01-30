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
                        required=True)
    parser.add_argument('description',
                        type=str,
                        required=True
                        )
    parser.add_argument('date',
                        type=str,
                        required=False)
    parser.add_argument('category_id',
                        type=int,
                        required=True)
    parser.add_argument('sale_id',
                        type=int,
                        required=False)
    parser.add_argument('method',
                        type=str,
                        required=False)

    @jwt_required
    def post(self):
        data = Transaction.parser.parse_args()

        product = TransactionModel(**data)

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred creating the operation"}, 500

        return product.json(), 201

    @jwt_required
    def put(self):
        data = Transaction.parser.parse_args()

        product = TransactionModel(**data)

        try:
            product.update_to_db()
        except:
            return {"message": "An error occurred updating the operation"}, 500

        return product.json(), 200
