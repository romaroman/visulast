from telegram import ReplyKeyboardMarkup

import visulast.tg.states as states
from visulast.tg.keyboards import configure as keyboard


def configure(update, context):
    # reply_markup = ReplyKeyboardMarkup(keyboard[''], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="You have called configuration dialog, choose appopriate option to set up",
        # reply_markup=reply_markup
    )
    return states.CONFIGURE
