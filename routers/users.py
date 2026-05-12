from starlette import status
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas import users
from crud import users


router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: users.UserRequest,db: AsyncSession = Depends(get_db)):
    # 验证用户存在----不存在则创建----生成token----响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    return {
        "code": "200",
        "msg": "注册成功",
        "data": {
            "token" : "jwt",
            "userInfo" : {
                "id" : user.id,
                "username" : user.username,
                "bio" : user.bio,
                "avatar" : user.avatar,
            }
        }
    }