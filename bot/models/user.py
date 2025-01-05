from sqlalchemy import Column, Integer, String, Boolean
from bot.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=True)  # 允许 username 为空
    chat_id = Column(Integer, unique=True, index=True)
    is_admin = Column(Boolean, default=False)  # 新增字段
