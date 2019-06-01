import telegram
from telegram.ext import CommandHandler

from visulast.utils.helpers import get_logger
import visulast.tg.states as states
from visulast.config import Configuration
from visulast.utils.helpers import is_lastfm_user_real


logger = get_logger(__name__)


def abort(update, context):
    if context.user_data:
        del context.user_data
    context.user_data.clear()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Current conversation is aborted",
        reply_markup=telegram.ReplyKeyboardRemove()
    )
    return states.END


def clean(update, context):
    if context.user_data:
        del context.user_data
    context.user_data.clear()
    update.message.reply_text("Your data is wiped")


def get_faq(update, context):
    update.message.reply_text("FAQ IS FUCK YOU")


def authorize(update, context):
    raise NotImplemented


def check_username(update, context):
    if 'lastfm_username' in context.user_data:
        username = context.user_data['lastfm_username']
        update.message.reply_text(
            f"Your last.fm username is [{username}](https://www.last.fm/user/{username})",
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text(
            'You haven\'t set last.fm username already. To set just type /authenticate _username_ ',
            parse_mode=telegram.ParseMode.MARKDOWN
        )


def authenticate(update, context):
    username = context.args[0]
    if is_lastfm_user_real(username):
        context.user_data['lastfm_username'] = username
        update.message.reply_text(
            f"You've set your last.fm username to [{username}](https://www.last.fm/user/{username})",
            parse_mode=telegram.ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id
        )
        return
    else:
        update.message.reply_text("Such user doesn't exist, please try again")


def get_help(update, context):
    print(context.chat_data)
    raise NotImplemented


def cancel(update, context):
    return states.END


def report(update, context):
    update.message.reply_text("Your report message was delivered to maintainer")
    context.bot.send_message(chat_id=Configuration().developerTelegramID, text=update.message.text)


def donate(update, context):
    raise NotImplemented


def error_callback(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Occured error "%s", report it with typing /report', context.error)


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
