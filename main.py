import telegram
import os
import logging
import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm memcoin pal bot, send /balance to see your balance")

def balance(bot, update):
    response = requests.get(api_url + '/user/' + str(update.message.chat_id)).text
    bot.send_message(chat_id=update.message.chat_id, text=response)

def register_command(dispatcher, command, method):
    handler = CommandHandler(command, method)
    dispatcher.add_handler(handler)

api_url = os.environ['APIURL']
updater = Updater(token=os.environ['TOKEN'])
dispatcher = updater.dispatcher

register_command(dispatcher, 'start', start)
register_command(dispatcher, 'balance', balance)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling()