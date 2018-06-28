import os

from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST

from resources.user import User, UserLogin, UserLogout, UserRegister, TokenRefresh
from resources.provider import Provider, ProviderList
from resources.product import Product, ProductList
from resources.category import Category, CategoryList
from resources.transaction import TransactionList, Transaction
from resources.sale import Sale, Voucher
from resources.client import Client, ClientList
from resources.promoter import Promoter, PromoterList


app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'bruno'

api = Api(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'fresh_revoked'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user')
api.add_resource(Provider, '/provider')
api.add_resource(ProviderList, '/providers')
api.add_resource(Product, '/product')
api.add_resource(ProductList, '/products')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/category')
api.add_resource(TransactionList, '/transactions')
api.add_resource(Transaction, '/transaction')
api.add_resource(Sale, '/sale')
api.add_resource(Voucher, '/sale/<int:sale_id>')
api.add_resource(Client, '/client')
api.add_resource(ClientList, '/clients')
api.add_resource(Promoter, '/promoter')
api.add_resource(PromoterList, '/promoters')

if __name__ == '__main__':

    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000, debug=True)
