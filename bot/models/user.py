from sqlalchemy import Column, Integer, String, Boolean
from bot.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, index=True) # user_id
    username = Column(String, unique=True, index=True, nullable=True)  # username
    chat_id = Column(Integer, unique=True, index=True) # chat_id
    is_admin = Column(Boolean, default=False)  # is_admin
