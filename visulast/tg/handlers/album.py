from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler

from visulast.core import models, controllers, tools
from visulast.tg.handlers.general import abort
from visulast.tg import helpers
from visulast.tg.handlers import commons, states

keyboards = {
    'decision': [['Global', 'My library', 'Specific user']],
    'subject': [['Tracks', 'Info']],
    'representation': [['Pie graph', 'Bar graph']]
}

ALBUM_MODEL = None
ALBUM_CONTROLLER = None


def album(update, context):
    if not helpers.is_username_set(context):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="You cannot use this bot if you haven't provided last.fm username.\n"
                 "You can do it with /authenticate *username* command",
            reply_markup=ReplyKeyboardRemove,
            parse_mode=ParseMode.MARKDOWN,

        )
        return states.END

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Type artist's name",
        reply_markup=ReplyKeyboardRemove
    )
    context.user_data['album'] = {}
    return states.ALBUM_ARTIST_NAME_TYPING


def artist_name_response(update, context):
    artist_name = update.message.text
    artist = models.ArtistModel(artist_name)

    if not artist:
        context.bot.send_message("Such artist is not present at last.fm or you have misspelled")
        return states.END

    context.user_data['album']['artist_name'] = artist_name
    keyboard = [[album.item.title] for album in artist.get_albums(limit=15)]

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Now type album title or select among presented in keyboard',
        reply_markup=ReplyKeyboardMarkup(keyboard)
    )

    return states.ALBUM_TITLE_TYPING


def album_title_response(update, context):
    global ALBUM_MODEL, ALBUM_CONTROLLER
    title = update.message.text

    if not tools.does_album_exist(context.user_data['album']['artist_name'], title):
        context.bot.send_message("Such album is not present at last.fm library or you have misspelled")
        return states.END

    ALBUM_MODEL = models.AlbumModel(context.user_data['album']['artist_name'], title)
    ALBUM_CONTROLLER = controllers.AlbumController(ALBUM_MODEL)
    context.user_data['album']['album_title'] = title

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Should it be global stats, related to your username or other user?',
        reply_markup=ReplyKeyboardMarkup(keyboards['user_decision'])
    )
    return states.ALBUM_INFO_SOURCE_DECISION


def info_source_decision_response(update, context):
    decision = update.message.text
    context.user_data['album']['source'] = decision

    if decision == 'Specific user':

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Type username or choose among your friends',
            reply_markup=helpers.get_friends_keyboard(context.user_data['username'])
        )
        return states.ALBUM_SPECIFIC_USERNAME_SELECTION

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose tracks or info to provide",
        reply_markup=ReplyKeyboardMarkup(keyboards['entity_selection'])
    )
    return states.ALBUM_SUBJECT_SELECTION


def specific_username_response(update, context):
    username = update.message.text

    if not tools.does_user_exist(username):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Such user doesn't exist, try again",
        )

    context.user_data['album']['source'] = username

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose tracks or info to provide",
        reply_markup=ReplyKeyboardMarkup(keyboards['entity_selection'])
    )
    return states.ALBUM_SUBJECT_SELECTION


def subject_selection_response(update, context):
    global ALBUM_MODEL
    entity = update.message.text
    context.user_data['album']['subject'] = entity

    if entity == 'Tracks':
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Select the graph type of tracks",
            reply_markup=ReplyKeyboardMarkup(keyboards['representation'])
        )
        return states.ALBUM_REPRESENTATION_SELECTION
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=ALBUM_MODEL.get_info(),
            reply_markup=ReplyKeyboardRemove()
        )
        return states.END


def representation_selection_response(update, context):
    representation = update.message.text
    context.user_data['album']['representation'] = representation
    global ALBUM_CONTROLLER
    commons.finish_dialog(update, context, ALBUM_CONTROLLER)
    return states.END


HANDLERS = [
    ConversationHandler(
        entry_points=[
            CommandHandler('album', album, pass_user_data=True),
        ],
        states={
            states.ALBUM_ARTIST_NAME_TYPING: [
                MessageHandler(Filters.text, artist_name_response),
            ],
            states.ALBUM_TITLE_TYPING: [
                MessageHandler(Filters.text, album_title_response),
            ],
            states.ALBUM_INFO_SOURCE_DECISION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['decision'])),
                    info_source_decision_response
                ),
            ],
            states.ALBUM_SPECIFIC_USERNAME_SELECTION: [
                MessageHandler(Filters.text, specific_username_response),
            ],
            states.ALBUM_SUBJECT_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['subject'])),
                    subject_selection_response,
                ),
            ],
            states.ALBUM_REPRESENTATION_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['representation'])),
                    representation_selection_response,
                )
            ],
        },
        fallbacks=[
            CommandHandler('abort', abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='album.conversation'
    ),
]
