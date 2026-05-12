from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的源，默认为*， 企业需要指定源origins
    allow_credentials=True, # 允许携带的cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 注册路由
app.include_router(news.router)
app.include_router(users.router)