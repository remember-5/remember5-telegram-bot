from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes

from bot.utils import logger


async def handler_reply_keyboard(update: Update, context: CallbackContext):
    """
    处理 /reply-keyboard 命令，发送内联键盘。
    """
    keyboard = [
        ["Option 1", "Option 2"], ["Option 3"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)


async def reply_keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    reply 是用 message 处理，和 inline 不同。
    """
    logger.info("reply_keyboard_callback")
    text = update.message.text
    if text == "Option 1":
        await update.message.reply_text("You chose Option 1")
    elif text == "Option 2":
        await update.message.reply_text("You chose Option 2")
    elif text == "Option 3":
        await update.message.reply_text("You chose Option 3")
    elif text == "Exit":
        await update.message.reply_text("Exiting...", reply_markup=None)
    else:
        await update.message.reply_text("Unknown option selected")
