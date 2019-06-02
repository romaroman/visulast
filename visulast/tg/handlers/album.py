from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CommandHandler

from visulast.core import tools
from visulast.core import models, controllers, scrappers
from visulast.tg.handlers.general import abort
from visulast.tg import states
from visulast.tg import helpers


keyboards = {
    'user_decision': [['Global', 'My library', 'Specific user']],
    'entity_selection': [['Tracks', 'Info']],
    'representation': [['Pie chart', 'Bar chart']]
}

ALBUM_MODEL = None


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
    keyboard = [[album.item.title] for album in artist.get_albums(limit=10)]

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Now type album title or select among presented in keyboard',
        reply_markup=ReplyKeyboardMarkup(keyboard)
    )

    return states.ALBUM_TITLE_TYPING


def album_title_response(update, context):
    global ALBUM_MODEL
    title = update.message.text

    if not tools.does_album_exist(context.user_data['album']['artist_name'], title):
        context.bot.send_message("Such album is not present at last.fm library or you have misspelled")
        return states.END

    ALBUM_MODEL = models.AlbumModel(context.user_data['album']['artist_name'], title)
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
        friends = scrappers.FriendsScrapper.get_friends_by_username(context.user_data['username'])
        reply_markup = ReplyKeyboardMarkup([[friend] for friend in friends])

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Type username or choose among your friends',
            reply_markup=reply_markup
        )
        return states.ALBUM_SPECIFIC_USERNAME_SELECTION

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose tracks or info to provide",
        reply_markup=ReplyKeyboardMarkup(keyboards['entity_selection'])
    )
    return states.ALBUM_ENTITY_SELECTION


def specific_username_response(update, context):
    username = update.message.text

    if tools.does_user_exist(username):
        context.bot.send_message("Such user doesn't exist")
        return states.END

    context.user_data['album']['source'] = username

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose tracks or info to provide",
        reply_markup=ReplyKeyboardMarkup(keyboards['entity_selection'])
    )
    return states.ALBUM_ENTITY_SELECTION


def entity_selection_response(update, context):
    global ALBUM_MODEL
    entity = update.message.text
    context.user_data['album']['entity'] = entity

    if entity == 'Tracks':
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Select the chart type of tracks",
            reply_markup=ReplyKeyboardMarkup(keyboards['representation'])
        )
        return states.ALBUM_REPRESENTATION_SELECTION
    else:
        reply_text = ALBUM_MODEL.get_info()
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_text,
            reply_markup=ReplyKeyboardRemove()
        )
        return states.END


def representation_selection_response(update, context):
    representation = update.message.text
    controller = controllers.AlbumController(ALBUM_MODEL)
    if representation == 'Bar chart':
        image = controller.tracks_bar_chart()
    else:
        image = controller.tracks_pie_chart()

    context.bot.send_photo(
        chat_id=update.message.chat_id,
        caption=f'Enjoy',
        photo=open(image, 'rb'),
        reply_markup=ReplyKeyboardRemove()
    )


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
                    Filters.regex(helpers.keyboard_to_regex(keyboards['user_decision'])),
                    info_source_decision_response
                ),
            ],
            states.ALBUM_SPECIFIC_USERNAME_SELECTION: [
                MessageHandler(Filters.text, specific_username_response),
            ],
            states.ALBUM_ENTITY_SELECTION: [
                MessageHandler(
                    Filters.regex(helpers.keyboard_to_regex(keyboards['entity_selection'])),
                    entity_selection_response,
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
