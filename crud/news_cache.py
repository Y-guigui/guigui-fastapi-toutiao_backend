from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cache_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category, News
from schemas.base import NewsItemBase
from utils.cache_decorator import async_cache

# async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
#     # 去缓存中获取数据
#     cache_categories = await get_cache_categories()
#     if cache_categories:
#         return cache_categories
#     # 如果缓存中没有数据，就去数据库里面查
#     stmt = select(Category).offset(skip).limit(limit)
#     result = await db.execute(stmt)
#     categories = result.scalars().all() #ORM
#     # 写入缓存
#     if categories:
#         categories = jsonable_encoder(categories)
#         await set_cache_categories(categories)
#     # 返回数据
#     return  categories

@async_cache(key_prefix="news:categories", expire=7200)
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
#     # 查询的是指定分类下的所有新闻
#     # 去缓存中获取数据
#     page = skip // limit + 1
#     size = limit
#     cache_news_list = await get_cache_news_list(category_id, page, size)  #json格式
#     if cache_news_list:
#         # return cache_news_list  #orm格式
#         return [News(**item) for item in cache_news_list]
#     # 如果缓存中没有数据，就去数据库里面查
#     stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
#     result = await db.execute(stmt)
#     news_list =  result.scalars().all()
#     # 写入缓存
#     if news_list:
#         # ORM 转成 dict
#         # orm ---> pydantic ----> dict
#         news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
#
#         await set_cache_news_list(category_id, page, size, news_data)
#     # 返回数据
#     return news_list

@async_cache(key_prefix="news_list", expire=600)
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询的是指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错


async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 更新 → 检查数据库是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # order_by 排序 → 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),  # 默认是升序，desc 表示降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式 推导出新闻的核心数据，然后再 return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]