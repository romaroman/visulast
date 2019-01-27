from functools import wraps
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from utils import get_logger
from core import controllers


logger = get_logger(__name__)
SUBJECT_CHOOSING, GRAPH_CHOOSING, PERIOD_CHOOSING = range(3)


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
    reply_markup = ReplyKeyboardMarkup(keyboards['subjects'], one_time_keyboard=True)
    logger.info("At visu")
    bot.send_message(chat_id=update.message.chat_id, text="Choose what to visualize", reply_markup=reply_markup)
    return SUBJECT_CHOOSING


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Bye, bro!")

    user_data.clear()
    return ConversationHandler.END


def visu(bot, update):
    reply_markup = ReplyKeyboardMarkup(keyboards['subjects'], one_time_keyboard=True)
    logger.info("At visu")
    bot.send_message(chat_id=update.message.chat_id, text="Choose what to visualize", reply_markup=reply_markup)
    return SUBJECT_CHOOSING


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
    reply_markup = ReplyKeyboardMarkup(keyboards['period'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose interval", reply_markup=reply_markup)


def graph_selector(bot, update):
    reply_markup = ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose graph style", reply_markup=reply_markup)
    return


def subject_selector(bot, update, user_data):
    user = update.message.from_user
    text = update.message.text
    print(text)
    logger.info("Info %s: %s", user.first_name, update.message.text)
    user_data['choice'] = text
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())
    reply_markup = ReplyKeyboardMarkup(keyboards['period'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose interval", reply_markup=reply_markup)
    return PERIOD_CHOOSING


def custom_period_selector(bot, update):
    raise NotImplemented
# </editor-fold>


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
