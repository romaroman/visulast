import os

from telegram.ext import Updater, CommandHandler

from config import CONFIGURATION
from logger import get_logger
from drawers import ArtistDrawer
from scrappers import ArtistCountryScrapper


logger = get_logger(os.path.basename(__file__))

updater = Updater(token=CONFIGURATION.telegram_bot)
dispatcher = updater.dispatcher


def countries(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Wait until bot will finish your request")
    countries = ArtistCountryScrapper.get_all_by_username('niedego', 1)
    file = ArtistDrawer.draw_countries(countries)
    bot.send_photo(chat_id=update.message.chat_id, caption='shiiit', photo=open(file, 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="Sending photo!")


start_handler = CommandHandler('countries', countries)
dispatcher.add_handler(start_handler)

updater.start_polling()
