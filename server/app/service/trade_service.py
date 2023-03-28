from flask import abort
import datetime
from sqlalchemy import text
from app import db
from app.model.trade import Trade
from app.model.component import Component
from app.model.user import User, followers
from app.service.currency_service import get_currency_by_id
from app.service.user_service import get_user_by_id
from app.service.auth_service import get_user_from_token
from app.service.currency_api import get_exchange_rate

def post_new_trade(data, token):

    author = get_user_from_token(token)
    if (author == None):
        abort(403, 'User Not Found')
    exchange_amount = data['percentage_trade']
    if (exchange_amount > 100 or exchange_amount < 0):
        abort(400, 'You cannot trade more than what you have or less than nothing.')
    debit_currency = get_currency_by_id(data['debit_currency_id'])
    credit_currency = get_currency_by_id(data['credit_currency_id'])

    components = author.portfolio.components
    credit_component = _filter_component_by_id(components, credit_currency.currency_id)
    debit_component = _filter_component_by_id(components, debit_currency.currency_id)

    if (credit_component == None):
        abort(400, 'Credit currency not in portfolio.')
    credit_amount = float(credit_component.amount) * float(exchange_amount/100)
    exchange_rate = get_exchange_rate(credit_currency.acronym, debit_currency.acronym)
    debit_amount = exchange_rate * float(credit_amount)

    if (credit_amount <= 0 or debit_amount <= 0):
        abort(500, 'Amounts to small.')

    try:
        if (debit_component == None):
            debit_component = Component(
                portfolio = author.portfolio,
                currency = debit_currency,
                amount = debit_amount
            )
        else:
            debit_component.amount = debit_amount
        
        new_trade = Trade(
            publish_date=datetime.datetime.utcnow(),
            start_date=datetime.datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date=datetime.datetime.strptime(data['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            motivation=data['motivation'],
            description=data['description'],
            expected_change=data['expected_change'],
            percentage_trade=exchange_amount,
            author=author,
            debit_currency=debit_currency,
            debit_amount=debit_amount,
            credit_currency=credit_currency,
            credit_amount=credit_amount,
        )

        if (exchange_amount == 100):
            db.session.delete(credit_component) # delete credit component since amount is 0
        else:
            credit_component.amount = float(credit_component.amount) - float(credit_amount)
            db.session.add(credit_component)

        db.session.add(debit_component)
        db.session.add(new_trade)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, 'Invalid data')

    response_object = {
        'status': 'success',
        'message': 'Successfully created'
    }
    return response_object, 201

def _filter_component_by_id(components, id):
    return next(filter(lambda x: x.currency_id == id, components), None)

def get_all_trades():
    last_trades = text("SELECT * FROM last_10_trades;")
    with db.engine.connect() as connection:
        result = db.engine.execute(last_trades)
        trades = []
        for row in result:
            trade = get_trade_by_id(trade_id=row[0])
            trades.append(trade)
    return trades

def get_followed_trades(token):
    user = get_user_from_token(token)
    return Trade.query.join(
        followers, (followers.c.followed_id == Trade.author_id)).filter(
            followers.c.follower_id == user.user_id).order_by(
                Trade.publish_date.desc()).all()

def get_trades_by_author(author_name):
    trades = Trade.query.join(Trade.author, aliased=True).filter_by(username=author_name).all()
    if not trades:
        return []
    else:
        return trades

def get_trade_by_id(trade_id: int):
    trade = Trade.query.filter_by(trade_id=trade_id).first()
    if not trade:
        abort(404, 'Trade Not Found')
    else:
        return trade

def save_changes(data):
    db.session.add(data)
    db.session.commit()