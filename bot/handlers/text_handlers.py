import os

from telegram import Update
from telegram.ext import CallbackContext

from bot.config import FILE_SAVE_PATH
from bot.utils import logger
from bot.utils.promission_utils import check_admin


async def text_callback(update: Update, context: CallbackContext):
    """
    处理用户输入的自定义路径。
    """
    logger.info(f"text_callback {update.message}")

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
