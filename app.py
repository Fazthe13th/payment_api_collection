import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from blacklist import BLACKLIST
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
# url = 'mysql+pymysql://{}:{}@{}:{}/{}'
# user = os.getenv('mariadb_user')
# password = os.getenv('mariadb_pwd')
# host = os.getenv('mariadb_host')
# port = os.getenv('mariadb_port')
# database = os.getenv('mariadb_database')
# url = url.format(user, password, host, port, database)
# app.config['SQLALCHEMY_DATABASE_URI'] = url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'Faz1313'
app.secret_key = 'faz13'
api = Api(app)
# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_token(identity):
    if identity == '38034422-b12a-11ea-9a81-eb0347fc01f2':
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'description': 'The token has expired',
                    'error': 'token_expied'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signeture varification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'description': 'Request does not contain a access token',
        'error': 'no_token'
    }), 401


@jwt.needs_fresh_token_loader
def need_refresh_token_callback():
    return jsonify({
        'description': 'This request require a fresh token',
        'error': 'unfresh_token'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'revoked_token'
    }), 401


# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(ItemList, '/items')
# api.add_resource(StoreList, '/store')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserLogin, '/login')
# api.add_resource(TokenRefresh, '/refresh')
# api.add_resource(UserLogout, '/logout')
if __name__ == "__main__":
    # from db import db

    # db.init_app(app)

    app.run(port=5000, debug=True)
