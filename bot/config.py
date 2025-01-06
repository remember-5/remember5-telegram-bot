import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 读取配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

UPDATE_MY_COMMANDS = os.getenv("UPDATE_MY_COMMANDS")

DATABASE_URL = os.getenv("DATABASE_URL")

FILE_SAVE_PATH = os.getenv("FILE_SAVE_PATH")
