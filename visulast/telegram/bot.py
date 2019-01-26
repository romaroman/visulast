from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler

from config import CONFIGURATION
from telegram.handlers import *

logger = logger
PERIOD_CHOOSING, TYPE_CHOOSING = range(2)


def main():
    updater = Updater(token=CONFIGURATION.telegram_bot)
    dispatcher = updater.dispatcher

    handlers = [
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                PERIOD_CHOOSING: [RegexHandler('^(Day|Week|Month|Quarter|Half a year|Year|Overall|Custom$', period)]
            },
            fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
        ),
        CommandHandler('artists', artists, pass_args=True),
        CommandHandler('default_username', default_username, pass_args=True),
    ]
    for handler in handlers:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
