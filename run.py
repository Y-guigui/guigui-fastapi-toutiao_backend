import uvicorn

if __name__ == "__main__":
    # 运行 FastAPI 应用
    # "main:app" 表示加载 main.py 文件中的 app 对象
    # reload=True 表示开启热更新，修改代码后服务器会自动重启，适合开发环境
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # 开启热更新，修改代码后会自动重启
    )