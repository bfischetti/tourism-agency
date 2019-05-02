from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.provider import ProviderModel
from utils import str_to_bool


class ProviderList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('deleted', type=str)

    @jwt_required
    def get(self):
        custom_filter = ProviderList.parser.parse_args()

        if custom_filter.get('deleted'):
            return [transaction.json() for transaction
                    in ProviderModel.filter_by_deleted(str_to_bool(custom_filter.get('deleted')))]
        else:
            return [provider.json() for provider in ProviderModel.find_all()]


class Provider(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('provider_id',
                        type=int,
                        required=False)
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('url',
                        type=str,
                        required=False
                        )
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=False)
    parser.add_argument('commission_rate',
                        type=float,
                        required=False)

    @jwt_required
    def post(self):
        data = Provider.parser.parse_args()

        provider = ProviderModel(**data)

        try:
            provider.save_to_db()
        except:
            return {"message": "An error occurred creating the operation"}, 500

        return provider.json(), 201

    @jwt_required
    def put(self):
        data = Provider.parser.parse_args()

        provider = ProviderModel(**data)

        try:
            provider.update_to_db()
        except:
            return {"message": "An error occurred updating the operation"}, 500

        return provider.json(), 200


class ProviderId(Resource):

    @jwt_required
    def get(self, provider_id):
        return ProviderModel.find_by_id(provider_id).json()

    @jwt_required
    def delete(self, provider_id):

        try:
            ProviderModel.delete_from_db(provider_id)
        except:
            return {"message": "An error occurred deleting the Provider"}, 500

        return {"message": "Provider deleted"}, 200
