# Toutiao Backend - 新闻头条后端

基于 FastAPI 构建的现代化新闻头条应用后端服务，提供用户认证、新闻浏览、收藏和历史记录等完整功能。

## 📋 项目

- ✅ 用户注册/登录认证系统
- ✅ JWT Token 身份验证
- ✅ 新闻分类浏览
- ✅ 新闻列表分页查询
- ✅ 新闻详情查看（含浏览量统计）
- ✅ 相关新闻推荐
- ✅ 新闻收藏功能
- ✅ 浏览历史记录
- ✅ Redis 缓存优化
- ✅ 全局异常处理
- ✅ CORS 跨域支持
- ✅ RESTful API 设计

## 📁 项目结构

```
toutiao_backend/
├── cache/              # 缓存层
│   └── news_cache.py   # 新闻缓存操作
├── config/             # 配置文件
│   ├── cache_conf.py   # Redis 配置
│   └── db_conf.py      # 数据库配置
├── crud/               # 数据库操作层
│   ├── favorite.py     # 收藏操作
│   ├── history.py      # 历史记录操作
│   ├── news.py         # 新闻操作
│   ├── news_cache.py   # 新闻缓存装饰器
│   └── users.py        # 用户操作
├── models/             # SQLAlchemy 数据模型
│   ├── favorite.py     # 收藏模型
│   ├── history.py      # 历史模型
│   ├── news.py         # 新闻模型
│   └── users.py        # 用户模型
├── routers/            # API 路由
│   ├── favorite.py     # 收藏接口
│   ├── history.py      # 历史接口
│   ├── news.py         # 新闻接口
│   └── users.py        # 用户接口
├── schemas/            # Pydantic 数据模型
│   ├── base.py         # 基础模型
│   ├── favorite.py     # 收藏模型
│   ├── history.py      # 历史模型
│   └── users.py        # 用户模型
├── utils/              # 工具函数
│   ├── auth.py         # 认证工具
│   ├── cache_decorator.py  # 缓存装饰器
│   ├── exception.py    # 异常定义
│   ├── exception_handlers.py  # 异常处理器
│   ├── response.py     # 响应封装
│   └── security.py     # 安全工具
├── main.py             # 应用入口
├── run.py              # 启动脚本
└── requirements.txt    # 依赖包
```

## 🛠️ 环境要求

- Python 3.9+
- MySQL 5.7+ / 8.0+
- Redis 6.0+


## 🚀 运行项目

### 启动

```bash
python run.py
```


## 📖 API 文档

启动服务后，可以访问以下文档：

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔌 API 接口概览

### 用户模块 `/api/user`
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/register` | 用户注册 |
| POST | `/login` | 用户登录 |
| GET | `/info` | 获取用户信息 |
| PUT | `/update` | 更新用户信息 |
| PUT | `/password` | 修改密码 |

### 新闻模块 `/api/news`
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/categories` | 获取新闻分类 |
| GET | `/list` | 获取新闻列表 |
| GET | `/detail` | 获取新闻详情 |

### 收藏模块 `/api/favorite`
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/add` | 添加收藏 |
| DELETE | `/remove` | 取消收藏 |
| GET | `/list` | 获取收藏列表 |

### 历史模块 `/api/history`
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/add` | 添加浏览历史 |
| GET | `/list` | 获取浏览历史 |



## 📊 性能优化

- ✅ 异步数据库操作（aiomysql）
- ✅ Redis 缓存减少数据库查询
- ✅ 数据库连接池配置
- ✅ 分页查询避免大数据量加载
- ✅ 索引优化（建议在数据库中为常用查询字段添加索引）
