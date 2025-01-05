import requests

from bot.handlers import handler_inline_keyboard, handler_reply_keyboard, handler_help, handler_start, handler_error
from bot.handlers.config_handlers import handler_config_keyboard, config_keyboard_callback_custom_path_input, \
    config_keyboard_callback_set_default_path, CALLBACK_PREFIX_CONFIG
from bot.handlers.inline_handlers import inline_keyboard_callback, CALLBACK_PREFIX_OPTION
from bot.handlers.reply_handlers import reply_keyboard_callback
from bot.utils.logger import logger  # 直接导入全局日志记录器
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.config import TELEGRAM_BOT_TOKEN
from bot.database import init_db
from bot.handlers.media_handlers import  handle_media

commands = [
    {"command": "start", "description": "Start the bot"},
    {"command": "config_path", "description": "Set config path"},
    {"command": "help", "description": "Get help"},
    {"command": "settings", "description": "Change settings"},
    {"command": "reply_keyboard", "description": "Send reply keyboard"},
    {"command": "inline_keyboard", "description": "Send inline keyboard"},
]

def set_bot_commands(bot_token: str, commands: list):
    """
    设置 Bot 的快捷命令。
    """
    url = f"https://api.telegram.org/bot{bot_token}/setMyCommands"
    payload = {
        "commands": commands
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Bot commands set successfully!")
    else:
        print(f"Failed to set bot commands: {response.text}")

set_bot_commands(TELEGRAM_BOT_TOKEN, commands)
# 初始化数据库
init_db()
def main():
    # 初始化 Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加命令处理器
    application.add_handler(CommandHandler("start", handler_start))
    application.add_handler(CommandHandler("help", handler_help))
    application.add_handler(CommandHandler("reply_keyboard", handler_reply_keyboard))
    application.add_handler(CommandHandler("inline_keyboard", handler_inline_keyboard))
    application.add_handler(CommandHandler("config_path", handler_config_keyboard))

    # 处理用户输入的自定义路径
    # 匹配 纯文本消息，同时排除 命令消息。
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, config_keyboard_callback_custom_path_input))
    application.add_handler(CallbackQueryHandler(config_keyboard_callback_set_default_path, pattern=f"^{CALLBACK_PREFIX_CONFIG}.+$"))

    # 添加回调处理器
    application.add_handler(CallbackQueryHandler(inline_keyboard_callback, pattern=f"^{CALLBACK_PREFIX_OPTION}.+$"))

    # 添加消息处理器（处理文本消息）
    # filters.TEXT ：匹配所有文本消息。
    # filters.Text("keyword") ：匹配包含特定关键词的文本消息。
    # filters.Regex(r"pattern") ：匹配符合正则表达式的文本消息。
    # filters.Command("command") ：匹配特定命令（如 /start）。
    # filters.PHOTO ：匹配图片消息。
    # filters.VIDEO ：匹配视频消息。
    application.add_handler(MessageHandler(filters.TEXT, reply_keyboard_callback))

    # 添加消息处理器（处理视频|图片）
    application.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, handle_media))


    # application.add_handler(MessageHandler(filters.FORWARDED, handle_media_group))

    # 添加错误处理器
    application.add_error_handler(handler_error)

    # 启动 Bot
    logger.info("Starting Telegram Bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
