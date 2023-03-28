import unittest
import datetime
import random
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.config import TestConfig
from app import db
from app.model import *

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()
        self.user = User(
            username='TM',
            email='tm@chinver.com',
            lastName='Thai',
            firstName='Mingh',
            password=b'asdASD123!',
            birthdate=datetime.datetime(2000, 5, 17),
            join_date=datetime.datetime.now()
        )
        self.debit_currency = Currency(name='Bitcoin', acronym='BTC', currency_type='crypto')
        self.credit_currency = Currency(name='Euro', acronym='EUR', currency_type='fiat', symbol='€')
        self.trade = Trade( # create a general and correct trade which is not committed
            publish_date=datetime.datetime.now(),
            start_date=datetime.datetime(2021, 3, 1),
            end_date=datetime.datetime(2021, 4, 1),
            motivation='This is my motivation.',
            description='Trade now, it is important! GOGOGOGOGOGOGOGOG!!!',
            expected_change=random.randint(0, 250),
            author=self.user,
            debit_currency=self.debit_currency,
            debit_amount=round(random.uniform(0, 1_000), 2),
            credit_currency=self.credit_currency,
            credit_amount=round(random.uniform(0, 1_000), 2),
        )
        db.session.add(self.user)
        db.session.add(self.debit_currency)
        db.session.add(self.credit_currency)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_trade(self):
        trade = self.trade
        db.session.add(trade)
        db.session.commit()
        assert trade in db.session
        assert trade == Trade.query.get(1)

    def test_trade_unequal_currency_constraint(self):
        trade = self.trade
        trade.credit_currency = self.debit_currency # same as trade.debit_currency; should raise an error
        db.session.add(trade)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_trade_start_end_date_constraint(self):
        trade = self.trade
        trade.end_date = datetime.datetime(2021, 2, 1) # end date before start date; should raise an error
        db.session.add(trade)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_trade_relationships(self):
        trade = self.trade
        db.session.add(trade)
        db.session.commit()
        assert trade in db.session
        assert trade == self.user.trades[0]
        assert trade == self.debit_currency.debit_trades[0]
        assert trade == self.credit_currency.credit_trades[0]

    def test_component_relationships(self):
        portfolio = Portfolio()
        self.user.portfolio = portfolio
        component = Component(
            portfolio = portfolio,
            currency = self.debit_currency,
            amount = random.uniform(0, 1_000_000))
        db.session.add(component)
        db.session.commit()
        assert component in db.session
        assert component == self.user.portfolio.components[0]
        assert component == self.debit_currency.components[0]

if __name__ == '__main__':
    unittest.main()