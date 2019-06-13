from telegram import ReplyKeyboardRemove, ChatAction
from visulast.core import controllers


def finish_dialog(update, context, controller):
    image = None
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Wait until I generate image...',
    )
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)

    if type(controller) == controllers.UserController:
        image = controller.process(
            subject=context.user_data['user']['subject'],
            representation=context.user_data['user']['representation'],
            period=context.user_data['user']['period'],
            amount=context.user_data['user']['amount'],
        )
    elif type(controller) == controllers.AlbumController:
        image = controller.process(
            subject=context.user_data['album']['entity'],
            representation=context.user_data['album']['representation'],
        )

    if not image:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='For specified parameters controller has no response not yet, sorry',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            caption=f'Enjoy',
            photo=open(image, 'rb'),
            reply_markup=ReplyKeyboardRemove()
        )
