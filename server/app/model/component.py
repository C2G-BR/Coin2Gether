from app import db
from . import *

class Component(db.Model):
    __tablename__ = 'components'
    __table_args__ = (
        db.ForeignKeyConstraint(['portfolio_name', 'portfolio_user_id'], ['portfolios.name', 'portfolios.user_id']),
    )
    portfolio_name = db.Column(db.String(50), primary_key=True)
    portfolio_user_id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'), primary_key=True)
    portfolio = db.relationship(Portfolio, foreign_keys=[portfolio_name, portfolio_user_id], backref=db.backref("components", cascade="all, delete-orphan"))
    currency = db.relationship(Currency, foreign_keys=currency_id, backref=db.backref("components", cascade="all, delete-orphan"))
    amount = db.Column(db.Numeric(asdecimal=True), nullable=False)
