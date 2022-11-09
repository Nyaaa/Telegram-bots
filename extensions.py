import requests
import json
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())  # TODO error handling
TOKEN = os.getenv('CURRENCY_BOT_TOKEN')


class APIException(Exception):
    pass


class ConversionException(APIException):
    pass


class ServerException(APIException):
    pass


class Converter:
    @staticmethod
    def convert(values):
        if len(values) == 3:
            base, quote, amount = values
        else:
            raise ConversionException("Error: incorrect input\nUsage: /help")

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConversionException(f"Error: incorrect amount ({amount})")

        url = f'https://api.exchangerate.host/convert?from={base}&to={quote}&amount={amount}&places=2'

        try:
            get = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ServerException(f"Error: server issue\n{e}")  # TODO test this

        reply = json.loads(get.content)
        if reply["info"]["rate"] is None:  # TODO check json parsing
            raise ConversionException("Error: unknown currency")

        return f'{reply["query"]["amount"]} {reply["query"]["from"]} = {reply["result"]} {reply["query"]["to"]}'
