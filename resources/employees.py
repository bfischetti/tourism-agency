from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.user import UserModel


class PromoterList(Resource):

    @jwt_required
    def get(self):
        return [promoter.json() for promoter in UserModel.find_promoters()]


class SellerList(Resource):

    @jwt_required
    def get(self):
        return [seller.json() for seller in UserModel.find_sellers()]
