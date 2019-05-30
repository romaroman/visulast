from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler, Filters, MessageHandler, \
    PicklePersistence

from visulast.tg import commands
from visulast.config import Configuration
from visulast.utils.helpers import keyboard_to_regex, get_logger

logger = get_logger(__name__)

CHOOSING_SUBJECT = 0
CHOOSING_PERIOD = 1
CHOOSING_GRAPH = 2
CHOOSING_HOW = 3


def main():
    pp = PicklePersistence(filename='bot')
    updater = Updater(token=Configuration().tokens.telegram_bot, persistence=pp, use_context=True)
    dispatcher = updater.dispatcher

    hs = [
        ConversationHandler(
            entry_points=[
                CommandHandler('visualize', commands.visualize, pass_user_data=True),
            ],
            states={
                CHOOSING_SUBJECT: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['subjects'])})$"),
                                   commands.visualize, pass_user_data=True)
                ],
                CHOOSING_PERIOD: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['periods'])})$"),
                                   commands.period_choice, pass_user_data=True),
                    MessageHandler(Filters.regex('^Custom$'), commands.custom_period_choice, pass_user_data=True),
                ],
                CHOOSING_GRAPH: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['graphs'])})$"),
                                   commands.graph_choice, pass_user_data=True),

                ],
                CHOOSING_HOW: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['how'])})$"),
                                   commands.how_choice, pass_user_data=True),
                ],
            },
            fallbacks=[
                CommandHandler('abort', commands.abort, pass_user_data=True),
            ],
            name="Regular conversation",
            persistent=True

        ),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
        CommandHandler('abort', commands.abort, pass_user_data=True),
    ]

    for handler in hs:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(commands.error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
