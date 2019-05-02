import os

from flask import Flask, send_from_directory
from flask.json import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from db import db

from blacklist import BLACKLIST

from resources.user import User, UserLogin, UserLogout, UserRegister, TokenRefresh
from resources.provider import Provider, ProviderList, ProviderId
from resources.product import Product, ProductList, ProductId
from resources.category import Category, CategoryList
from resources.transaction import TransactionList, Transaction, TransactionId
from resources.sale import Sale, SaleList, SaleId
from resources.client import Client, ClientList
from resources.employees import SellerList, PromoterList
from resources.sold_products import PendingProducts, PayProducts
from resources.currency import Currency, CurrencyList, CurrencyId

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['DEBUG'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'bruno'

api = Api(app)

jwt = JWTManager(app)
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


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
    return decrypted_token['jti'] in BLACKLIST


@app.route('/')
def hello_world():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>')
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user')
api.add_resource(Provider, '/provider')
api.add_resource(ProviderList, '/providers')
api.add_resource(ProviderId, '/provider/<int:provider_id>')
api.add_resource(Product, '/product')
api.add_resource(ProductList, '/products')
api.add_resource(ProductId, '/product/<int:product_id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/category')
api.add_resource(TransactionList, '/transactions')
api.add_resource(Transaction, '/transaction')
api.add_resource(TransactionId, '/transaction/<int:transaction_id>')
api.add_resource(Sale, '/sale')
api.add_resource(SaleList, '/sales')
api.add_resource(SaleId, '/sale/<int:sale_id>')
api.add_resource(Client, '/client')
api.add_resource(ClientList, '/clients')
api.add_resource(PromoterList, '/promoters')
api.add_resource(SellerList, '/sellers')
api.add_resource(PendingProducts, '/pending')
api.add_resource(PayProducts, '/pay')
api.add_resource(Currency, '/currency')
api.add_resource(CurrencyId, '/currency/<int:currency_id>')
api.add_resource(CurrencyList, '/currencies')

if __name__ == '__main__':
    manager.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)
