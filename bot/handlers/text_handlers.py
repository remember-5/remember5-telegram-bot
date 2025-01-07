import os
from telegram import Update
from telegram.ext import CallbackContext

from bot.config import FILE_SAVE_PATH
from bot.utils.logger import logger

async def text_callback(update: Update, context: CallbackContext):
    """
    处理用户输入的文本。
    """
    logger.info(f"text_callback {update.message}")

    # 检查是否有待处理的输入
    if "pending_input" not in context.user_data:
        logger.warning("No pending input. Ignoring message.")
        return

    # 获取用户输入的文本
    user_input = update.message.text.strip()  # 去除前后空格
    logger.info(f"User input: {user_input}")

    # 根据输入类型处理
    pending_input = context.user_data["pending_input"]
    input_type = pending_input.get("type")

    if input_type == "input_custom_path":
        # 处理自定义路径输入
        await handle_custom_path_input(update, context, user_input)
    elif input_type == "folder_name":
        # 处理文件夹名称输入
        await handle_folder_name_input(update, context, user_input)
    else:
        logger.warning(f"Unknown input type: {input_type}")
        await update.message.reply_text("未知的输入类型，请重试。")

    # 清除标记
    del context.user_data["pending_input"]

async def handle_custom_path_input(update: Update, context: CallbackContext, user_input: str):
    """
    处理用户输入的自定义路径。
    """
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

async def handle_folder_name_input(update: Update, context: CallbackContext, user_input: str):
    """
    处理用户输入的文件夹名称。
    """
    # 假设用户输入的是文件夹名称
    folder_name = user_input
    save_path = os.path.join(FILE_SAVE_PATH, folder_name)

    # 检查路径是否存在，如果不存在则创建
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
        await update.message.reply_text(f"文件夹 '{folder_name}' 已创建: {save_path}")
    else:
        await update.message.reply_text(f"文件夹 '{folder_name}' 已存在: {save_path}")
