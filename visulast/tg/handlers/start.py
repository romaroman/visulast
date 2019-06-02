from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from visulast.tg import states
from visulast.tg.handlers.general import abort
from visulast.tg.handlers.visualize import CommandHandler

keyboards = {

}


def start(update, context):
    # reply_markup = ReplyKeyboardMarkup(keyboard[''], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="It's the very beginning of our conversation. We should set up some moments before getting started",
        # reply_markup=reply_markup
    )
    return states.START


HANDLERS = {
    ConversationHandler(
        entry_points=[
            CommandHandler('start', start, pass_user_data=True),
        ],
        states={

        },
        fallbacks=[
            CommandHandler('abort', abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='start.conversation'
    ),
}
