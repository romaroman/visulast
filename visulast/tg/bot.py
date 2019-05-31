from telegram.ext import Updater, PicklePersistence
from visulast.tg import commands
from visulast.config import Configuration
from visulast.utils.helpers import get_logger
from visulast.tg.handlers import handlers
from visulast.utils.helpers import PROJ_PATH

logger = get_logger(__name__)


def attach_handlers(dispatcher):
    for handler in handlers:
        dispatcher.add_handler(handler)
    logger.info(f'All {len(handlers)} where successfully attached')


def start():
    updater = Updater(
        token=Configuration().tokens.telegram_bot, use_context=True,
        persistence=PicklePersistence(filename=f'{PROJ_PATH}cache/visulast.pkl')
    )
    dispatcher = updater.dispatcher
    attach_handlers(dispatcher)

    dispatcher.add_error_handler(commands.error_callback)

    updater.start_polling()
    updater.idle()
