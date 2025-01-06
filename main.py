import requests

from bot.command import set_bot_commands, commands, commands_keys
from bot.handlers import handler_inline_keyboard, handler_reply_keyboard, handler_help, handler_start, handler_error
from bot.handlers.config_handlers import handler_config_keyboard, config_keyboard_callback_custom_path_input, \
    config_keyboard_callback_set_default_path, CALLBACK_PREFIX_CONFIG
from bot.handlers.inline_handlers import inline_keyboard_callback, CALLBACK_PREFIX_OPTION
from bot.handlers.reply_handlers import reply_keyboard_callback
from bot.utils.logger import logger  # 直接导入全局日志记录器
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.config import TELEGRAM_BOT_TOKEN, UPDATE_MY_COMMANDS
from bot.database import init_db, close_db
from bot.handlers.media_handlers import  handle_media


def main():
    # 设置 Bot 快捷命令
    if UPDATE_MY_COMMANDS:
        set_bot_commands(TELEGRAM_BOT_TOKEN, commands)

    # 初始化 Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 初始化数据库
    init_db()

    # 添加错误处理器
    application.add_error_handler(handler_error)

    # 添加命令处理器
    # 配置在command/commands_config.py
    application.add_handler(CommandHandler(commands_keys["start"]["command"], handler_start))
    application.add_handler(CommandHandler(commands_keys["help"]["command"], handler_help))
    application.add_handler(CommandHandler(commands_keys["reply_keyboard"]["command"], handler_reply_keyboard))
    application.add_handler(CommandHandler(commands_keys["inline_keyboard"]["command"], handler_inline_keyboard))
    application.add_handler(CommandHandler(commands_keys["config_path"]["command"], handler_config_keyboard))

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
    # 启动 Bot
    logger.info("Starting Telegram Bot...")


    application.run_polling()

    # 关闭数据库连接
    close_db()

if __name__ == "__main__":

    main()
