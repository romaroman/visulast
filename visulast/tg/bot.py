from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler, Filters, MessageHandler

from visulast.tg import handlers
from visulast.config import Configuration
from visulast.utils.helpers import keyboard_to_regex, get_logger

logger = get_logger(__name__)

CHOOSING_SUBJECT = 0
CHOOSING_PERIOD = 1
CHOOSING_GRAPH = 2
NO_JOBS = 3


def main():
    updater = Updater(token=Configuration().tokens.telegram_bot)
    dispatcher = updater.dispatcher

    hs = [
        ConversationHandler(
            entry_points=[
                CommandHandler('visualize', handlers.visualize, pass_user_data=True),
                RegexHandler(f"^({keyboard_to_regex(handlers.keyboards['subjects'])})$",
                                                handlers.visualize, pass_user_data=True)
            ],
            states={
                CHOOSING_PERIOD: [
                    RegexHandler(f"^({keyboard_to_regex(handlers.keyboards['periods'])})$",
                                 handlers.period_choice, pass_user_data=True),
                    RegexHandler('^Custom$', handlers.custom_period_choice, pass_user_data=True),
                ],
                CHOOSING_GRAPH: [
                    RegexHandler(f"^({keyboard_to_regex(handlers.keyboards['graphs'])})$",
                                 handlers.graph_choice, pass_user_data=True),
                ],
            },
            fallbacks=[
                CommandHandler('done', handlers.done, pass_user_data=True),
                CommandHandler('remove_keyboard', handlers.remove_keyboard, pass_user_data=True),
                CommandHandler('force_finish', handlers.force_finish, pass_user_data=True),
            ]
        ),
        CommandHandler('faq', handlers.faq),
        CommandHandler('examples', handlers.examples, pass_args=True),
        CommandHandler('remove_keyboard', handlers.remove_keyboard)
    ]

    for handler in hs:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(handlers.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
