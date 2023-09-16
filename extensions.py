# extensions.py
import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            return amount

        try:
            url = f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}"
            response = requests.get(url)
            data = json.loads(response.text)

            if quote in data:
                rate = data[quote]
                converted_amount = amount * rate
                return converted_amount
            else:
                raise APIException(f"Курс для валюты '{quote}' не найден в ответе от API.")
        except Exception as e:
            raise APIException(f"Произошла ошибка при конвертации: {str(e)}")
