from flask_restx import Namespace, fields
from .component_dto import ComponentDto


class PortfolioDto:
    api = Namespace('portfolios', description='portfolio related operations')
    model = api.model('portfolio', {
        'name': fields.String(readonly=True, attribute='name'),
        'user_id': fields.Integer(readonly=True),
        'components': fields.List(
            fields.Nested(ComponentDto().detailed_model)
        )
    })