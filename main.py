from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from bot.command import set_bot_commands, commands, commands_keys
from bot.config import TELEGRAM_BOT_TOKEN, UPDATE_MY_COMMANDS
from bot.database import init_db, close_db
from bot.handlers import handler_error, start, settings, helps, reply, handle_media_callback
from bot.handlers.text_handlers import text_callback
from bot.handlers.inline_handlers import handler_inline_callback
from bot.utils.logger import logger


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
    # filters.Command("command") ：匹配特定命令（如 /start）。
    application.add_handler(CommandHandler(commands_keys["start"]["command"], start))
    application.add_handler(CommandHandler(commands_keys["settings"]["command"], settings))
    application.add_handler(CommandHandler(commands_keys["help"]["command"], helps))
    application.add_handler(CommandHandler(commands_keys["reply_keyboard"]["command"], reply))

    # 添加inline回调处理器
    application.add_handler(CallbackQueryHandler(handler_inline_callback))

    # 处理用户输入的自定义路径
    # 匹配 纯文本消息，同时排除 命令消息。
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, config_keyboard_callback_custom_path_input))

    # 添加消息处理器（处理文本消息） 处理reply和普通的message
    # filters.TEXT ：匹配所有文本消息。
    # filters.Text("keyword") ：匹配包含特定关键词的文本消息。
    # filters.Regex(r"pattern") ：匹配符合正则表达式的文本消息。
    application.add_handler(MessageHandler(filters.TEXT, text_callback))

    # filters.PHOTO ：匹配图片消息。
    # filters.VIDEO ：匹配视频消息。
    application.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, handle_media_callback))

    # 启动 Bot
    logger.info("Starting Telegram Bot...")
    application.run_polling()

    # 关闭数据库连接
    close_db()


if __name__ == "__main__":
    main()
