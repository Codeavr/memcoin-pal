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

def start_command(bot, update):
    msg = [
        "Hello, I'm memcoin pal bot",
        "I can manage memcoins for you",
        "Type /balance to see your balance",
        "Type /id to get your payment id",
        "Use '/transfer [id] [amount]' to transfer memcoins to user"
    ]
    answer(bot, update, '\n'.join(msg))

def balance_command(bot, update):
    response = api.get_user(str(update.message.chat_id))
    if response.success:
        answer(bot, update, f"Your balance: {response.json['balance']}")
    else:
        answer(bot, update, 'Something went, wrong..')

def transfer_command(bot, update, args):    
    if len(args) != 2:
        answer(bot, update, 'I don\'t understand yu, boye')
    else:
        response = api.transfer(sender_id=update.message.chat_id, receiver_id=args[0], amount=args[1])
        if response.success:
            answer(bot, update, f'Successfully transfered {args[1]} coins')
        elif response.error == 'NotEnoughCoinsError':
            answer(bot, update, 'Not enough coins for transfer')
        elif response.error == 'SendSelfError':
            answer(bot, update, 'Can\'t transfer coins to yourself')

def id_command(bot, update):
    answer(bot, update, f"Your id is '{update.message.chat_id}'")

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

register_command(dispatcher, 'start', start_command)
register_command(dispatcher, 'balance', balance_command)
register_command(dispatcher, 'transfer', transfer_command, pass_args=True)
register_command(dispatcher, 'id', id_command)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling()