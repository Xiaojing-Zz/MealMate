# MealMate（餐伴）- 架构设计文档

## 系统架构

```mermaid
graph TB
    subgraph 前端["前端 (Vue 3 + Vant)"]
        B1[推荐页]
        B2[记录页]
        B3[历史页]
        B4[统计页]
        B5[个人中心]
    end

    subgraph 后端["后端 (FastAPI)"]
        R1[用户路由]
        R2[推荐路由]
        R3[记录路由]
        R4[历史路由]
        R5[统计路由]
        R6[反馈路由]
    end

    subgraph 数据层["数据层 (SQLite)"]
        DB[(SQLite)]
    end

    前端 -->|"HTTP /api/*"| 后端
    后端 -->|"aiosqlite"| 数据层
```

## 前端架构

### 页面路由

```mermaid
graph LR
    A["/"] --> B["/recommend<br/>推荐"]
    A --> C["/record<br/>记录"]
    A --> D["/history<br/>历史"]
    A --> E["/statistics<br/>统计"]
    A --> F["/profile<br/>我的"]
```

### 组件结构

```mermaid
graph TB
    App["App.vue<br/>底部导航栏"]
    App --> Recommend["RecommendView.vue<br/>筛选栏 + 快捷入口 + 结果卡片"]
    App --> Record["RecordView.vue<br/>表单（类型/名称/地点/花费/评分/日期）"]
    App --> History["HistoryView.vue<br/>日历视图 + 时间轴视图"]
    App --> Stats["StatisticsView.vue<br/>柱状图 + 品类 + 地点 + 排行"]
    App --> Profile["ProfileView.vue<br/>用户卡片 + 偏好 + 管理"]
```

### 状态管理

使用 Pinia 管理全局状态：

| Store | 状态 | 用途 |
|-------|------|------|
| user | user, isLoggedIn | 用户信息和登录状态 |

## 后端架构

### 分层结构

```mermaid
graph TB
    Client["客户端请求"]
    Router["路由层 routers/"]
    Service["服务层 services/"]
    Model["数据模型 models/"]
    DB["SQLite 数据库"]

    Client --> Router
    Router --> Service
    Router --> Model
    Service --> Model
    Service --> DB
```

| 层级 | 职责 | 文件 |
|------|------|------|
| 路由层 | 接收 HTTP 请求，参数校验，调用服务 | routers/*.py |
| 服务层 | 业务逻辑（预留扩展） | services/ |
| 数据模型 | Pydantic 类型定义，请求/响应格式 | models/schemas.py |
| 依赖注入 | 数据库连接管理 | core/deps.py |

### API 路由一览

```mermaid
graph LR
    API["/api"] --> U["/users"]
    API --> R["/recommend"]
    API --> REC["/records"]
    API --> H["/history"]
    API --> S["/statistics"]
    API --> F["/feedback"]
    API --> HC["/health"]

    U --> U1["POST /register"]
    U --> U2["GET /me"]
    U --> U3["PUT /me"]

    R --> R1["POST /"]
    R --> R2["POST /quick/:scenario"]

    REC --> REC1["POST /"]
    REC --> REC2["GET /"]
    REC --> REC3["GET /:id"]
    REC --> REC4["PUT /:id"]
    REC --> REC5["DELETE /:id"]

    H --> H1["GET /calendar"]
    H --> H2["GET /timeline"]
    H --> H3["GET /search"]

    S --> S1["GET /"]

    F --> F1["POST /"]
```

## 数据库设计

详见 [ER-DIAGRAM.md](./ER-DIAGRAM.md)

### 核心表

| 表 | 行数（预估） | 增长率 |
|----|-------------|--------|
| users | O(千) | 低 |
| dishes | O(百) | 低（管理维护） |
| meal_records | O(万/用户) | 高（每餐1-3条） |
| user_feedback | O(千/用户) | 中 |

## 推荐算法

```mermaid
flowchart TD
    A[接收推荐请求] --> B{有筛选条件?}
    B -->|是| C[构建 WHERE 查询]
    B -->|否| D[查询全部启用菜品]
    C --> E[执行数据库查询]
    D --> E
    E --> F{有结果?}
    F -->|是| G[随机选择一道]
    F -->|否| H[返回 404]
    G --> I[生成推荐理由]
    I --> J[返回菜品 + 理由]
```

### 筛选逻辑

| 维度 | 查询方式 |
|------|----------|
| 菜系 | `WHERE cuisine = ?` |
| 口味 | `WHERE tags LIKE '%辣%'` |
| 价格 | `WHERE reference_price >= ? AND reference_price < ?` |
| 热量 | `WHERE calories >= ? AND calories < ?` |
| 场景-超饿 | `WHERE prep_time <= 25` |
| 场景-清理冰箱 | `WHERE prep_time <= 20` |

### 未来优化方向

1. **基于用户偏好**：结合 `users.taste_tags` 加权推荐
2. **基于历史反馈**：低评分菜品降低推荐权重
3. **避免重复**：排除近 7 天已吃过的同类菜品
4. **协同过滤**：相似用户喜欢的菜品推荐

## 技术选型详解

### 为什么选 FastAPI

- 原生 async/await 支持，与 aiosqlite 完美匹配
- 自动生成 OpenAPI/Swagger 文档
- Pydantic 集成，请求自动校验
- 性能优于 Flask，开发效率优于 Django

### 为什么选 SQLite

- 零配置，无需安装数据库服务
- 单文件存储，部署简单
- 足够支撑个人/小团队使用
- 后期可无缝迁移到 PostgreSQL

### 为什么选 Vue 3 + Vant

- Vue 3 Composition API 灵活高效
- Vant 专为移动端设计，组件丰富
- Vite 构建速度极快
- 生态成熟，社区活跃

## 部署架构

```mermaid
graph TB
    subgraph 服务器
        Nginx["Nginx 反向代理"]
        FE["前端静态文件"]
        BE["FastAPI + Uvicorn"]
        DB[("SQLite 数据库")]
    end

    User["用户浏览器"] --> Nginx
    Nginx --> FE
    Nginx --> BE
    BE --> DB
```

### 部署步骤

```bash
# 1. 构建前端
cd frontend && npm run build

# 2. 配置 Nginx
# 将 frontend/dist 指向静态文件
# 将 /api 代理到 uvicorn

# 3. 启动后端
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
