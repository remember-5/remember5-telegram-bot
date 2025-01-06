from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from telegram import Update
from telegram.ext import CallbackContext

from bot.database import SessionLocal
from bot.handlers.btn_constants import config_btn, folder_btn
from bot.models import User
from bot.utils.logger import logger  # 直接导入全局日志记录器
from bot.utils.promission_utils import check_admin


async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # 记录日志
    logger.info(f"Received /start command from user {username}, user_id: {user_id} (chat_id: {chat_id})")
    # 保存用户到数据库
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        logger.info(f"User {user}")
        if not user:
            user = User(username=username, chat_id=chat_id, user_id=user_id)
            db.add(user)
            db.commit()
            logger.info(f"New user registered: {username} (chat_id: {chat_id})")
            await update.message.reply_text(f"Welcome, {username}! You are now registered.")
        else:
            logger.info(f"Existing user logged in: {username} (chat_id: {chat_id})")
            await update.message.reply_text("Hello")

    except Exception as e:
        logger.error(f"Error saving user to database: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
    finally:
        db.close()


async def settings(update: Update, context: CallbackContext):
    """
    处理用户配置保存路径的命令。
    """
    # 创建路径配置按钮
    # 动态生成按钮数组

    # 检查用户是否为管理员
    if not check_admin(update.message.from_user.id):
        await update.message.reply_text("You do not have permission to use this command.")
        return

    keyboard = [
        [
            InlineKeyboardButton(btn["text"], callback_data=btn["callback_data"]) for btn in folder_btn.values()
        ],
        [
            InlineKeyboardButton(btn["text"], callback_data=btn["callback_data"]) for btn in config_btn.values()
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # 询问用户选择保存路径
    await update.message.reply_text("请选择：", reply_markup=reply_markup)


async def helps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /help 命令。
    """
    await update.message.reply_text("Here are the available commands:\n/start - Start the bot\n/help - Get help")


async def reply(update: Update, context: CallbackContext):
    """
    处理 /reply-keyboard 命令，发送内联键盘。
    """
    # 检查用户是否为管理员
    if not check_admin(update.message.from_user.id):
        await update.message.reply_text("You do not have permission to use this command.")
        return

    keyboard = [
        ["Option 1", "Option 2"],
        ["Option 3"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)
