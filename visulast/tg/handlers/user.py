import re
from visulast.tg import helpers
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler
from visulast.core import controllers, models
from visulast.tg.handlers import commons, states
from visulast.tg.handlers.general import abort

keyboards = {
    'source': [['My library', 'Specific user library']],
    'subject': [['Artists', 'Albums', 'Tracks'], ['Tags', 'Friends']],
    'amount': [['1', '5', '8', '10'], ['20', '30', '40', 'All (max=50)']],
    'period': [['Overall', 'Week', 'Month'], ['3 Months', '6 Months', '12 Months', 'Custom']],
    'representation': {
        'Artists': [['5x5 covers', '4x4 covers', 'Classic eight', 'World map'],
                    ['Bar diagram', 'Pie diagram', 'Stack diagram', 'Heat map']],
        'Albums': [['5x5 covers', '4x4 covers', 'Classic eight', 'World map'],
                   ['Bar diagram', 'Pie diagram', 'Stack diagram', 'Heat map']],
        'Tracks': [['Bar diagram', 'Pie diagram'], ['Stack diagram', 'Heat map']],
        'Tags': [['Bar diagram', 'Pie diagram'], ['Stack diagram', 'Heat map']],
        'Friends': [['Bar diagram', 'Pie diagram', 'Stack diagram', 'Heat map']],
    },
}

USER_MODEL = None
USER_CONTROLLER = None


def user(update, context):
    if not helpers.is_username_set(context):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="You cannot use this bot if you haven't provided last.fm username.\n"
                 "You can do it with /authenticate *username* command",
            reply_markup=ReplyKeyboardRemove,
            parse_mode=ParseMode.MARKDOWN,

        )
        return states.END

    context.user_data['user'] = {}
    context.user_data['user']['amount'] = 0
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose where from should I gather data",
        reply_markup=ReplyKeyboardMarkup(keyboards['source'])
    )
    return states.USER_SOURCE_SELECTION


def source_selection_response(update, context):
    source = update.message.text

    if source == 'Specific user library':
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Type username or select among your friends",
            reply_markup=helpers.get_friends_keyboard(context.user_data['username'])
        )
        return states.USER_SPECIFIC_USER_TYPING
    elif source == 'My library':
        global USER_MODEL
        USER_MODEL = models.UserModel(context.user_data['username'])
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Choose subject which to draw",
            reply_markup=ReplyKeyboardMarkup(keyboards['subject'])
        )
        return states.USER_SUBJECT_SELECTION


def specific_user_typing_response(update, context):
    source = update.message.text
    global USER_MODEL
    USER_MODEL = models.UserModel(source)
    if USER_MODEL:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Choose subject which to draw",
            reply_markup=ReplyKeyboardMarkup(keyboards['subject'])
        )
        return states.USER_SUBJECT_SELECTION
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Such user doesn't exist, try again or type /abort"
        )


def subject_selection_response(update, context):
    global USER_CONTROLLER
    USER_CONTROLLER = controllers.UserController(USER_MODEL)

    subject = update.message.text
    context.user_data['user']['subject'] = subject

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Now choose period over which I should look up",
        reply_markup=ReplyKeyboardMarkup(keyboards['period'])
    )
    return states.USER_PERIOD_SELECTION


def period_selection_response(update, context):
    period = update.message.text
    if period == 'Custom':
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Select dates between which you want to get info",
            reply_markup=ReplyKeyboardMarkup(keyboards['period'])
        )
        return states.USER_CUSTOM_PERIOD_SELECTION

    context.user_data['user']['period'] = helpers.convert_period_to_var(period)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Now representation style",
        reply_markup=ReplyKeyboardMarkup(keyboards['representation'][context.user_data['user']['subject']])
    )
    return states.USER_REPRESENTATION_SELECTION


def custom_period_selection_response(update, context):
    pass


def representation_selection_response(update, context):
    representation = update.message.text
    context.user_data['user']['representation'] = representation

    if representation in ['5x5 covers', '4x4 covers', 'Classic eight']:
        commons.finish_dialog(update, context, USER_CONTROLLER)
        return states.END

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Now choose amount of subjects to process",
        reply_markup=ReplyKeyboardMarkup(keyboards['amount'])
    )
    return states.USER_AMOUNT_SELECTION


def amount_selection_response(update, context):
    amount = update.message.text
    context.user_data['user']['amount'] = int(re.sub("\D", "", amount))
    commons.finish_dialog(update, context, USER_CONTROLLER)
    return states.END


HANDLERS = {
    ConversationHandler(
        entry_points=[
            CommandHandler('user', user, pass_user_data=True),
        ],
        states={
            states.USER_SOURCE_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['source'])),
                    source_selection_response
                )
            ],
            states.USER_SPECIFIC_USER_TYPING: [
                MessageHandler(
                    Filters.text,
                    specific_user_typing_response
                )
            ],
            states.USER_SUBJECT_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['subject'])),
                    subject_selection_response
                )
            ],
            states.USER_PERIOD_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['period'])),
                    period_selection_response
                )
            ],
            states.USER_CUSTOM_PERIOD_SELECTION: [

            ],
            states.USER_REPRESENTATION_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['representation'])),
                    representation_selection_response
                )
            ],
            states.USER_AMOUNT_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['amount'])),
                    amount_selection_response
                )
            ],
        },
        fallbacks=[
            CommandHandler('abort', abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='user.conversation'
    ),
}
