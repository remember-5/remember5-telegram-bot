from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bot.config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建基础类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化数据库
def init_db():
    Base.metadata.create_all(bind=engine)

# 关闭数据库
def close_db():
    engine.dispose()
