import os
from telegram import Update
from telegram.ext import CallbackContext
from bot.utils import logger
from bot.utils.download_utils import download_small_file, download_large_file


# 全局变量，用于存储媒体组消息
media_group_cache = {}


async def handle_media_group(update: Update, context: CallbackContext, media_group_id: str, save_path: str):
    """
    处理媒体组消息。
    """
    global media_group_cache

    # 初始化媒体组缓存
    if media_group_id not in media_group_cache:
        media_group_cache[media_group_id] = []

    # 将当前消息添加到媒体组缓存
    if update.message.photo:
        file_id = update.message.photo[-1].file_id  # 获取最高分辨率的图片
        file_name = f"photo_{file_id}.jpg"
        media_group_cache[media_group_id].append((file_id, file_name, "photo"))
    elif update.message.video:
        file_id = update.message.video.file_id
        file_name = f"video_{file_id}.mp4"
        media_group_cache[media_group_id].append((file_id, file_name, "video"))

    # 检查媒体组是否完整（假设媒体组最多包含 10 个文件）
    if len(media_group_cache[media_group_id]) >= 10:
        # 下载媒体组中的所有文件
        for file_id, file_name, file_type in media_group_cache[media_group_id]:
            file_path = os.path.join(save_path, file_name)
            if file_type == "photo":
                await download_small_file(file_id, file_path, context.bot)
                logger.info(f"图片已下载: {file_path}")
            elif file_type == "video":
                await download_large_file(file_id, file_path, context.bot)
                logger.info(f"视频已下载: {file_path}")

        # 回复用户
        await update.message.reply_text(f"媒体组中的文件已全部下载到: {save_path}")

        # 清除缓存
        del media_group_cache[media_group_id]

async def handle_media(update: Update, context: CallbackContext):
    """
    处理用户转发的图片或视频。
    """
    # 获取默认下载路径
    save_path = context.user_data.get("save_path", "downloads")
    # 检查路径是否存在
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    if update.message.media_group_id:
        # 处理媒体组
        media_group_id = update.message.media_group_id
        logger.info(f"检测到媒体组消息，media_group_id: {media_group_id}")
        await handle_media_group(update, context, media_group_id, save_path)

    else:
        # 处理单个文件
        if update.message.photo:
            # 下载图片
            file_id = update.message.photo[-1].file_id
            file_name = f"photo_{file_id}.jpg"
            file_path = os.path.join(save_path, file_name)
            await download_small_file(file_id, file_path, context.bot)
            logger.info(f"图片已下载: {file_path}")
            await update.message.reply_text(f'图片已下载到: {file_path}')

        elif update.message.video:
            # 下载视频
            file_id = update.message.video.file_id
            file_name = f"video_{file_id}.mp4"
            file_path = os.path.join(save_path, file_name)
            await download_large_file(file_id, file_path, context.bot)
            logger.info(f"视频已下载: {file_path}")
            await update.message.reply_text(f'视频已下载到: {file_path}')

        else:
            await update.message.reply_text('请发送一个图片或视频文件。')
