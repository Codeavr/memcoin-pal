import logging
from config import Config
from telegram.ext import Updater
from telegram.ext import CommandHandler
from memcoin_api import MemcoinAPI

config = Config()

api_url = config['APIURL']
mem_token = config['MEMTOKEN']
tg_token = config['TOKEN']
use_proxy = bool(config['USE_PROXY'])
if use_proxy: 
    proxy = config['PROXY']

api = MemcoinAPI(api_url, mem_token)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm memcoin pal bot, send /balance to see your balance")

def balance(bot, update):
    response = api.get_user(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=response)

def transfer(bot, update, args):
    if len(args) != 2:
        answer(bot, update, 'I don\'t understand yu, boye')
    else:
        response = api.transfer(sender_id=update.message.chat_id, receiver_id=args[0], amount=args[1])
        bot.send_message(chat_id=update.message.chat_id, text=response)

def answer(bot, context, msg):
    bot.send_message(chat_id=context.message.chat_id, text=msg)

def register_command(dispatcher, command, method, pass_args=False):
    handler = CommandHandler(command, method, pass_args=pass_args)
    dispatcher.add_handler(handler)

if use_proxy:
    updater = Updater(token=tg_token, request_kwargs={ 'proxy_url': proxy })
else:
    updater = Updater(token=tg_token)

dispatcher = updater.dispatcher

register_command(dispatcher, 'start', start)
register_command(dispatcher, 'balance', balance)
register_command(dispatcher, 'transfer', transfer, pass_args=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling()