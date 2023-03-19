import telebot
from telebot import types
import requests
import json
from extensions import Convertor, APIExceptions
from config import *


bot = telebot.TeleBot(TOKEN)


def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for button in currencies.keys():
        if button != base:
            buttons.append(types.KeyboardButton(button.upper()))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Hello, there! Welcome to Telegram Bot converting the currencies!'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = 'Available commands to interact with a Bot are:\n \
See all available currencies: /currencies\n \
Start converting currencies using command: /convert'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for i in currencies.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Choose the currency converting from:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip().upper()
    text = 'Choose the currency converting to:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)


def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Choose the amount to convert:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        price = Convertor.get_price(base, quote, amount)
    except APIExceptions as e:
        bot.send_message(message.chat.id, f'Conversion error:\n{e}')
    else:
        text = f'Price for {amount} {base} to {quote} : {price}'
        bot.send_message(message.chat.id, text)


bot.polling()
