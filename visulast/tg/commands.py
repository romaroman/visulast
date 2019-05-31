from functools import wraps
import pylast
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from visulast.utils.helpers import get_logger
from visulast.core import controllers
from visulast.core.scrappers import lastfm_client
from visulast.config import Configuration


logger = get_logger(__name__)

CHOOSING_SUBJECT_TYPE, CHOOSING_USER_SUBJECT, CHOOSING_LASTFM_SUBJECT, CHOOSING_PERIOD, CHOOSING_GRAPH, CHOOSING_HOW, CONFIRMATION = range(7)


remove_keyboard = telegram.ReplyKeyboardRemove()
keyboards = {
    'subject_types': [['Based on user library'], ['General last.fm domain data']],
    'user_subjects': [['My library', 'My followers', 'My following']],
    'lastfm_subjects': [['Artist', 'Album', 'Trends']],
    'periods': [['Today', 'Week', 'Month', 'Quartal'],
                ['Half a year', 'Year', 'Overall']],
    'graphs': [['Histogram', 'Worldmap', 'Flow'],
               ['Pie', 'Bar', 'Line'],
               ['Swarm', 'Hear', 'Cluster']],
    # 'how': [['Photo', 'File', 'Share Link', 'Telegram Link']]
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


# <editor-fold desc="Essentials">
def abort(bot, update, user_data):
    if user_data:
        del user_data
    user_data.clear()
    bot.send_message(chat_id=update.message.chat_id, text="Current conversation is aborted", reply_markup=remove_keyboard)
    return ConversationHandler.END


def clean(bot, update, user_data):
    if user_data:
        del user_data
    user_data.clear()
    update.message.reply_text("Your data is wiped")


def faq(bot, update):
    logger.info("Sent FAQ")
    raise NotImplemented


def authorize(bot, update, userdata):
    raise NotImplemented


def authenticate(bot, update, userdata):
    try:
        lastfm_client.get_user(update.message.text)
        userdata['lastfm_username'] = update.message.text
        update.message.reply_text("You've set your last.fm username to " + userdata['lastfm_username'])
        return
    except pylast.WSError:
        update.message.reply_text("Such user doesn't exist try again or use /abort command to cancel")
        return


def help(bot, update, userdata):
    raise NotImplemented


def cancel(bot, update, userdata):
    return ConversationHandler.END


def report(bot, update):
    update.message.reply_text("Your report message was delivered to maintainer")
    bot.send_message(chat_id=Configuration().developerTelegramID, text=update.message.text)


def donate(bot, update, userdata):
    raise NotImplemented
# </editor-fold>


# <editor-fold desc="Main conversation">
def visualize(bot, update, user_data):
    reply_markup = ReplyKeyboardMarkup(keyboards['subject_types'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Okay, choose what kind of subject to analyze", reply_markup=reply_markup)
    return CHOOSING_SUBJECT_TYPE


def subject_type_choosing(bot, update, user_data):
    subject_type = update.message.text
    user_data['subject'] = update.message.text
    reply_message = f"Okay, type is {subject_type}. Now choose the real subject of this type"
    if subject_type == keyboards['subject_types'][0][0]:
        reply_markup = ReplyKeyboardMarkup(keyboards['user_subjects'], one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return CHOOSING_USER_SUBJECT
    elif subject_type is keyboards['subject_types'][1][0]:
        reply_markup = ReplyKeyboardMarkup(keyboards['lastfm_subjects'], one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return CHOOSING_LASTFM_SUBJECT


def lastfm_subject_choosing(bot, update, user_data):
    lastfm_subject = update.message.text
    user_data['lastfm_subject'] = update.message.text
    reply_message = f"Okay, last.fm subject is {lastfm_subject}. Now choose among what days should I look up"

    reply_markup = ReplyKeyboardMarkup(keyboards['periods'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return CHOOSING_PERIOD


def user_subject_choosing(bot, update, user_data):
    user_subject = update.message.text
    user_data['user_subject'] = update.message.text
    reply_message = f"Okay, user subject is {user_subject}. Now choose among what days should I look up"

    reply_markup = ReplyKeyboardMarkup(keyboards['periods'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return CHOOSING_PERIOD


def period_choosing(bot, update, user_data):
    period = update.message.text
    user_data['period'] = period
    reply_message = f"Okay, period is {period}. There's left only to choose graph type"

    reply_markup = ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return CHOOSING_GRAPH


@send_action(telegram.ChatAction.UPLOAD_PHOTO)
def graph_choosing(bot, update, user_data):
    graph = update.message.text
    user_data['graph'] = graph
    reply_message = f"Everything is okay, graph type is {graph}. Wait for a moment untill I'll finish generating image"

    bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=remove_keyboard)

    controller = controllers.UserController('niedego', update.message.chat_id)
    file = controller.scrobbles_world_map(2)

    bot.send_photo(chat_id=update.message.chat_id, caption=f'Enjoy this {graph.lower()}', photo=open(file, 'rb'))

    return ConversationHandler.END


def wrong_response(bot, update, user_data):
    raise NotImplemented

# </editor-fold>


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
