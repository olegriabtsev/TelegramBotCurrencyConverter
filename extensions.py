import requests
import json
from config import currencies


class APIExceptions(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = currencies[base.lower()]
        except KeyError:
            raise APIExceptions(f'Currency {base} not found!')
        try:
            quote_key = currencies[quote.lower()]
        except KeyError:
            raise APIExceptions(f'Currency {quote} not found!')

        if base_key == quote_key:
            raise APIExceptions(f'Not possible to convert the same currency {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIExceptions(f"Couldn't process amount of {amount}, try again.")

        url = f"https://api.apilayer.com/currency_data/convert?to={quote_key}&from={base_key}&amount={amount}"
        payload = {}
        headers = {
            "apikey": "hVhMovZolF6ZYIw9YMOAi3RVke4DRncR"
        }
        response = requests.get(url, headers=headers, data=payload)
        result = response.json()
        price = result['result']
        return round(price, 2)
