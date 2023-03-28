from flask_restx import Namespace, fields

from .currency_dto import CurrencyDto


class ComponentDto:
    api = Namespace('components', description='component related operations')
    model = api.model('component', {
        'portfolio_name': fields.String(readonly=True, attribute='portfolio_name'),
        'currency_id': fields.Integer(required=True, attribute='currency.currency_id'),
        'user_id': fields.Integer(required=False, attribute='portfolio_user_id'),
        'amount': fields.Float(required=True)
    })

    detailed_model = api.model('component_details', {
        'portfolio_name': fields.String(readonly=True, attribute='portfolio_name'),
        'currency': fields.Nested(
            CurrencyDto().model
        ),
        'amount': fields.Float(required=True)
    })

    condensed_model = api.model('component_condensed', {
        'portfolio_name': fields.String(readonly=True, attribute='portfolio_name'),
        'currency_id': fields.Integer(),
        'amount': fields.Float(required=True)
    })