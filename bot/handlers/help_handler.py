from telegram import Update
from telegram.ext import ContextTypes

async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /help 命令。
    """
    await update.message.reply_text("Here are the available commands:\n/start - Start the bot\n/help - Get help")
