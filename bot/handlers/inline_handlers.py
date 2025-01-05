from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ContextTypes

from bot.utils import logger


CALLBACK_PREFIX_OPTION = "option_"

async def handler_inline_keyboard(update: Update, context: CallbackContext):
    """
    处理 /line-keyboard 命令，发送内联键盘。
    """
    user_id = update.message.from_user.id

    # 创建内联键盘
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data=f"{CALLBACK_PREFIX_OPTION}option1_{user_id}")],
        [InlineKeyboardButton("Option 2", callback_data=f"{CALLBACK_PREFIX_OPTION}option2_{user_id}")],
        [InlineKeyboardButton("Option 3", callback_data=f"{CALLBACK_PREFIX_OPTION}option3_{user_id}")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # 发送内联键盘
    await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)


async def inline_keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理用户点击按钮的回调。
    """
    logger.info("inline_keyboard_callback")
    query = update.callback_query
    await query.answer()

    # 解析 callback_data
    data = query.data.split("_")
    logger.info(f"data: {data}")
    option = data[0]
    user_id = int(data[1])

    if option == f"{CALLBACK_PREFIX_OPTION}option1":
        await query.edit_message_text(text=f"User {user_id} chose Option 1")
    elif option == f"{CALLBACK_PREFIX_OPTION}option2":
        await query.edit_message_text(text=f"User {user_id} chose Option 2")
    elif option == f"{CALLBACK_PREFIX_OPTION}option3":
        await query.edit_message_text(text=f"User {user_id} chose Option 3")
