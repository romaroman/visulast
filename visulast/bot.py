import os

from telegram.ext import Updater, CommandHandler
from config import CONFIGURATION
from logger import get_logger
import controllers


logger = get_logger(os.path.basename(__file__))

updater = Updater(token=CONFIGURATION.telegram_bot)
dispatcher = updater.dispatcher


def artists(bot, update, args):
    controller = controllers.UserController(args[0], update.message.chat_id)
    if args[1] == 'scrobbles':
        file = controller.scrobbles_world_map(args[2])
    if args[1] == 'amount':
        file = controller.artist_amount_world_map(int(args[2]))
    bot.send_photo(chat_id=update.message.chat_id, caption='Your map bro)',
                   photo=open(file, 'rb'))
    # bot.send_message(chat_id=update.message.chat_id, text="Sending photo!")


def default_username(bot, update, args):
    username = " ".join(args)
    update.message.reply_text("You've set default last.fm username to " + username)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


artists_handler = CommandHandler('artists', artists, pass_args=True)
dispatcher.add_handler(artists_handler)

default_username_handler = CommandHandler('default_username', default_username, pass_args=True)
dispatcher.add_handler(default_username_handler)

updater.start_polling()
