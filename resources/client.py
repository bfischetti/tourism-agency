from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.client import ClientModel


class ClientList(Resource):

    @jwt_required
    def get(self):
        return [client.json() for client in ClientModel.find_all()]


class Client(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('client_id',
                        type=int,
                        required=False)
    parser.add_argument('name',
                        type=str,
                        required=True)
    parser.add_argument('email',
                        type=str,
                        required=True)
    parser.add_argument('passport_number',
                        type=str,
                        required=False)
    parser.add_argument('nationality',
                        type=str,
                        required=False)
    parser.add_argument('hotel',
                        type=str,
                        required=False)
    parser.add_argument('address',
                        type=str,
                        required=False)
    parser.add_argument('room_number',
                        type=str,
                        required=False)
    parser.add_argument('contact_number',
                        type=str,
                        required=False)


    @jwt_required
    def post(self):
        data = Client.parser.parse_args()

        client = ClientModel(**data)

        try:
            client.save_to_db()
        except:
            return {"message": "An error occurred creating the client"}, 500

        return client.json(), 201

    @jwt_required
    def put(self):
        data = Client.parser.parse_args()

        client = ClientModel(**data)

        try:
            client.update_to_db()
        except:
            return {"message": "An error occurred updating the operation"}, 500

        return client.json(), 200
