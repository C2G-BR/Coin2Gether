from flask_restx import Resource, Namespace
from flask import request
from app.service.user_service import *
from app.service.post_service import *
from app.util.blog_dto import BlogDto
from app.service.auth_service import verify_abort

api = BlogDto().api
_blog = BlogDto.model
_blog_short = BlogDto.model_shorted
_blog_new = BlogDto.model_new

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/<int:blog_id>')
class BlogID(Resource):
    @api.doc('Blog ID')
    @api.marshal_list_with(_blog, envelope='data')
    @api.response(404, 'Wrong Request')
    def get(self, blog_id):
        return get_post_by_id(blog_id)

@api.route('/<string:username>')
class BlogFromUser(Resource):
    @api.doc('Blog Username')
    @api.marshal_list_with(_blog, envelope='data')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Wrong Request')
    def get(self, username):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_posts_by_username(username)

@api.route('/followed')
class BlogFollowed(Resource):
    @api.doc('Blog Followed')
    @api.marshal_list_with(_blog_short, envelope='data')
    @api.expect(auth_parser, validate=True)
    @api.response(404, 'Wrong Request')
    def get(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        return get_followed_posts(token)

@api.route('/')
class Blog(Resource):
    @api.doc('Blog')
    @api.response(404, 'Wrong Request')
    @api.marshal_list_with(_blog_short, envelope='data')
    def get(self):
        return get_all_posts()

    @api.doc('New Blog-Post')
    @api.response(404, 'Wrong Request')
    @api.expect(auth_parser, _blog_new, envelope='data')
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        verify_abort(token)
        data = request.json
        return new_post(token, data)