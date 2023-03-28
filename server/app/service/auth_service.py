from app.config import TokenConfig
import datetime
import jwt
from flask_restx import abort
from app.model.user import User

def secretKey():
    secret = TokenConfig.SECRET_TOKEN_KEY
    return secret

def create_token(email):
    secret = secretKey()
    bearer = "Bearer "
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        return bearer + jwt.encode(payload, secret, algorithm='HS256')
    except Exception as e:
        return e
    
def verify_token(auth_token):
    if auth_token is None:
        abort(404, message="No token provided in Header")
    
    secret = secretKey()

    try:
        auth_token = auth_token.replace('Bearer ', '')
        payload = jwt.decode(auth_token, secret, algorithms="HS256")
        return True
    except jwt.exceptions.ExpiredSignatureError:
        abort(404, message="Token expired")
    except jwt.exceptions.InvalidSignatureError:
        abort(404, message="Token invalid")

def get_user_from_token(auth_token):
    # auth_token = auth_token[7:]

    if not verify_token(auth_token):
        abort(404, message="Token invalid")


    auth_token = auth_token.replace('Bearer ', '')

    secret = secretKey()

    payload = jwt.decode(auth_token, secret, algorithms="HS256")
    email = payload["sub"]
    user = User.query.filter_by(email=email).first()
    if user == None:
        abort(400, 'Invalid data')
    return user

def verify_abort(auth_token):
    if verify_token(auth_token):
        return True
    else:
        abort(403, 'Not Authorized')