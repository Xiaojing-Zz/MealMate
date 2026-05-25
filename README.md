# MealMate（餐伴）

> 不再纠结吃什么，每顿饭都有一个懂你的伴侣帮你决定、帮你记住。

## 项目简介

MealMate（餐伴）是一款解决"今天吃什么"选择困难的智能决策助手，同时提供饮食记录功能，帮助用户形成健康的饮食习惯。

### 核心功能

- **随机推荐** — 一键盲选/多维度筛选/场景快捷入口
- **饮食记录** — 快速记录菜品、花费、评分、地点
- **历史回顾** — 日历视图、时间轴浏览、搜索筛选
- **统计分析** — 花费趋势、品类分布、热量追踪、排行
- **个人中心** — 口味偏好设置、数据管理

## 技术选型

| 层级 | 技术 | 选型理由 |
|------|------|----------|
| 后端框架 | FastAPI | 异步支持好，自动生成 OpenAPI 文档，Python 生态 |
| 数据库 | SQLite | 轻量级，无需安装服务，适合开发和中小规模部署 |
| 数据库驱动 | aiosqlite | 异步 SQLite 驱动，与 FastAPI 异步架构匹配 |
| 数据校验 | Pydantic v2 | FastAPI 原生集成，自动请求/响应校验 |
| 前端框架 | Vue 3 | Composition API，响应式，生态成熟 |
| 移动端 UI 库 | Vant 4 | 专为移动端设计，组件丰富 |
| 前端构建工具 | Vite | 极速 HMR，原生 ESM 支持 |
| 状态管理 | Pinia | Vue 3 官方推荐，轻量级 |
| HTTP 客户端 | Axios | 拦截器机制，请求/响应转换 |
| 图表 | ECharts | 功能强大的图表库 |
| 测试框架 | pytest + pytest-asyncio | Python 异步测试标准方案 |
| HTTP 测试 | httpx | 支持异步 ASGI 测试 |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 或 yarn

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -c "import asyncio; from app.core.deps import init_db; asyncio.run(init_db())"

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后访问：
- API 服务：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端默认运行在 http://localhost:5173

### 运行测试

```bash
cd backend

# 运行全部测试（50个用例）
pytest tests/ -v

# 运行单元测试
pytest tests/test_users.py tests/test_recommend.py tests/test_records.py tests/test_feedback.py tests/test_statistics.py -v

# 运行端到端测试
pytest tests/test_e2e.py -v
```

## 项目结构

```
MealMate/
├── README.md
├── .gitignore
├── backend/                    # 后端
│   ├── app/
│   │   ├── main.py             # FastAPI 应用入口
│   │   ├── models/
│   │   │   ├── schemas.py      # Pydantic 数据模型
│   │   │   └── __init__.py
│   │   ├── routers/
│   │   │   ├── users.py        # 用户 API
│   │   │   ├── recommend.py    # 推荐 API
│   │   │   ├── records.py      # 饮食记录 API
│   │   │   ├── history.py      # 历史回顾 API
│   │   │   ├── statistics.py   # 统计分析 API
│   │   │   └── feedback.py     # 用户反馈 API
│   │   ├── services/           # 业务服务层（预留）
│   │   └── core/
│   │       ├── deps.py         # 依赖注入（数据库连接）
│   │       └── database.py     # 数据库初始化
│   ├── tests/                  # 测试
│   │   ├── conftest.py         # 测试配置
│   │   ├── test_users.py       # 用户模块测试
│   │   ├── test_recommend.py   # 推荐模块测试
│   │   ├── test_records.py     # 记录模块测试
│   │   ├── test_feedback.py    # 反馈模块测试
│   │   ├── test_statistics.py  # 统计+历史测试
│   │   └── test_e2e.py         # 端到端测试
│   ├── schema.sql              # 数据库 Schema
│   ├── requirements.txt        # Python 依赖
│   └── pytest.ini              # 测试配置
├── frontend/                   # 前端
│   ├── src/
│   │   ├── main.js             # 入口
│   │   ├── App.vue             # 根组件（底部导航）
│   │   ├── router/index.js     # 路由配置
│   │   ├── store/index.js      # Pinia 状态管理
│   │   ├── assets/global.css   # 全局样式
│   │   └── views/
│   │       ├── RecommendView.vue  # 推荐页
│   │       ├── RecordView.vue     # 记录页
│   │       ├── HistoryView.vue    # 历史页
│   │       ├── StatisticsView.vue # 统计页
│   │       └── ProfileView.vue    # 个人中心
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── docs/                       # 文档
    ├── PRD.md                  # 产品需求文档
    ├── ER-DIAGRAM.md           # ER 图
    ├── API.md                  # API 接口文档
    ├── ARCHITECTURE.md         # 架构设计文档
    └── TESTING.md              # 测试文档
```

## GitHub 账号

- 仓库地址：https://github.com/Xiaojing-Zz/MealMate
- 账号：Xiaojing-Zz

## 开发流程

本项目严格遵循 **SDD → DDD → TDD → E2E** 四阶段开发范式：

1. **SDD（契约驱动）** — 先定义数据模型和 API 契约
2. **DDD（设计驱动）** — 先设计 UI 组件再实现
3. **TDD（测试驱动）** — 先写测试再写实现（红-绿-重构）
4. **E2E（端到端）** — 完整用户旅程测试

## 许可证

MIT
