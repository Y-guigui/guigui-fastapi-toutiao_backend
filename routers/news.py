from fastapi import APIRouter, Depends, Query, HTTPException
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
        "code": 200,
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
        "code": 200,
        "msg": "获取新闻列表成功",
        "data": {
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

@router.get("/detail")
async def get_news_detail(
        news_id: int = Query(..., alias="id"),
        db: AsyncSession = Depends(get_db),
):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(db, news_id)
    if news_detail is None:
        raise HTTPException(status_code=404, detail="新闻不存在")

    view_res = await news.increase_news_views(db, news_detail.id)
    if not view_res:
        raise HTTPException(status_code=404, detail="新闻不存在")
    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id,5)
    
    return {
      "code": 200,
      "message": "success",
      "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
      }
    }