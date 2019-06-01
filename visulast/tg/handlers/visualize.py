from functools import wraps
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from visulast.utils.helpers import get_logger
from visulast.core import controllers
import visulast.tg.states as states
from visulast.tg.keyboards import visualize as keyboard

logger = get_logger(__name__)


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
    reply_markup = ReplyKeyboardMarkup(keyboard['subject_types'], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Okay, choose what kind of subject to analyze", reply_markup=reply_markup
    )
    return states.CHOOSING_SUBJECT_TYPE


def subject_type_choosing(update, context):
    subject_type = update.message.text
    context.user_data['subject'] = update.message.text
    reply_message = generate_reply_message('type', subject_type, 'real subject')

    if subject_type == keyboard['subject_types'][0][0]:
        reply_markup = ReplyKeyboardMarkup(keyboard['user_subjects'], one_time_keyboard=True)
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return states.CHOOSING_USER_SUBJECT

    elif subject_type is keyboard['subject_types'][1][0]:
        reply_markup = ReplyKeyboardMarkup(keyboard['lastfm_subjects'], one_time_keyboard=True)
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)
        return states.CHOOSING_LASTFM_SUBJECT


def lastfm_subject_choosing(update, context):
    lastfm_subject = update.message.text
    context.user_data['lastfm_subject'] = update.message.text
    reply_message = generate_reply_message('last.fm subject', lastfm_subject, 'period')

    reply_markup = ReplyKeyboardMarkup(keyboard['periods'], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return states.CHOOSING_PERIOD


def user_subject_choosing(update, context):
    user_subject = update.message.text
    context.user_data['user_subject'] = update.message.text
    reply_message = generate_reply_message('user subject', user_subject, 'period')

    reply_markup = ReplyKeyboardMarkup(keyboard['periods'], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_message, reply_markup=reply_markup)

    return states.CHOOSING_PERIOD


def period_choosing(update, context):
    period = update.message.text
    context.user_data['period'] = period
    reply_message = generate_reply_message('period', period, 'graph')

    reply_markup = ReplyKeyboardMarkup(keyboard['graphs'], one_time_keyboard=True)
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
