from flask import abort

from app.model.currency import Currency
from app.model.user import User
from app.service.auth_service import get_user_from_token


def get_all_currencies():
    return Currency.query.all()

def get_currency_by_id(currency_id: int):
    currency = Currency.query.filter_by(currency_id=currency_id).first()
    if not currency:
        abort(404, 'Currency Not Found')
    else:
        return currency

def get_currency_by_user(token):
    user = get_user_from_token(token)
    if (user == None):
        abort(403, 'Not Authorized')
    currencies = []
    try:
        components = user.portfolio.components
        if (components != None):
            for component in components:
                currencies.append(component.currency)
    except:
        currencies = []
    return currencies