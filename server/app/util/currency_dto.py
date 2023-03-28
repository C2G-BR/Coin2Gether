from flask_restx import Namespace, fields


class CurrencyDto:
    api = Namespace('currencies', description='currency related operations')
    model = api.model('currency', {
        'id': fields.Integer(readonly=True, attribute='currency_id'),
        'name': fields.String(required=True),
        'acronym': fields.String(required=True),
        'currency_type': fields.String(required=True, choices=('fiat', 'crypto')),
        'symbol': fields.String(required=True)
    })