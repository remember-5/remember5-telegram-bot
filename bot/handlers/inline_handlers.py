from telegram import Update
from telegram.ext import CallbackContext
from bot.config import FILE_SAVE_PATH
from bot.handlers.btn_constants import folder_btn, config_btn


async def handler_inline_callback(update: Update, context: CallbackContext):
    """
    处理用户选择的保存路径。
    """
    query = update.callback_query
    await query.answer()

    # 获取用户选择的路径
    if query.data == folder_btn["create_folder"]["callback_data"]:
        # 创建文件夹
        await query.edit_message_text(folder_btn["create_folder"]["text"])
    elif query.data == folder_btn["delete_folder"]["callback_data"]:
        # 删除文件夹
        await query.edit_message_text(folder_btn["delete_folder"]["text"])
    elif query.data == folder_btn["show_folder"]["callback_data"]:
        # 查看文件夹
        await query.edit_message_text(folder_btn["show_folder"]["text"])
    elif query.data == config_btn["set_default_path"]["callback_data"]:
        # 设置默认路径
        save_path = FILE_SAVE_PATH
        context.user_data["save_path"] = save_path
        await query.edit_message_text(f"保存路径已设置为默认路径: {save_path}")
    elif query.data == config_btn["get_default_path"]["callback_data"]:
        # 获取默认路径
        save_path = context.user_data.get("save_path", FILE_SAVE_PATH)
        await query.edit_message_text(f"当前保存路径为默认路径: {save_path}")
    elif query.data == config_btn["input_custom_path"]["callback_data"]:
        # 提示用户输入自定义路径
        await query.edit_message_text("请输入自定义路径（例如：/path/to/save）：")
        context.user_data["pending_path_input"] = True
