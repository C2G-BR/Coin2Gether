from flask_restx import Resource
from app.service.recommender_service import *
from app.util.recommender_dto import RecommenderDto
from app.util.user_dto import UserDto
from app.service.auth_service import verify_abort

api = RecommenderDto().api
_user = UserDto.model_recommend

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/')
class Recommender(Resource):
    @api.doc('Get user recommendations based on the current user')
    @api.marshal_list_with(_user, envelope='data')
    @api.expect(auth_parser, validate=True)
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return recommend_users(token)
