from app import db
from sqlalchemy.ext.associationproxy import association_proxy

class Currency(db.Model):
    __tablename__ = 'currencies'
    currency_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    acronym = db.Column(db.String, nullable=False, unique=True)
    currency_type = db.Column(db.Enum('fiat', 'crypto', name='currency_type'), nullable=False)
    symbol = db.Column(db.String(1), nullable=True)
    components = association_proxy('components', 'portfolio')
    debit_trades = association_proxy('trades', 'author')
    credit_trades = association_proxy('trades', 'author')