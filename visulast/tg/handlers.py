from functools import wraps
import pylast
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from utils.helpers import get_logger
from core import controllers
from core.scrappers import lastfm_client


logger = get_logger(__name__)
CHOOSING_SUBJECT = 0
CHOOSING_PERIOD = 1
CHOOSING_GRAPH = 2
NO_JOBS = 3

keyboards = {
    'subjects': [['Myself', 'User', 'Followers'],
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
    return NO_JOBS

def abort(bot, update):
    raise NotImplemented


def guide(bot, update):
    raise NotImplemented


def faq(bot, update):
    raise NotImplemented


def examples(bot, update):
    raise NotImplemented


# TODO: IMPLEMENT THIS
def set_lastfm_username(bot, update, userdata):
    try:
        lastfm_client.get_user(update.message.text)
        userdata['lastfm_username'] = update.message.text
        update.message.reply_text("You've set your last.fm username to " + userdata['lastfm_username'])
        return
    except pylast.WSError:
        update.message.reply_text("Such user doesn't exist try again or use /abort command to cancel")
        return


def done(bot, update, user_data):
    if user_data:
        del user_data
    update.message.reply_text("Bye, bro!")
    user_data.clear()
    return ConversationHandler.END
# </editor-fold>


# <editor-fold desc="Selectors">
def visu(bot, update):
    reply_markup = ReplyKeyboardMarkup(keyboards['subjects'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Okay, choose what subject from last.fm to analyze", reply_markup=reply_markup)
    return CHOOSING_SUBJECT


def subject_choice(bot, update, user_data):
    user_data['subject'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(keyboards['periods'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Nice, over what time you need your stats? (larger date - longer waiting)", reply_markup=reply_markup)
    return CHOOSING_PERIOD


def period_choice(bot, update, user_data):
    user_data['period'] = update.message.text
    update.message.reply_text("Okay, cool, there's left only to choose graph type")
    reply_markup = ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Okay, choose what to analyze", reply_markup=reply_markup)
    return CHOOSING_GRAPH


def custom_period_choice(bot, update, user_data):
    user_data['c_period'] = update.message.text
    update.message.reply_text("Okay, cool, there's left only to choose graph type")
    reply_markup = ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Okay, choose what to analyze", reply_markup=reply_markup)
    return CHOOSING_GRAPH


@send_action(telegram.ChatAction.UPLOAD_PHOTO)
def graph_choice(bot, update, user_data):
    user_data['graph'] = update.message.text
    controller = controllers.UserController('niedego', update.message.chat_id)
    file = controller.scrobbles_world_map(2)
    bot.send_photo(chat_id=update.message.chat_id, caption='Your map bro)',
                   photo=open(file, 'rb'))
    return NO_JOBS

# </editor-fold>


def set0(bot, update):
    return 0


def reset(bot, update):
    return NO_JOBS


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
