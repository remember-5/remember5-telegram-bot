from bot.database import Base
from sqlalchemy import Column, Integer, String

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String, unique=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
