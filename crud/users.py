import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security


# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data : UserRequest):
    # 密码加密
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读回最新的user
    return user

# 生成Token
async def create_token(db: AsyncSession, user_id : int):
    # 生成token ---- 设置过期时间 ---- 查询数据库是否有token --有就更新，没有新建
    token = str(uuid.uuid4())
    expirse_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expirse_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expirse_at)
        db.add(user_token)
        await db.commit()

    return  token