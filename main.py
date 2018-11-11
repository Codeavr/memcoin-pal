import telegram
import os
import logging
import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler


updater = Updater(token=os.environ['TOKEN'])
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
balance_handler = CommandHandler('balance', balance)
dispatcher.add_handler(start_handler)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

api_url = os.environ['APIURL']

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm memcoin pal bot, send /balance to see your balance")

def balance(bot, update):
    response = requests.get(api_url + 'user/' + update.message.chat_id).text
    bot.send_message(chat_id=update.message.chat_id, text=response)