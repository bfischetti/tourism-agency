from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt,
                                fresh_jwt_required)
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank")
_user_parser.add_argument('first_name',
                          type=str,
                          required=False)
_user_parser.add_argument('last_name',
                          type=str,
                          required=False)


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=False)
    parser.add_argument('password',
                        type=str,
                        required=False)
    parser.add_argument('first_name',
                        type=str,
                        required=False)
    parser.add_argument('last_name',
                        type=str,
                        required=False)

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}
        return user.json()

    @fresh_jwt_required
    def put(self):
        user_id = get_jwt_identity()
        data = User.parser.parse_args()

        user_to_update = UserModel(**data)
        user_to_update.update_to_db(user_id)

        return {"message": "User updated successfully."}, 200


class UserRegister(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(user.user_id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def get(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
