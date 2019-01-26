import os
import telegram

from telegram.ext import Updater, CommandHandler
from config import CONFIGURATION
from logger import get_logger
import controllers
from functools import wraps


logger = get_logger(os.path.basename(__file__))

updater = Updater(token=CONFIGURATION.telegram_bot)
dispatcher = updater.dispatcher


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)

        return command_func

    return decorator


send_upload_photo_action = send_action(telegram.ChatAction.UPLOAD_PHOTO)


@send_action(telegram.ChatAction.UPLOAD_PHOTO)
def artists(bot, update, args):
    # bot.send_message(chat_id=update.message.chat_id, text='Wait, I\'m processing your request')
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


def period_keyboard(bot, update):
    custom_keyboard = [['today', 'week', 'month'],
                       ['quartal', 'half of year', 'year'],
                       ['overall', 'custom']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)


artists_handler = CommandHandler('artists', artists, pass_args=True)
dispatcher.add_handler(artists_handler)

default_username_handler = CommandHandler('default_username', default_username, pass_args=True)
dispatcher.add_handler(default_username_handler)

keyboard_handler = CommandHandler('keyboard', period_keyboard)
dispatcher.add_handler(keyboard_handler)

updater.start_polling()
