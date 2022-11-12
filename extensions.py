import requests
import json
from dotenv import load_dotenv, find_dotenv
import os


class API:
    """Gets telegram token from .env"""
    load_dotenv(find_dotenv())
    TOKEN = os.getenv('CURRENCY_BOT_TOKEN')


class APIException(Exception):
    pass


class ConversionException(APIException):
    pass


class ServerException(APIException):
    pass


class Converter:
    """Currency conversion API: https://exchangerate.host/"""

    @classmethod
    def check_server(cls, url: str):
        """Handles server errors"""
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ServerException(f"Error: server issue\n{e}")
        else:
            return r.content

    @classmethod
    def check_input(cls, query: str) -> tuple[str, str, float]:
        """Parses user input, handles input errors"""
        try:
            base, quote, amount = query.split()
            base = base.upper()
            quote = quote.upper()
        except ValueError:
            raise ConversionException("Error: incorrect input\nUsage: /help")

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConversionException(f"Error: incorrect amount ({amount})")

        cur = cls.load_currencies()
        for i in base, quote:
            if i not in cur['symbols'].keys():
                raise ConversionException(f"Error: unknown currency {i}")

        return base, quote, amount

    @classmethod
    def load_currencies(cls, force: bool = False):
        """Downloads and returns a list of supported currencies"""
        file = 'symbols.json'
        url = 'https://api.exchangerate.host/symbols'

        if not os.path.isfile(file) or force:
            response = cls.check_server(url)
            data = json.loads(response)
            with open(file, 'w') as outfile:
                json.dump(data, outfile)
            return data
        else:
            file = open(file)
            return json.load(file)

    @classmethod
    def get_currencies(cls) -> str:
        """Returns a list of currencies"""
        data = cls.load_currencies(force=True)
        text = ""
        for i in data['symbols'].values():
            description = i['description']
            code = i['code']
            text += "".join(f"{code}: {description}\n")
        return text

    @classmethod
    def convert(cls, query: str) -> str:
        """Converts currencies"""
        base, quote, amount = cls.check_input(query)
        url = f"https://api.exchangerate.host/convert?from={base}&to={quote}&amount={amount}&places=2"
        response = cls.check_server(url)
        reply = json.loads(response)
        if reply['info']['rate'] is None:  # this should never happen
            raise ConversionException("Error: unknown currency")

        return f"{amount} {base} = {reply['result']} {quote}"
