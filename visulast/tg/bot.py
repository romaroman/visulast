from telegram.ext import Updater, ConversationHandler, CommandHandler, Filters, MessageHandler, PicklePersistence, \
    CallbackQueryHandler
from visulast.tg import commands
from visulast.config import Configuration
from visulast.utils.helpers import keyboard_to_regex, get_logger
import visulast.tg.calendar as calendar


logger = get_logger(__name__)

END = -1
CHOOSING_SUBJECT_TYPE, CHOOSING_USER_SUBJECT, CHOOSING_LASTFM_SUBJECT, CHOOSING_PERIOD, CHOOSING_GRAPH, CHOOSING_HOW, CONFIRMATION = range(7)


def attach_handlers(dispatcher):
    handlers = [
        ConversationHandler(
            entry_points=[
                CommandHandler('visualize', commands.visualize, pass_user_data=True),
            ],
            states={
                CHOOSING_SUBJECT_TYPE: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['subject_types'])})$"),
                                   commands.subject_type_choosing, pass_user_data=True)
                ],
                CHOOSING_USER_SUBJECT: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['user_subjects'])})$"),
                                   commands.user_subject_choosing, pass_user_data=True)
                ],
                CHOOSING_LASTFM_SUBJECT: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['lastfm_subjects'])})$"),
                                   commands.lastfm_subject_choosing, pass_user_data=True)
                ],
                CHOOSING_PERIOD: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['periods'])})$"),
                                   commands.period_choosing, pass_user_data=True),
                ],
                CHOOSING_GRAPH: [
                    MessageHandler(Filters.regex(f"^({keyboard_to_regex(commands.keyboards['graphs'])})$"),
                                   commands.graph_choosing, pass_user_data=True),
                ],
                CONFIRMATION: [

                ],
            },
            fallbacks=[
                CommandHandler('abort', commands.abort, pass_user_data=True),
            ],
            allow_reentry=True,
            persistent=True,
            name='visualize conversation'
        ),
        CommandHandler('help', commands.get_help, pass_user_data=True),
        CommandHandler('faq', commands.get_faq, pass_user_data=True),
        CommandHandler('clean', commands.clean, pass_user_data=True),
        CommandHandler('authenticate', commands.authenticate, pass_user_data=True, pass_args=True),
        CommandHandler('authorize', commands.authorize, pass_user_data=True),
        CommandHandler('report', commands.report, pass_user_data=True),
        CommandHandler('donate', commands.donate, pass_user_data=True),
        CommandHandler('check_username', commands.check_username, pass_user_data=True),
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)


def main():
    persistance = PicklePersistence(filename='visulast.tg.bot')
    updater = Updater(token=Configuration().tokens.telegram_bot, use_context=True, persistence=persistance)
    dispatcher = updater.dispatcher

    attach_handlers(dispatcher)
    dispatcher.add_error_handler(commands.error_callback)

    updater.dispatcher.add_handler(CommandHandler("calendar", calendar.calendar_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(calendar.inline_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
