import os

from telegram.ext import Updater, CommandHandler
from config import CONFIGURATION
from logger import get_logger
import controllers


logger = get_logger(os.path.basename(__file__))

updater = Updater(token=CONFIGURATION.telegram_bot)
dispatcher = updater.dispatcher


def countries(bot, update, args):
    lastfm_username = " ".join(args)
    controller = controllers.UserController(lastfm_username, update.message.chat_id)
    bot.send_photo(chat_id=update.message.chat_id, caption='Your map bro)',
                   photo=open(controller.scrobbles_world_map(2), 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="Sending photo!")


def default_username(bot, update, args):
    username = " ".join(args)
    update.message.reply_text("You've set default last.fm username to " + username)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


countries_handler = CommandHandler('countries', countries, pass_args=True)
dispatcher.add_handler(countries_handler)

default_username_handler = CommandHandler('default_username', default_username, pass_args=True)
dispatcher.add_handler(default_username_handler)

updater.start_polling()
