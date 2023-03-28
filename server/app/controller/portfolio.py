from flask import request
from flask_restx import Resource
from app.util.portfolio_dto import PortfolioDto
from app.util.component_dto import ComponentDto
from app.service.portfolio_service import *
from app.service.auth_service import verify_token, verify_abort

api = PortfolioDto().api
_portfolio = PortfolioDto().model
_component_condensed = ComponentDto().condensed_model

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/')
class PortfolioByToken(Resource):
    @api.doc('Users Portfolio')
    @api.marshal_with(_portfolio)
    @api.expect(auth_parser)
    @api.response(404, 'No Portfolio Found')
    @api.response(403, 'Not Authorized')
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_portfolio_by_token(token)

    @api.doc('Create a new or update an existing Portfolio for a user')
    @api.expect(auth_parser, [_component_condensed], validate=True)
    @api.response(403, 'Not Authorized')
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return create_update_portfolio_by_token(token, request.json)
