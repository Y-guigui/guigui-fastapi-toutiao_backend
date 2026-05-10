from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news

# 创建 APIRouter 实例
# prefix-路由前缀  tags分组
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 获取数据库数据  --  定义模型类  --  封装crud方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": "200",
        "msg": "获取新闻分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, le=100,  alias="pageSize"),
        db: AsyncSession = Depends(get_db),
):
    # 分页 -- 查询新闻列表 -- 计算总量 -- 计算是否hasMore
    offset = (page - 1) * page_size
    limit = page_size
    news_list = await news.get_news_list(db, category_id, offset, limit)
    total = await news.get_news_count(db, category_id)
    # 跳过的 + 当前的数量 < 总量
    has_more = (offset + len(news_list)) < total
    return {
        "code": "200",
        "msg": "获取新闻分类成功",
        "data": {
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }