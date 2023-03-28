from datetime import datetime
import random
from flask_restx import Resource, Namespace
from flask import request
from flask_cors import cross_origin
from app.service.user_service import *
from app.service.auth_service import verify_abort
from app.service.portfolio_service import get_portfolio_by_user_id_currency
from app.util.user_dto import UserDto
from flask_cors import CORS, cross_origin

api = UserDto.api
_user = UserDto.model
_username = UserDto.model_username
_login = UserDto.model_login
_token = UserDto.model_token
_signup = UserDto.model_signup
_profile = UserDto.model_profile
_update_receive = UserDto.model_update_receive
_update_send = UserDto.model_update_send

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/<int:user_id>')
class UserById(Resource):
    @api.doc('User by ID')
    @api.marshal_with(_user)
    @api.response(404, 'User Not Found')
    def get(self, user_id):
        return get_user_by_id(user_id)

@api.route('/signup')
class SignUp(Resource):
    @api.doc('Signup')
    @api.expect(_signup, envelope='data')
    @api.response(404, 'Errors with SignUp')
    def post(self):
        data = request.json
        try:
            accounts = data["accounts"]
        except:
            accounts = None
        register(username=data["username"], email=data["email"], lastName=data["lastName"], firstName=data["firstName"], birthdate=data["birthdate"], socialMediaProfiles=accounts, password=data["password"])

@api.route('/usernames')
class Usernames(Resource):
    @api.doc('Usernames')
    # @api.marshal_list_with(envelope='data')
    @api.response(404, 'Errors with Usernames')
    def get(self):
        usernames = get_all_usernames()

        return { "data": usernames }

@api.route('/signin')
class Login(Resource):
    @api.doc('Signin')
    @api.expect(_login, validate=True)
    @api.response(404, 'Wrong credentials or user not found')
    # @cross_origin(supports_credentials=True)
    # @api.marshal_with(_token, envelope='data')
    @cross_origin(supports_credentials=True)
    def post(self):
        email = request.json["email"]
        password = request.json["password"]
        token, username = login(email, password)
        return {"message" : "Successfully authenticated", "username" : username}, 201, {"Authorization" :  token, "Access-Control-Expose-Headers": "Authorization"}

@api.route('/<string:username>')
class UserByUsername(Resource):
    @api.doc('Get User by username')
    @api.marshal_with(_profile)
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Wrong username or user not found')
    def get(self, username):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        user = get_user_by_username(username)
        requester = get_user_from_token(token)
        user.follows = requester.is_following(user)
 
        if (user.portfolio):
            user.portfolio = get_portfolio_by_user_id_currency(user.user_id)
        user.correct_trades = 0
        user.wrong_trades = 0
        len_trades = len(user.trades)
        if (len_trades > 0):
            user.correct_trades = random.randint(0, len_trades)
            user.wrong_trades = len_trades - user.correct_trades       
        return user

@api.route('/<string:username>/follow')
class Follow(Resource):
    @api.doc('Follow')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Wrong credentials or user not found')
    def get(self, username):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return follow(token, username)

@api.route('/<string:username>/unfollow')
class Unfollow(Resource):
    @api.doc('Unfollow')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Wrong credentials or user not found')
    def get(self, username):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return unfollow(token, username)

@api.route('/verify-token')
class VerifyToken(Resource): 
    @api.expect(auth_parser, validate=True)
    @api.doc('Verifies Token')
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        if verify_abort(token):
            response_object = {
                'status': 'success',
                'message': 'Token is valid'
            }
            return response_object, 201

@api.route('/update')
class UpdateUser(Resource): 
    @api.expect(auth_parser, _update_receive, validate=True, envelope='data')
    @api.doc('Verifies Token')
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        data = request.json
        try:
            accounts = data["account"]
        except:
            accounts = None
        return update_user(token, firstName = data["firstName"], lastName = data["lastName"], birthdate = data["birthdate"], socialMediaProfiles = accounts)

    @api.expect(auth_parser, validate=True)
    @api.marshal_with(_update_send)
    @api.doc('Receive relevant attributes that can be updated')
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        user = get_user_from_token(token)
        return user