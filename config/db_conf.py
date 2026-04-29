from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 输出 SQL 日志
    pool_size=10,  # 设置连接池中保持的持久连接数
    max_overflow=20, # 设置连接池允许创建的额外连接数
)

# 创建异步会话工厂
AsyncioSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 依赖项
async def get_db():
    async with AsyncioSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()