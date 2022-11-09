import requests
import json
import telebot
from extensions import *
# TODO add async


bot = telebot.TeleBot(TOKEN)
cmd_help = telebot.types.BotCommand("help", "Bot usage")
cmd_start = telebot.types.BotCommand("start", "Bot info")
cmd_values = telebot.types.BotCommand("values", "Supported currencies")
bot.set_my_commands(commands=[cmd_start, cmd_help, cmd_values])


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, "Welcome to currency converter bot!\n"
                                      "Usage: /help\n"
                                      "Supported currencies: /values")


@bot.message_handler(commands=['help'])
def message_help(message):
    bot.send_message(message.chat.id, "Usage:\n"
                                      "[currency to convert from] [currency to convert to] [amount]\n"
                                      "Example: usd eur 100\n"
                                      "Supported currencies: /values")


@bot.message_handler(commands=['values'])  # TODO move this
def message_help(message):
    url = 'https://api.exchangerate.host/symbols'
    response = requests.get(url)
    data = json.loads(response.content)
    text = ""
    for i in data['symbols'].values():
        description = i["description"]
        code = i["code"]
        text += "".join(f'{code}: {description}\n')
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def message_convert(message):
    values = message.text.split()
    try:
        text = Converter.convert(values)
    except APIException as e:
        bot.send_message(message.chat.id, f'{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.infinity_polling()
