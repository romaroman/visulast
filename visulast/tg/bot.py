from telegram.ext import Updater, PicklePersistence
from visulast.config import Configuration
from visulast.tg.handlers.general import error_callback
from visulast.utils.helpers import get_logger
from visulast.utils.helpers import PROJ_PATH

from visulast.tg import handlers


logger = get_logger(__name__)


def attach_handlers(dispatcher):
    hs = []
    hs.extend(handlers.general_handlers)
    hs.extend(handlers.calendar_handlers)
    hs.extend(handlers.visualize_handlers)
    hs.extend(handlers.start_handlers)
    hs.extend(handlers.configure_handlers)
    hs.extend(handlers.album_handlers)
    hs.extend(handlers.user_handlers)
    for handler in hs:
        dispatcher.add_handler(handler)
    logger.info(f'All {len(hs)} handlers where successfully attached')


def start():
    updater = Updater(
        token=Configuration().tokens.telegram_bot, use_context=True,
        persistence=PicklePersistence(filename=f'{PROJ_PATH}cache/visulast.pkl'),
    )
    dispatcher = updater.dispatcher
    attach_handlers(dispatcher)

    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start()