import requests
import json
import os
import telebot
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())


@dataclass(frozen=True)
class API:
    bot_name: str = os.getenv('CURRENCY_BOT')
    bot_token: str = os.getenv('CURRENCY_API_TOKEN')


bot = telebot.TeleBot(API.bot_token)


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.reply_to(message, "start message")


@bot.message_handler(commands=['help'])
def message_help(message):
    bot.reply_to(message, "help message")


@bot.message_handler(func=lambda message: True)
def message_convert(message):
    base, to, amount = message.text.split()
    url = f'https://api.exchangerate.host/convert?from={base}&to={to}&amount={amount}'
    bot.reply_to(message, f'{base}, {to}, {amount}')


bot.infinity_polling()
