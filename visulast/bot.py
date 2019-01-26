import os
import telegram

from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler
from config import CONFIGURATION
from logger import get_logger
import controllers
from functools import wraps


logger = get_logger(os.path.basename(__file__))

PERIOD = 1


# noinspection PyUnusedLocal
def start(bot, update):
    update.message.reply_text('Hi! I am your personal last.fm plotter')


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)

        return command_func
    return decorator


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
    return PERIOD
    # bot.send_message(chat_id=update.message.chat_id, text="Sending photo!")


def default_username(bot, update, args):
    username = " ".join(args)
    update.message.reply_text("You've set default last.fm username to " + username)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


def period(bot, update):
    custom_keyboard = [['today', 'week', 'month'],
                       ['quartal', 'half of year', 'year'],
                       ['overall', 'custom']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose interval", reply_markup=reply_markup)


def main():
    updater = Updater(token=CONFIGURATION.telegram_bot)
    dispatcher = updater.dispatcher

    handlers = [
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                PERIOD: [RegexHandler('^(Day|Week|Month|Quarter|Half a year|Year|Overall|Custom$', period)]
            }
        ),
        CommandHandler('artists', artists, pass_args=True),
        CommandHandler('default_username', default_username, pass_args=True),
    ]
    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
