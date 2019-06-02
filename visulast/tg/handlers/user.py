from visulast.tg import states
from visulast.tg import helpers
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CommandHandler
from visulast.core import scrappers, controllers, models, tools as core_helpers
from visulast.tg.handlers.general import abort

keyboards = {
    'source': [['My library', 'Specific user library']],
    'subject': [['Artists', 'Albums', 'Tracks', 'Tags']],
    'amount': [['5', '10', '20', 'All (max=30)']],
    'period': [['Overall', 'Week', 'Month'], ['3 Months', '6 Months', '12 Months']],
    'representation': {
        'Artists': [['Classic 8 view', 'Bar chart', 'Pie chart']],
        'Albums': [['Classic 8 view', 'Bar chart', 'Pie chart']],
        'Tracks': [['Bar chart', 'Pie chart']],
        'Tags': [['Bar chart', 'Pie chart']],
    }
}

USER_MODEL = None


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
            reply_markup=ReplyKeyboardMarkup(keyboards['source'])
        )
        return states.USER_SPECIFIC_USER_TYPING
    elif source == 'My library':
        global USER_MODEL
        USER_MODEL = models.UserModel(context.user_data['username'])
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Choose where from should I gather data",
            reply_markup=ReplyKeyboardMarkup(keyboards['source'])
        )


def specific_user_typing_response(update, context):
    pass


def subject_selection_response(update, context):
    pass


def period_selection_response(update, context):
    pass


def custom_period_selection_response(update, context):
    pass


def amount_selection_response(update, context):
    pass


def representation_selection_response(update, context):
    pass


HANDLERS = {
    ConversationHandler(
        entry_points=[
            CommandHandler('user', user, pass_user_data=True),
        ],
        states={
            states.USER_SOURCE_SELECTION: [
                MessageHandler(Filters.regex(helpers.keyboard_to_regex(keyboards['source'])), source_selection_response)
            ],
            states.USER_SPECIFIC_USER_TYPING: [

            ],
            states.USER_SUBJECT_SELECTION: [

            ],
            states.USER_PERIOD_SELECTION: [

            ],
            states.USER_CUSTOM_PERIOD_SELECTION: [

            ],
            states.USER_AMOUNT_SELECTION: [

            ],
            states.USER_REPRESENTATION_SELECTION: [

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
