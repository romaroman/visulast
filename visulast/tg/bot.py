from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler, Filters, MessageHandler

from tg import handlers
from config import Configuration
from utils import keyboard_to_regex, get_logger

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
            entry_points=[CommandHandler('start', handlers.start)],
            states={
                NO_JOBS: [CommandHandler('visu', handlers.visu)],
                CHOOSING_SUBJECT: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['subjects'])),
                                                handlers.subject_choice, pass_user_data=True)],
                CHOOSING_PERIOD: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['periods'])),
                                               handlers.period_choice, pass_user_data=True),
                                  RegexHandler('^Custom$',
                                               handlers.custom_period_choice, pass_user_data=True)
                                  ],
                CHOOSING_GRAPH: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['graphs'])),
                                              handlers.graph_choice, pass_user_data=True)],
                # GRAPH_CHOOSING: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['graphs'])),
                #                               handlers.graph_selector, pass_user_data=True)],

                # CHOOSING_SUBJECT: [MessageHandler(Filters.text,
                #                                   handlers.subject_choice, pass_user_data=True),
                #                    ],
            },
            fallbacks=[RegexHandler('^Done$', handlers.done, pass_user_data=True)]
        ),
        CommandHandler('guide', handlers.guide),
        CommandHandler('faq', handlers.faq),
        CommandHandler('examples', handlers.examples, pass_args=True),
        CommandHandler('set_username', handlers.set_username, pass_args=True),
        CommandHandler('abort', handlers.abort)
    ]

    for handler in hs:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(handlers.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
