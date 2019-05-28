from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler, Filters, MessageHandler, PicklePersistence

from visulast.tg import commands
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
    pp = PicklePersistence(filename='bot')

    hs = [
        ConversationHandler(
            entry_points=[
                CommandHandler('visualize', commands.visualize, pass_user_data=True),
            ],
            states={
                CHOOSING_SUBJECT: RegexHandler(f"^({keyboard_to_regex(commands.keyboards['subjects'])})$",
                             commands.visualize, pass_user_data=True),
                CHOOSING_PERIOD: [
                    RegexHandler(f"^({keyboard_to_regex(commands.keyboards['periods'])})$",
                                 commands.period_choice, pass_user_data=True),
                    RegexHandler('^Custom$', commands.custom_period_choice, pass_user_data=True),
                ],
                CHOOSING_GRAPH: [
                    RegexHandler(f"^({keyboard_to_regex(commands.keyboards['graphs'])})$",
                                 commands.graph_choice, pass_user_data=True),
                ],
            },
            fallbacks=[
            ],
            name="Regular conversation",
            persistent=True

        ),
    ]

    for handler in hs:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(commands.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
