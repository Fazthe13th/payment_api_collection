from flask_restful import Resource, reqparse
from models.User import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt)
from blacklist import BLACKLIST
# Register parser
_user_register_parser = reqparse.RequestParser()
_user_register_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='Username required'
)
_user_register_parser.add_argument(
    'email',
    type=str,
    required=True,
    help='Email address required'
)
_user_register_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='Password is required'
)
_user_register_parser.add_argument(
    'firstname',
    type=str,
    required=True,
    help='First name is required'
)
_user_register_parser.add_argument(
    'lastname',
    type=str,
    required=True,
    help='Last name is required'
)

_user_register_parser.add_argument(
    'address',
    type=str,
    required=True,
    help='Address is required'
)
# Register parser end

# login start
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='Username is required'
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='This felid cannot be blank'
)
# login end

userModel = UserModel()


class UserRegister(Resource):

    def post(self):
        data = _user_register_parser.parse_args()
        newUser = UserModel(**data)
        if newUser.find_by_username(data['username']):
            return {'message': 'This user already exists'}, 400
        newUser.save_to_db()
        return {'message': 'User created successfully'}, 201


class User(Resource):

    @classmethod
    def get(cls, username):
        user = userModel.find_by_username(username)
        if not user:
            return {'message': 'No user by this name found'}
        return userModel.json(user.username, user.email, user.firstname, user.lastname, user.address)

    @classmethod
    def delete(cls, username):
        user = userModel.find_by_username(username)
        if user:
            UserModel.delete(user)
        return {'message': 'User deleted'}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        request_data = _user_parser.parse_args()
        user = userModel.find_by_username(request_data['username'])
        if user and safe_str_cmp(user.password, request_data['password']):
            access_token = create_access_token(
                identity=user.username, fresh=True)
            refresh_token = create_refresh_token(user.username)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is jwt id
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}
