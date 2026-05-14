from functools import wraps
from typing import Callable, Any
from fastapi.encoders import jsonable_encoder
from config.cache_conf import get_json_cache, set_cache

def async_cache(key_prefix: str, expire: int = 3600):
    """
    通用异步缓存装饰器
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 动态生成Cache Key ，过滤db session这种不能用于key的对象
            key_parts = [f"{k}:{v}" for k, v in kwargs.items() if k != 'db' ]
            cache_key = f"{key_prefix}:{func.__name__}:{'-'.join(key_parts)}"
            # 尝试获取缓存
            cache_data = await get_json_cache(cache_key)
            if cache_data:
                return cache_data
            # 缓存未命中，执行原本的数据库查询函数
            result = await func(*args, **kwargs)

            # 如果查到了数据，写入缓存
            if result:
                cache_data = jsonable_encoder(result)
                await set_cache(cache_key, cache_data, expire)

            return  result
        return wrapper
    return decorator


