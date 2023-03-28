from flask_restx import Resource
from app.util.currency_dto import CurrencyDto
from app.service.currency_service import *
from app.service.auth_service import verify_abort

api = CurrencyDto().api
_currency = CurrencyDto().model

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/')
class CurrencyList(Resource):
    @api.doc('List of currencies')
    @api.marshal_list_with(_currency, envelope='data')
    def get(self):
        return get_all_currencies()

@api.route('/user')
class CurrencyByUser(Resource):
    @api.doc('List of available currencies for the user')
    @api.marshal_list_with(_currency, envelope='data')
    @api.expect(auth_parser)
    @api.response(403, 'Not Authorized')
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_currency_by_user(token)