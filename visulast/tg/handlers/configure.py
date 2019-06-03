from telegram.ext import ConversationHandler, CommandHandler

from visulast.tg.handlers import states
from visulast.tg.handlers.general import abort

keyboards = {

}


def configure(update, context):
    # reply_markup = ReplyKeyboardMarkup(keyboard[''], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="You have called configuration dialog, choose appropriate option to set up",
        # reply_markup=reply_markup
    )
    return states.CONFIGURE


HANDLERS = [
    ConversationHandler(
        entry_points=[
            CommandHandler('configure', configure, pass_user_data=True),
        ],
        states={

        },
        fallbacks=[
            CommandHandler('abort', abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='configure.conversation'
    ),
]