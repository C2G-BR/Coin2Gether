from flask import request
from flask_restx import Resource, Namespace
from app.model.trade import Trade
from app.util.trade_dto import TradeDto
from app.service.trade_service import *
from app.service.auth_service import verify_abort

dto = TradeDto()
api = dto.api
_trade = dto.model
_condensed_trade = dto.condensed_model
_detailed_trade = dto.detailed_model
_create_trade = dto.create_model

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/')
class TradesList(Resource):
    @api.doc('List of trades')
    @api.marshal_list_with(_condensed_trade, envelope='data')
    @api.response(404, 'No Trade Found')
    def get(self):
        return get_all_trades()

    @api.doc('Create new trade')
    @api.expect(auth_parser, _create_trade, validate=True)
    @api.response(400, 'Trade Not Created')
    @api.response(403, 'Not Authorized')
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return post_new_trade(request.json, token)

@api.route('/followed')
class TradesListFollowed(Resource):
    @api.doc('List of trades of users I follow')
    @api.marshal_list_with(_condensed_trade, envelope='data')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'No Trade Found')
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_followed_trades(token)

@api.route('/<int:trade_id>')
class TradesById(Resource):
    @api.doc('Trade by ID')
    @api.marshal_with(_detailed_trade)
    @api.response(404, 'Trade Not Found')
    def get(self, trade_id):
        return get_trade_by_id(trade_id)

@api.route('/<string:author>')
class TradesByAuthor(Resource):
    @api.doc('List of trades from an specific author')
    @api.marshal_list_with(_condensed_trade, envelope='data')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Trades Not Found')
    def get(self, author):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_trades_by_author(author)