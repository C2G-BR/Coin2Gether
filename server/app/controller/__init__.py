from flask import Blueprint
from flask_restx import Api
from .user import api as user_ns
from .trade import api as trade_ns
from .currency import api as currency_ns
from .portfolio import api as portfolio_ns
from .component import api as component_ns
from .post import api as blog_ns
from .chatbot import api as chatbot_ns
from .recommender import api as recommender_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint, title="FLASK RESTX API", version="1.0", description="FLASK RESTX API "
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(trade_ns, path='/trades')
api.add_namespace(currency_ns, path='/currencies')
api.add_namespace(portfolio_ns, path='/portfolios')
api.add_namespace(component_ns, path='/components')
api.add_namespace(blog_ns, path='/blogs')
api.add_namespace(chatbot_ns, path='/chatbot')
api.add_namespace(recommender_ns, path='/recommender')