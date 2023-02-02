import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class ValueConvector:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertionException('Одинаковые значения')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('Неверно введена Первая валюта')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('Неверно введена Вторая валюта')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Некорректное кол-во')

        r = requests.get(
            f'https://api.exchangerate.host/convert?from={quote_ticker}&to={base_ticker}&amount={amount}')
        d = json.loads(r.content)['result']

        return d
