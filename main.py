import telegram
import os
bot = telegram.Bot(token=os.environ['TOKEN'])
print(bot.get_me())
