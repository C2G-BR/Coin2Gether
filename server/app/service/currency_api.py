import requests
import json

from app.config import CURRENCY_API_KEY

# returns the current (realtime) value of one entity of the base currency in quote currency
def get_exchange_rate(base_acronym, quote_acronym):
    try:
        if (base_acronym != quote_acronym):
            CURRENCY_ENDPOINT = 'https://rest.coinapi.io/v1/'
            url = f'{CURRENCY_ENDPOINT}exchangerate/{base_acronym}/{quote_acronym}'
            headers = {'X-CoinAPI-Key' : CURRENCY_API_KEY}
            response = requests.get(url, headers=headers)
            response = response.json()
            return response['rate']
        else:
            return 1 # return 1 to indicate that both currencies are equal
    except:
        return 50 # Value if request fails or available requests are taken