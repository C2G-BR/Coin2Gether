import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') + os.environ.get('DATABASE_NAME')

class TestConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY_TEST')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')

class TokenConfig:
    SECRET_TOKEN_KEY = os.environ.get('SECRET_TOKEN_KEY')

CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')