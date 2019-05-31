from telegram import ReplyKeyboardMarkup

import visulast.tg.states as states
from visulast.tg.keyboards import start as keyboard


def start(update, context):
    # reply_markup = ReplyKeyboardMarkup(keyboard[''], one_time_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="It's the very beginning of our conversation. We should set up some moments before getting started",
        # reply_markup=reply_markup
    )
    return states.START
