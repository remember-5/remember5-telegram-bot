import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext
from bot.config import FILE_SAVE_PATH
from bot.utils import logger


# 定义回调前缀
CALLBACK_PREFIX_CONFIG = "config_"

async def handler_config_keyboard(update: Update, context: CallbackContext):
    """
    处理用户配置保存路径的命令。
    """
    # 创建路径配置按钮
    keyboard = [
        [InlineKeyboardButton("查看当前路径", callback_data=f"{CALLBACK_PREFIX_CONFIG}get_default_path")],
        [InlineKeyboardButton("使用默认路径", callback_data=f"{CALLBACK_PREFIX_CONFIG}set_default_path")],
        [InlineKeyboardButton("输入自定义路径", callback_data=f"{CALLBACK_PREFIX_CONFIG}input_custom_path")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # 询问用户选择保存路径
    await update.message.reply_text("请选择保存路径：", reply_markup=reply_markup)


async def config_keyboard_callback_set_default_path(update: Update, context: CallbackContext):
    """
    处理用户选择的保存路径。
    """
    # 获取用户选择的路径
    query = update.callback_query
    await query.answer()

    if query.data == f"{CALLBACK_PREFIX_CONFIG}set_default_path":
        # 设置默认路径
        save_path = FILE_SAVE_PATH
        context.user_data["save_path"] = save_path
        await query.edit_message_text(f"保存路径已设置为默认路径: {save_path}")
    elif query.data == f"{CALLBACK_PREFIX_CONFIG}get_default_path":
        # 获取默认路径
        save_path = context.user_data.get("save_path", FILE_SAVE_PATH)
        await query.edit_message_text(f"当前保存路径为默认路径: {save_path}")
    elif query.data == f"{CALLBACK_PREFIX_CONFIG}input_custom_path":
        # 提示用户输入自定义路径
        await query.edit_message_text("请输入自定义路径（例如：/path/to/save）：")
        context.user_data["pending_path_input"] = True


async def config_keyboard_callback_custom_path_input(update: Update, context: CallbackContext):
    """
    处理用户输入的自定义路径。
    """
    logger.info("config_keyboard_callback_custom_path_input")

    # 检查是否有待处理的路径输入
    if not context.user_data.get("pending_path_input"):
        logger.warning("No pending path input. Ignoring message.")
        return

    # 获取用户输入的路径
    user_input = update.message.text.strip()  # 去除前后空格
    logger.info(f"User input path: {user_input}")

    # 判断路径类型并生成完整路径
    if os.path.isabs(user_input):
        # 如果输入是绝对路径，直接使用
        save_path = os.path.normpath(user_input)  # 规范化路径
    else:
        # 如果输入是相对路径，与全局默认路径拼接
        save_path = os.path.normpath(os.path.join(FILE_SAVE_PATH, user_input))  # 规范化路径

    logger.info(f"Final save path: {save_path}")

    # 检查路径是否合法
    if not os.path.isabs(save_path):
        await update.message.reply_text("路径必须是绝对路径，请重新输入。")
        return

    # 检查路径是否存在，如果不存在则创建
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
        await update.message.reply_text(f"路径不存在，已创建: {save_path}")

    # 保存路径到 context.user_data
    context.user_data["save_path"] = save_path
    await update.message.reply_text(f"保存路径已设置为: {save_path}")

    # 清除标记
    del context.user_data["pending_path_input"]
