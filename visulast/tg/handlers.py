from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler, CallbackQueryHandler

import visulast.tg.states as states
import visulast.tg.commands as commands
import visulast.tg.calendar as calendar
import visulast.tg.keyboards as keyboards

from visulast.utils.helpers import keyboard_to_regex


handlers = [
    ConversationHandler(
        entry_points=[
            CommandHandler('visualize', commands.visualize, pass_user_data=True),
        ],
        states={
            states.CHOOSING_SUBJECT_TYPE: [
                MessageHandler(Filters.regex(f"^({keyboard_to_regex(keyboards.visualize['subject_types'])})$"),
                               commands.subject_type_choosing, pass_user_data=True)
            ],
            states.CHOOSING_USER_SUBJECT: [
                MessageHandler(Filters.regex(f"^({keyboard_to_regex(keyboards.visualize['user_subjects'])})$"),
                               commands.user_subject_choosing, pass_user_data=True)
            ],
            states.CHOOSING_LASTFM_SUBJECT: [
                MessageHandler(Filters.regex(f"^({keyboard_to_regex(keyboards.visualize['lastfm_subjects'])})$"),
                               commands.lastfm_subject_choosing, pass_user_data=True)
            ],
            states.CHOOSING_HOW_MUCH: [

            ],
            states.CHOOSING_PERIOD: [
                MessageHandler(Filters.regex(f"^({keyboard_to_regex(keyboards.visualize['periods'])})$"),
                               commands.period_choosing, pass_user_data=True),
            ],
            states.CHOOSING_GRAPH: [
                MessageHandler(Filters.regex(f"^({keyboard_to_regex(keyboards.visualize['graphs'])})$"),
                               commands.graph_choosing, pass_user_data=True),
            ],
            states.CONFIRMATION: [

            ],
        },
        fallbacks=[
            CommandHandler('abort', commands.abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='visualize.conversation'
    ),
    ConversationHandler(
        entry_points=[
            CommandHandler('start', commands.configure, pass_user_data=True),
        ],
        states={

        },
        fallbacks=[
            CommandHandler('abort', commands.abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='start.conversation'
    ),
    ConversationHandler(
        entry_points=[
            CommandHandler('configure', commands.configure, pass_user_data=True),
        ],
        states={

        },
        fallbacks=[
            CommandHandler('abort', commands.abort, pass_user_data=True),
        ],
        allow_reentry=True,
        persistent=True,
        name='configure.conversation'
    ),
    CommandHandler('help', commands.get_help, pass_user_data=True),
    CommandHandler('faq', commands.get_faq, pass_user_data=True),

    CommandHandler('authorize', commands.authorize, pass_user_data=True),
    CommandHandler('authenticate', commands.authenticate, pass_user_data=True, pass_args=True),
    CommandHandler('is_authenticated', commands.check_username, pass_user_data=True),

    CommandHandler('clean', commands.clean, pass_user_data=True),
    CommandHandler('report', commands.report, pass_user_data=True),
    CommandHandler('donate', commands.donate, pass_user_data=True),

    # TODO: move to visualize conversation
    CommandHandler('calendar', calendar.calendar_handler),
    CallbackQueryHandler(calendar.inline_handler)
]