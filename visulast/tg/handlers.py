from functools import wraps
import telegram
from telegram.ext import ConversationHandler

import logger
from core import controllers


logger = logger.get_logger(__name__)
PERIOD_CHOOSING, TYPE_CHOOSING = range(2)


states = {

}

keyboards = {
    'subjects': [['Me', 'User', 'Followers'],
                 ['Artist', 'Album', 'Followings'],
                 ['Country', 'Tag', 'Trends']],
    'periods': [['Today', 'Week', 'Month'],
               ['Quartal', 'Half a year', 'Year'],
               ['5 years', 'Overall', 'Custom']],
    'graphs': [['Histogram', 'Worldmap', 'Flow'],
               ['Pie', 'Bar', 'Line'],
               ['Swarm', 'Hear', 'Cluster']]
}


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)

        return command_func
    return decorator


# <editor-fold desc="Globals">
def start(bot, update):
    update.message.reply_text('Hi! I am your personal last.fm plotter')


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Bye, bro!")

    user_data.clear()
    return ConversationHandler.END


def visu(bot, update):
    raise NotImplemented


def abort(bot, update):
    raise NotImplemented


def guide(bot, update):
    raise NotImplemented


def faq(bot, update):
    raise NotImplemented


def examples(bot, update):
    raise NotImplemented
# </editor-fold>


def set_username(bot, update, args):
    username = " ".join(args)
    update.message.reply_text("You've set default last.fm username to " + username)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# <editor-fold desc="Selectors">
def period_selector(bot, update):
    reply_markup = telegram.ReplyKeyboardMarkup(keyboards['period'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose interval", reply_markup=reply_markup)


def graph_selector(bot, update):
    reply_markup = telegram.ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose graph style", reply_markup=reply_markup)
    return


def subject_selector(bot, update):
    reply_markup = telegram.ReplyKeyboardMarkup(keyboards['subjects'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose what to visualize", reply_markup=reply_markup)


def custom_period_selector(bot, update):
    raise NotImplemented
# </editor-fold>


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
