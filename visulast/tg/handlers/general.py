from telegram import ReplyKeyboardRemove, ParseMode
from telegram.ext import CommandHandler

from visulast.utils.helpers import get_logger
from visulast.tg import states
from visulast.config import Configuration
from visulast.core import tools

logger = get_logger(__name__)


def abort(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Current conversation is aborted",
        reply_markup=ReplyKeyboardRemove()
    )
    return states.END


def clean(update, context):
    if context.user_data:
        del context.user_data
    context.user_data.clear()
    update.message.reply_text("Your data is wiped")


def get_faq(update, context):
    raise NotImplemented


def authorize(update, context):
    raise NotImplemented


def check_username(update, context):
    if 'username' in context.user_data:
        username = context.user_data['username']
        update.message.reply_text(
            f"Your last.fm username is [{username}](https://www.last.fm/user/{username})",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text(
            'You haven\'t set last.fm username already. To set just type /authenticate _username_ ',
            parse_mode=ParseMode.MARKDOWN
        )


def authenticate(update, context):
    username = context.args[0]
    if tools.does_user_exist(username):
        context.user_data['username'] = username
        update.message.reply_text(
            f"You've set your last.fm username to [{username}](https://www.last.fm/user/{username})",
            parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id
        )
        return
    else:
        update.message.reply_text("Such user doesn't exist, please try again")


def get_help(update, context):
    update.message.reply_text("""
/user - Visualize user's library
/artist - Visualize specific artist data
/album - Visualize specific album information
/tag - Visualize specific tag data
/track - Visualize specific track summary

/abort - Cancel current operation
/cancel - Set conversation state to beginning

/help - List all commands with theirs descriptions
/faq - Find out how to use this bot

/clean - Wipe out ALL data associated with your Telegram ID
/authenticate - Set your last.fm username without authorization
/authorize - Authenticate with last.fm website

/report - Send a bug report with maintainer
/donate - Share some money with developer
    """)


def cancel(update, context):
    return states.END


def report(update, context):
    update.message.reply_text("Your report message was delivered to maintainer")
    user_link = f'[{update.message.chat.username}](tg://user?id={update.message.chat.id})'
    message = f"From {user_link} was reported _{''.join(context.args)}_"
    context.bot.send_message(chat_id=Configuration().developerTelegramID, text=message, parse_mode=ParseMode.MARKDOWN)


def donate(update, context):
    raise NotImplemented


def error_callback(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Occurred error "%s", report it with typing /report', context.error)


HANDLERS = [
    CommandHandler('help', get_help, pass_user_data=True),
    CommandHandler('faq', get_faq, pass_user_data=True),

    CommandHandler('authorize', authorize, pass_user_data=True),
    CommandHandler('authenticate', authenticate, pass_user_data=True, pass_args=True),
    CommandHandler('is_authenticated', check_username, pass_user_data=True),

    CommandHandler('clean', clean, pass_user_data=True),
    CommandHandler('report', report, pass_user_data=True),
    CommandHandler('donate', donate, pass_user_data=True),
]
