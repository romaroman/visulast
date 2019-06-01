from functools import wraps
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler

import visulast.tg.helpers
from visulast.tg.handlers.general import abort
from visulast.utils.helpers import get_logger
from visulast.core import controllers
import visulast.tg.states as states


logger = get_logger(__name__)

keyboards = {
    'subject_types': [['Based on user library'], ['General last.fm domain data']],

    'user_subjects': [['My library', 'My followers', 'My following']],

    'lastfm_subjects': [['Artist', 'Album', 'Trends']],

    'periods': [['Today', 'Week', 'Month', 'Quarter'],
                ['Half a year', 'Year', 'Overall']],

    'graphs': [['Histogram', 'Worldmap', 'Flow'],
               ['Pie', 'Bar', 'Line'],
               ['Swarm', 'Hear', 'Cluster']],

    'how': [['Photo', 'File', 'Share Link', 'Telegram Link']]
}


def generate_reply_message(item, choice, next_item):
    return f"Okay, {item} is {choice.lower()}. Now choose {next_item}:"


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            update, context = args
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, **kwargs)

        return command_func

    return decorator


def visualize(update, context):
    reply_markup = ReplyKeyboardMarkup(keyboards['subject_types'], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Okay, choose what kind of subject to analyze", reply_markup=reply_markup
    )
    return states.CHOOSING_SUBJECT_TYPE


def subject_type_choosing(update, context):
    subject_type = update.message.text
    context.user_data['subject'] = update.message.text
    reply_message = generate_reply_message('type', subject_type, 'real subject')

    if subject_type == keyboards['subject_types'][0][0]:
        reply_markup = ReplyKeyboardMarkup(keyboards['user_subjects'], one_time_keyboard=True)
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return states.CHOOSING_USER_SUBJECT

    elif subject_type is keyboards['subject_types'][1][0]:
        reply_markup = ReplyKeyboardMarkup(keyboards['lastfm_subjects'], one_time_keyboard=True)
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return states.CHOOSING_LASTFM_SUBJECT


def lastfm_subject_choosing(update, context):
    lastfm_subject = update.message.text
    context.user_data['lastfm_subject'] = update.message.text
    reply_message = generate_reply_message('last.fm subject', lastfm_subject, 'period')

    reply_markup = ReplyKeyboardMarkup(keyboards['periods'], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return states.CHOOSING_PERIOD


def user_subject_choosing(update, context):
    user_subject = update.message.text
    context.user_data['user_subject'] = update.message.text
    reply_message = generate_reply_message('user subject', user_subject, 'period')

    reply_markup = ReplyKeyboardMarkup(keyboards['periods'], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return states.CHOOSING_PERIOD


def period_choosing(update, context):
    period = update.message.text
    context.user_data['period'] = period
    reply_message = generate_reply_message('period', period, 'graph')

    reply_markup = ReplyKeyboardMarkup(keyboards['graphs'], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return states.CHOOSING_GRAPH


@send_action(telegram.ChatAction.UPLOAD_PHOTO)
def graph_choosing(update, context):
    graph = update.message.text
    context.user_data['graph'] = graph
    reply_message = f"Everything is okay, graph type is {graph.lower()}." \
        f" Wait for a moment untill I'll finish generating image"

    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=ReplyKeyboardRemove())

    controller = controllers.UserController('niedego', update.message.chat_id)
    file = controller.scrobbles_world_map(2)

    context.bot.send_photo(chat_id=update.message.chat_id, caption=f'Enjoy this {graph.lower()}',
                           photo=open(file, 'rb'))

    return states.END


# TODO: implement wrong choice saving state
def wrong_response(update, context):
    raise NotImplemented


HANDLERS = [
    ConversationHandler(
        entry_points=[
            CommandHandler('visualize', visualize, pass_user_data=True),
        ],
        states={
            states.CHOOSING_SUBJECT_TYPE: [
                MessageHandler(Filters.regex(f"^({visulast.tg.helpers.keyboard_to_regex(keyboards['subject_types'])})$"),
                               subject_type_choosing, pass_user_data=True)
            ],
            states.CHOOSING_USER_SUBJECT: [
                MessageHandler(Filters.regex(f"^({visulast.tg.helpers.keyboard_to_regex(keyboards['user_subjects'])})$"),
                               user_subject_choosing, pass_user_data=True)
            ],
            states.CHOOSING_LASTFM_SUBJECT: [
                MessageHandler(Filters.regex(f"^({visulast.tg.helpers.keyboard_to_regex(keyboards['lastfm_subjects'])})$"),
                               lastfm_subject_choosing, pass_user_data=True)
            ],
            states.CHOOSING_HOW_MUCH: [

            ],
            states.CHOOSING_PERIOD: [
                MessageHandler(Filters.regex(f"^({visulast.tg.helpers.keyboard_to_regex(keyboards['periods'])})$"),
                               period_choosing, pass_user_data=True),
            ],
            states.CHOOSING_GRAPH: [
                MessageHandler(Filters.regex(f"^({visulast.tg.helpers.keyboard_to_regex(keyboards['graphs'])})$"),
                               graph_choosing, pass_user_data=True),
            ],
            states.CONFIRMATION: [

            ],
        },
        fallbacks=[
            CommandHandler('abort', abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='visualize.conversation'
    ),
]