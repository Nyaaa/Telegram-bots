import telebot
from extensions import *


bot = telebot.TeleBot(API.TOKEN)
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


@bot.message_handler(commands=['values'])
def message_help(message):
    try:
        bot.send_message(message.chat.id, Converter.get_currencies())
    except APIException as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(content_types=['text'])
def message_convert(message):
    try:
        bot.send_message(message.chat.id, Converter.convert(message.text))
    except APIException as e:
        bot.send_message(message.chat.id, str(e))


bot.infinity_polling()
