from fastapi import FastAPI, APIRouter

# 创建 APIRouter 实例
# prefix-路由前缀  tags分组
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg": "success"}