import os
import requests
from bot.database import SessionLocal
from bot.models.video import Video
from bot.utils.logger import setup_logger

logger = setup_logger()

def save_video_to_db(file_id: str, file_name: str, file_path: str):
    """
    将视频信息保存到数据库。
    """
    db = SessionLocal()
    try:
        video = Video(file_id=file_id, file_name=file_name, file_path=file_path)
        db.add(video)
        db.commit()
        logger.info(f"Video saved to database: {file_name}")
    except Exception as e:
        logger.error(f"Error saving video to database: {e}")
        db.rollback()
    finally:
        db.close()

async def download_video(file_id: str, file_path: str, bot):
    """
    下载视频文件并保存到本地。
    """
    # 确保 downloads 目录存在
    os.makedirs("downloads", exist_ok=True)

    # 下载视频
    file = await bot.get_file(file_id)
    file_url = file.file_path
    response = requests.get(file_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    logger.info(f"Video downloaded to: {file_path}")
