from bot.database import SessionLocal
from bot.models import User

def check_admin(user_id: int) -> bool:
    """
    检查用户是否为管理员。
    :param user_id: 用户的 user_id
    :return: 如果是管理员返回 True，否则返回 False
    """
    with SessionLocal() as db:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user and user.is_admin:
            return True
        return False
