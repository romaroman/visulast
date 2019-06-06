from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler

from visulast.tg.handlers import states
from visulast.tg.handlers.general import abort

keyboards = {

}


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="It's the very beginning of our conversation. We should set up some moments before getting started.",
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Type /authenticate _username_ to set default username. "
             "Otherwise you won't be able to use main functionality.",
        parse_mode=ParseMode.MARKDOWN,
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
