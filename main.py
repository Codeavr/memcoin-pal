import telegram
import os
import logging
import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler

api_url = os.environ['APIURL']
mem_token = os.environ['MEMTOKEN']
tg_token = os.environ['TOKEN']

headers = {'token': mem_token }

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm memcoin pal bot, send /balance to see your balance")

def balance(bot, update):
    response = requests.get(api_url + '/user/' + str(update.message.chat_id), headers=headers).text
    bot.send_message(chat_id=update.message.chat_id, text=response)

def transfer(bot, update, args):
    if len(args) != 2:
        answer(bot, update, 'I don\'t understand you, boye')
    else:
        payload = {'senderId': update.message.chat_id, 'receiverId': args[0], 'amount': args[1] }
        response = requests.post(api_url + '/transfer/' + str(update.message.chat_id), data=payload, headers=headers).text
        bot.send_message(chat_id=update.message.chat_id, text=response)

def answer(bot, context, msg):
    bot.send_message(chat_id=context.message.chat_id, text=msg)

def register_command(dispatcher, command, method, pass_args=False):
    handler = CommandHandler(command, method, pass_args=pass_args)
    dispatcher.add_handler(handler)

updater = Updater(token=tg_token)
dispatcher = updater.dispatcher

register_command(dispatcher, 'start', start)
register_command(dispatcher, 'balance', balance)
register_command(dispatcher, 'transfer', transfer, pass_args=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling()