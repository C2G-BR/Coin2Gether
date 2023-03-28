from sqlalchemy import desc, Index
from app import db
from . import *

class Trade(db.Model):
    __tablename__ = 'trades'
    __table_args__ = (
        db.CheckConstraint('debit_currency_id != credit_currency_id', name='unequal_currencies'),
        db.CheckConstraint('percentage_trade > 0 AND percentage_trade <= 100', name='real_percentage'),
        db.CheckConstraint('start_date <= end_date', name='correct_dates'),
    )
    trade_id = db.Column(db.Integer, primary_key=True)
    publish_date = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    motivation = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    expected_change = db.Column(db.Numeric(asdecimal=True), nullable=False)
    percentage_trade = db.Column(db.Numeric(asdecimal=True), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    debit_currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'), nullable=False)
    credit_currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'), nullable=False)
    author = db.relationship(User, backref=db.backref("trades", cascade="all, delete-orphan"))
    debit_currency = db.relationship(Currency, foreign_keys=debit_currency_id, backref=db.backref("debit_trades", cascade="all, delete-orphan"))
    credit_currency = db.relationship(Currency, foreign_keys=credit_currency_id, backref=db.backref("credit_trades", cascade="all, delete-orphan"))
    debit_amount = db.Column(db.Numeric(asdecimal=True), nullable=False)
    credit_amount = db.Column(db.Numeric(asdecimal=True), nullable=False)
Index('trade_publish_date_idx', Trade.publish_date.desc())