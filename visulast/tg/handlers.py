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
    'period': [['Today', 'Week', 'Month'],
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


# global commands
def start(bot, update):
    update.message.reply_text('Hi! I am your personal last.fm plotter')


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Bye, bro!")

    user_data.clear()
    return ConversationHandler.END


def visu(bot, update):
    pass


def abort(bot, update):
    pass


def guide(bot, update):
    pass


def faq(bot, update):
    pass


def examples(bot, update):
    pass


# @send_action(telegram.ChatAction.UPLOAD_PHOTO)
def artists(bot, update, args):
    # controller = controllers.UserController(args[0], update.message.chat_id)
    # file = controller.scrobbles_world_map(1)
    # bot.send_photo(chat_id=update.message.chat_id, caption='Your map bro)',
    #                photo=open(file, 'rb'))
    return PERIOD_CHOOSING
    # bot.send_message(chat_id=update.message.chat_id, text="Sending photo!")


def set_username(bot, update, args):
    username = " ".join(args)
    update.message.reply_text("You've set default last.fm username to " + username)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# selectors
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

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
