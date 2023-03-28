from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.create_db import create_db

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
 
    bcrypt.init_app(app)
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            from app.model.currency import Currency
            if (Currency.query.first() is None):
                from app.generate import generate
                generate()
        except Exception as e:
            create_db()
            db.create_all()
            from app.generate import generate
            generate()
    from app.controller import blueprint as api
    app.register_blueprint(api, url_prefix="/v1")

    CORS(app, support_credentials=True)
    return app