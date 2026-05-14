from typing import Any

import redis.asyncio as redis
import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "*******"

# Redis connection
redis_client = redis.Redis(
    host=REDIS_HOST, # redis 服务器主机地址
    port=REDIS_PORT, # redis 端口号
    db=REDIS_DB, # redis 数据库索引号  0-15
    decode_responses= True,  # 返回结果为字符串类型
    password=REDIS_PASSWORD
)

# 设置 ---- 读取（字符串   列表和字典）“【{}】”
# 读取：字符串
async def get_cache(key: str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None
# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            # 序列化
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败：{e}")
        return None

# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存储
            value = json.dumps(value, ensure_ascii=False) #中文正常报存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
