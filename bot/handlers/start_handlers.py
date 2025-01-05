from telegram import Update
from telegram.ext import CallbackContext

from bot.database import SessionLocal
from bot.models import User
from bot.utils.logger import logger  # 直接导入全局日志记录器

# 处理 /start 命令
async def handler_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    # 记录日志
    logger.info(f"Received /start command from user {username} (chat_id: {chat_id})")

    # 保存用户到数据库
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        logger.info(f"User {user}")
        if not user:
            user = User(username=username, chat_id=chat_id)
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
