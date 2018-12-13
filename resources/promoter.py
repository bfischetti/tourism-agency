from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.promoter import PromoterModel


class PromoterList(Resource):

    @jwt_required
    def get(self):
        return [promoter.json() for promoter in PromoterModel.find_all()]


class Promoter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('promoter_id',
                        type=int,
                        required=False)
    parser.add_argument('first_name',
                        type=str,
                        required=True
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True
                        )
    parser.add_argument('email',
                        type=str,
                        required=True
                        )

    @jwt_required
    def post(self):
        data = Promoter.parser.parse_args()

        promoter = PromoterModel(**data)

        try:
            promoter.save_to_db()
        except:
            return {"message": "An error occurred creating the promoter"}, 500

        return promoter.json(), 201

    @jwt_required
    def put(self):
        data = Promoter.parser.parse_args()

        promoter = PromoterModel(**data)

        try:
            promoter.update_to_db()
        except:
            return {"message": "An error occurred updating the promoter"}, 500

        return promoter.json(), 200
