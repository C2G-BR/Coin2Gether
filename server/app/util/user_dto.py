from flask_restx import Namespace, fields

from .portfolio_dto import PortfolioDto


class UserDto:
    api = Namespace('users', description='user related operations')
    model = api.model('user', {
        'id': fields.Integer(readonly=True, attribute='user_id'),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'birthdate': fields.Date(required=True),
        'join_date': fields.DateTime(readonly=True),
        'trade_ids': fields.List(
            fields.Integer(attribute='trade_id'),
            attribute='trades'
        ),
        'portfolio': fields.Nested(
            PortfolioDto().model
        )
    })
    model_links = api.model('links', {
        'name': fields.String(attribute='username'),
        'platform': fields.String(attribute='platform.platform_name'),
        'link': fields.String(attribute=lambda x: x.platform.platform_specific_link + x.username)
    })
    model_account = api.model('account', {
        'socialMediaPlatform': fields.String(required=True, attribute='platform.platform_name'),
        'socialMediaAccount': fields.String(required=True, attribute='username')
    })
    model_account2 = api.model('account2', {
        'socialMediaPlatform': fields.String(required=True, attribute='platform.platform_name'),
        'username': fields.String(required=True, attribute='username')
    })
    model_profile = api.model('profile', {
        'id': fields.Integer(readonly=True, attribute='user_id'),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'birthdate': fields.Date(required=True),
        'join_date': fields.DateTime(readonly=True),
        'posts': fields.Integer(attribute=lambda x: x.posts.count()),
        'trades': fields.Integer(attribute=lambda x: len(x.trades)),
        'follower': fields.Integer(attribute=lambda x: len(x.followers.all())),
        'correct_trades': fields.Integer(),
        'wrong_trades': fields.Integer(),
        'follows': fields.Boolean(attribute='follows'),
        'links': fields.List(
                fields.Nested(
                    model_links
                ),
                attribute='accounts'
            ),
        'portfolio': fields.Nested(
            PortfolioDto().model
        )
    })
    model_recommend = api.model('recommend', {
        'id': fields.Integer(readonly=True, attribute='user_id'),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'birthdate': fields.Date(required=True),
        'join_date': fields.DateTime(readonly=True),
        'posts': fields.Integer(attribute=lambda x: x.posts.count()),
        'trades': fields.Integer(attribute=lambda x: len(x.trades)),
        'follower': fields.Integer(attribute=lambda x: len(x.followers.all()))
    })
    model_update_send = api.model('update', {
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'birthdate': fields.Date(required=True),
        'account': fields.List(fields.Nested(model_account), attribute='accounts', required=False)
    })
    model_update_receive = api.model('update', {
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'birthdate': fields.Date(required=True),
        'account': fields.List(fields.Nested(model_account2))
    })
    model_username = api.model('username', {
        'username': fields.String(required=True)
    })
    model_login = api.model('login', {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })
    model_token = api.model('token', {
        'token': fields.String(required=True)
    })
    model_signup = api.model('signup', {
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'lastName': fields.String(required=True),
        'firstName': fields.String(required=True),
        'password': fields.String(), # not to good idea
        'birthdate': fields.Date(required=True),
        'accounts': fields.List(fields.Nested(model_account))
    })