from flask_restx import Namespace, fields

class BlogDto:
    api = Namespace('blogs')
    model = api.model('posts', {
        'id': fields.Integer(required=True, attribute='post_id'),
        'author': fields.String(required=True, attribute='user.username'),
        'title': fields.String(required=True),
        'content': fields.String(required=True, attribute='description'),
        'date': fields.Date(required=False)
    })
    model_shorted = api.model('posts_short', {
        'id': fields.Integer(required=True, attribute='post_id'),
        'author': fields.String(required=True, attribute='user.username'),
        'title': fields.String(required=True),
        'content': fields.String(required=True, attribute=lambda x: x.description[:150]),
        'date': fields.Date(required=False)
    })
    model_new = api.model('post_new', {
        'title': fields.String(required=True),
        'content': fields.String(required=True, attribute='description')
    })
    