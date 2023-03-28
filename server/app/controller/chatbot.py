from flask_restx import Resource
from flask import request
from app.service.auth_service import verify_abort
from app.service.chatbot_service import *
from app.util.chatbot_dto import ChatbotDto

api = ChatbotDto().api
receive_model = ChatbotDto().receive_model
response_model = ChatbotDto().response_model

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers')

@api.route('/')
class Chatbot(Resource):
    @api.doc('Send a Message to the chatbot')
    @api.expect(auth_parser, receive_model, validate=False)
    @api.marshal_with(response_model)
    def post(self):
        token = auth_parser.parse_args()['Authorization']
        return handle_data(request.json, token)