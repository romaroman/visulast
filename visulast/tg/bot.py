from telegram.ext import Updater, ConversationHandler, CommandHandler, RegexHandler

from config import Configuration
import tg.handlers as handlers
from utils import keyboard_to_regex, get_logger

logger = get_logger(__name__)
SUBJECT_CHOOSING, GRAPH_CHOOSING, PERIOD_CHOOSING = range(3)


def main():
    updater = Updater(token=Configuration().tokens.telegram_bot)
    dispatcher = updater.dispatcher

    hs = [
        ConversationHandler(
            entry_points=[CommandHandler('start', handlers.start)],
            states={
                SUBJECT_CHOOSING: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['subjects'])),
                                                handlers.subject_selector, pass_user_data=True)],

                GRAPH_CHOOSING: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['graphs'])),
                                              handlers.graph_selector, pass_user_data=True)],

                PERIOD_CHOOSING: [RegexHandler('^({})$'.format(keyboard_to_regex(handlers.keyboards['periods'])),
                                               handlers.period_selector, pass_user_data=True),
                                  RegexHandler('^Something else...$',
                                               handlers.custom_period_selector, pass_user_data=True)
                                  ],
            },
            fallbacks=[RegexHandler('^Done$', handlers.done, pass_user_data=True)]
        ),
        CommandHandler('visu', handlers.visu, pass_args=True),
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
