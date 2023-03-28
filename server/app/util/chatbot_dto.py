from flask_restx import Namespace, fields

class ChatbotDto:
    api = Namespace('chatbot')
    receive_model = api.model('chatbot', {
        'message': fields.String(required=False),
        'session_id': fields.String(required=False)
    })
    response_model = api.model('chatbot_response', {
        'message': fields.String(required=False),
        'session_id': fields.String(required=False),
        'is_action': fields.Boolean(required=True),
        'is_confirmation': fields.Boolean(required=True)
    })