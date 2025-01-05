from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.logger import logger

async def handler_error(update: Update, context: CallbackContext):
    """
    处理错误
    :param update:
    :param context:
    :return:
    """
    logger.warning(f'Update {update} caused error {context.error}')
