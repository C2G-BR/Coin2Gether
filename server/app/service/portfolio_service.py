from flask import abort

from app import db
from app.service.auth_service import get_user_from_token
from app.service.currency_api import get_exchange_rate
from app.model.portfolio import Portfolio
from app.model.component import Component
from app.model.currency import Currency
from app.model.user import User


def get_portfolio_by_token(token):
    user = get_user_from_token(token)
    if (user == None):
        abort(403, 'User Not Found')
    return _get_portfolio_by_user(user)

def get_portfolio_by_user_id_currency(user_id):
    STANDARD_CURRENCY = Currency.query.filter_by(acronym='USD').first()
    user = User.query.filter_by(user_id=user_id).first()
    if (user == None):
        abort(404, 'User Not Found')
    portfolio = _get_portfolio_by_user(user)
    for component in portfolio.components:
        component.amount = float(component.amount) * float(get_exchange_rate(component.currency.acronym, STANDARD_CURRENCY.acronym))
    return portfolio

def _get_portfolio_by_user(user):
    if (user.portfolio):
        return user.portfolio
    else:
        return _create_portfolio(user)
    
def create_update_portfolio_by_token(token, components):
    user = get_user_from_token(token)
    if (user == None):
        abort(403, 'User Not Found')
    try:
        if (user.portfolio == None):
            portfolio = _create_portfolio(user)
        else:
            portfolio = user.portfolio
        Component.query.filter_by(portfolio_name = portfolio.name, portfolio_user_id = portfolio.user_id).delete()
        for component in components:
            db.session.add(
                _create_component(component, portfolio)
            )

        save_changes(portfolio)
    except Exception as e:
        db.session.rollback()
        abort(400, 'Invalid data')

    response_object = {
        'status': 'success',
        'message': 'Successfully created'
    }
    return response_object, 201

def _create_portfolio(user):
    portfolio = Portfolio(
        user_id = user.user_id
    )
    save_changes(portfolio)
    return portfolio

def _filter_component_by_id(components, id):
    return next(filter(lambda x: x.currency_id == id, components), None)

def _create_component(component, portfolio):
    component = Component(
        currency = Currency.query.filter_by(currency_id = component['currency_id']).first(),
        portfolio = portfolio,
        amount = component['amount']
    )
    return component

def delete(data):
    db.session.delete(data)
    db.session.commit()

def save_changes(data):
    db.session.add(data)
    db.session.commit()