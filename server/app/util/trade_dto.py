from flask_restx import Namespace, fields
from app.util.currency_dto import CurrencyDto


class TradeDto:
    api = Namespace('trades', description='trade related operations')
    model = api.model('trade', {
        'id': fields.Integer(readonly=True, attribute='trade_id'),
        'date': fields.DateTime(readonly=True, attribute='publish_date'),
        'startdate': fields.Date(required=True, attribute='start_date'),
        'enddate': fields.Date(required=True, attribute='end_date'),
        'motivation': fields.String(required=True),
        'description': fields.String(required=True),
        'expectedIncrease': fields.Float(required=True, attribute='expected_change'),
        'percent': fields.Float(required=True, attribute='percentage_trade'),
        'author_id': fields.Integer(required=True),
        'cryptocurrency': fields.Integer(required=True, attribute='debit_currency'),
        'fiatcurrency': fields.Integer(required=True, attribute='credit_currency'),
        'debit_amount': fields.Float(required=True),
        'credit_amount': fields.Float(required=True),
    })

    create_model = api.model('trade_create', {
        'id': fields.Integer(readonly=True, attribute='trade_id'),
        'date': fields.DateTime(readonly=True, attribute='publish_date'),
        'start_date': fields.Date(required=True, attribute='start_date'),
        'end_date': fields.Date(required=True, attribute='end_date'),
        'motivation': fields.String(required=True),
        'description': fields.String(required=True),
        'expected_change': fields.Float(required=True, attribute='expected_change'),
        'percentage_trade': fields.Float(required=True, attribute='percentage_trade'),
        'debit_currency_id': fields.Integer(required=True, attribute='debit_currency'),
        'credit_currency_id': fields.Integer(required=True, attribute='credit_currency')
    })

    detailed_model = api.model('trade_details', {
        'id': fields.Integer(readonly=True, attribute='trade_id'),
        'date': fields.DateTime(readonly=True, attribute='publish_date'),
        'startdate': fields.Date(required=True, attribute='start_date'),
        'enddate': fields.Date(required=True, attribute='end_date'),
        'motivation': fields.String(required=True),
        'description': fields.String(required=True),
        'expectedIncrease': fields.Float(required=True, attribute='expected_change'),
        'percent': fields.Float(required=True, attribute='percentage_trade'),
        'author': fields.String(attribute='author.username', required=True),
        'debit_currency': fields.Nested(CurrencyDto().model),
        'credit_currency': fields.Nested(CurrencyDto().model),
        'debit_amount': fields.Float(required=True),
        'credit_amount': fields.Float(required=True),
    })

    condensed_model = api.model('trade_condensed', {
        'id': fields.Integer(readonly=True, attribute='trade_id'),
        'date': fields.DateTime(readonly=True, attribute='publish_date'),
        'startdate': fields.Date(required=True, attribute='start_date'),
        'enddate': fields.Date(required=True, attribute='end_date'),
        'expectedIncrease': fields.Float(required=True, attribute='expected_change'),
        'percent': fields.Float(required=True, attribute='percentage_trade'),
        'author': fields.String(attribute='author.username', required=True),
        'cryptocurrency': fields.String(attribute='debit_currency.acronym', required=True),
        'fiatcurrency': fields.String(attribute='credit_currency.acronym', required=True),
        'debit_amount': fields.Float(required=True),
        'credit_amount': fields.Float(required=True),
    })