import re
from visulast.tg import states
from visulast.tg import helpers
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CommandHandler
from visulast.core import controllers, models
from visulast.tg.handlers.general import abort

keyboards = {
    'source': [['My library', 'Specific user library']],
    'subject': [['Artists', 'Albums', 'Tracks', 'Tags', 'Friends']],
    'amount': [['1', '5', '8', '10'], ['20', '30', '40', 'All (max=50)']],
    'period': [['Overall', 'Week', 'Month'], ['3 Months', '6 Months', '12 Months']],
    'representation': [['Classic eight', 'World map'], ['Bar diagram', 'Pie diagram']],
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
    # else:
    #     context.bot.send_message(
    #         chat_id=update.message.chat_id,
    #         text="Wrong choice, dialog is finished",
    #         reply_markup=ReplyKeyboardRemove()
    #     )
    #     return states.END


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
        text="Now choose amount of stuff to retrieve",
        reply_markup=ReplyKeyboardMarkup(keyboards['amount'])
    )
    return states.USER_AMOUNT_SELECTION


def custom_period_selection_response(update, context):
    pass


def amount_selection_response(update, context):
    amount = update.message.text
    context.user_data['user']['amount'] = int(re.sub("\D", "", amount))
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Now choose type of chart",
        reply_markup=ReplyKeyboardMarkup(keyboards['representation'])
    )
    return states.USER_REPRESENTATION_SELECTION


def representation_selection_response(update, context):
    representation = update.message.text
    context.user_data['user']['representation'] = representation

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Wait until I generate image',
    )

    image = controllers.UserController(USER_MODEL).process(
        subject=context.user_data['user']['subject'],
        period=context.user_data['user']['period'],
        amount=context.user_data['user']['amount'],
        representation=context.user_data['user']['representation'],
    )

    context.bot.send_photo(
        chat_id=update.message.chat_id,
        caption=f'Enjoy',
        photo=open(image, 'rb'),
        reply_markup=ReplyKeyboardRemove()
    )
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
            states.USER_AMOUNT_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['amount'])),
                    amount_selection_response
                )
            ],
            states.USER_REPRESENTATION_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['representation'])),
                    representation_selection_response
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
