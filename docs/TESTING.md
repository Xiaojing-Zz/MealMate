# MealMate（餐伴）- 测试文档

## 测试策略

本项目采用 **TDD（测试驱动开发）** 范式，先写测试再写实现。

```mermaid
graph LR
    A[编写测试 红灯] --> B[编写实现 绿灯]
    B --> C[重构优化]
    C --> A

    style A fill:#ff6b6b,color:#fff
    style B fill:#51cf66,color:#fff
    style C fill:#339af0,color:#fff
```

## 测试架构

```mermaid
graph TB
    T[测试金字塔 50个用例]

    T --> E2E["E2E 端到端测试 (7)"]
    T --> UNIT["单元测试 (43)"]

    E2E --> E1[注册→偏好旅程]
    E2E --> E2[推荐流程旅程]
    E2E --> E3[记录CRUD旅程]
    E2E --> E4[反馈旅程]
    E2E --> E5[历史搜索旅程]
    E2E --> E6[统计分析旅程]
    E2E --> E7[健康检查]

    UNIT --> U1[用户模块 (6)]
    UNIT --> U2[推荐模块 (10)]
    UNIT --> U3[记录模块 (13)]
    UNIT --> U4[反馈模块 (5)]
    UNIT --> U5[统计历史 (9)]
```

## 测试环境

| 组件 | 说明 |
|------|------|
| 测试框架 | pytest 8.3 |
| 异步支持 | pytest-asyncio 0.24 |
| HTTP 客户端 | httpx（ASGITransport） |
| 数据库 | SQLite 内存数据库（每个测试独立） |
| 依赖注入 | 通过 `deps.set_test_db()` 注入测试数据库 |

## 测试配置

**conftest.py** 提供以下 fixture：

| Fixture | 说明 |
|---------|------|
| `db` | 创建内存数据库，注入 Schema，每个测试独立 |
| `client` | HTTP 测试客户端，基于 ASGI transport |
| `seed_dishes` | 插入 5 条测试菜品数据（含 1 条已下架） |

## 测试用例清单

### 单元测试 (43个)

#### 用户模块 - test_users.py (6个)

| 用例 | 说明 | 断言 |
|------|------|------|
| test_register_success | 注册成功 | 返回 201，包含 id 和 phone |
| test_register_duplicate_phone | 重复手机号 | 返回 400 |
| test_register_missing_fields | 缺少必填字段 | 返回 422 |
| test_register_with_taste_tags | 注册携带口味标签 | taste_tags 正确 |
| test_get_current_user | 获取当前用户 | 返回正确 nickname |
| test_update_user | 更新用户信息 | nickname 和 taste_tags 更新 |

#### 推荐模块 - test_recommend.py (10个)

| 用例 | 说明 | 断言 |
|------|------|------|
| test_recommend_returns_dish | 无筛选推荐 | 返回 dish 和 reason，is_active=true |
| test_recommend_with_cuisine_filter | 按菜系筛选 | cuisine 匹配 |
| test_recommend_with_taste_filter | 按口味筛选 | tags 含辣或 cuisine=川菜 |
| test_recommend_with_price_filter | 按价格筛选 | reference_price 在范围内 |
| test_recommend_excludes_inactive | 排除下架菜品 | 20次推荐不含已下架菜品 |
| test_recommend_no_match | 无匹配条件 | 返回 200 或 404 |
| test_quick_hungry | 我超饿 | prep_time <= 25 |
| test_quick_casual | 随便就行 | 返回 200 |
| test_quick_fridge | 清理冰箱 | 返回 200 |
| test_quick_invalid_scenario | 无效场景 | 返回 404 |

#### 记录模块 - test_records.py (13个)

| 用例 | 说明 | 断言 |
|------|------|------|
| test_create_record_success | 创建记录 | 返回 201，字段正确 |
| test_create_record_full_fields | 完整字段创建 | cost/calories/location 正确 |
| test_create_record_missing_required | 缺必填字段 | 返回 422 |
| test_create_record_invalid_rating | 评分超范围 | 返回 422 |
| test_create_record_invalid_meal_type | 无效用餐类型 | 返回 422 |
| test_list_records_empty | 空列表 | total=0, items=[] |
| test_list_records_with_data | 有数据列表 | total=2 |
| test_list_records_pagination | 分页 | total=5, items=2 |
| test_list_records_filter_by_date | 日期筛选 | total=1 |
| test_get_record | 获取单条 | dish_name 正确 |
| test_get_record_not_found | 记录不存在 | 返回 404 |
| test_update_record | 更新记录 | 字段已更新 |
| test_delete_record | 删除记录 | 返回 204，再次获取返回 404 |

#### 反馈模块 - test_feedback.py (5个)

| 用例 | 说明 | 断言 |
|------|------|------|
| test_create_like_feedback | 喜欢反馈 | action=like |
| test_create_dislike_feedback | 不喜欢反馈 | action=dislike |
| test_create_accept_feedback | 接受反馈 | action=accept |
| test_feedback_invalid_dish | 菜品不存在 | 返回 404 |
| test_feedback_invalid_action | 无效动作 | 返回 422 |

#### 统计历史模块 - test_statistics.py (9个)

| 用例 | 说明 | 断言 |
|------|------|------|
| test_get_statistics_empty | 空统计 | 包含所有统计字段 |
| test_get_statistics_week | 本周统计 | 返回 200 |
| test_get_statistics_month | 本月统计 | 返回 200 |
| test_get_statistics_custom | 自定义周期 | 返回 200 |
| test_get_calendar | 日历视图 | 返回 200 |
| test_get_timeline | 时间轴 | 返回 200 |
| test_get_timeline_pagination | 时间轴分页 | 返回 200 |
| test_search_records | 搜索记录 | 找到匹配记录 |
| test_search_by_location | 按地点搜索 | 返回 200 |

### E2E 端到端测试 (7个)

#### test_e2e.py

| 用例 | 用户旅程 | 步骤 |
|------|----------|------|
| test_register_and_profile | 注册→查看→更新 | 注册 → GET /me → PUT /me |
| test_recommend_flow | 推荐全流程 | 无筛选 → 菜系筛选 → 价格筛选 → 快捷推荐 |
| test_record_meal_journey | 记录全流程 | 创建 → 查看 → 修改 → 列表 → 删除 |
| test_feedback_and_recommend_optimize | 反馈流程 | 推荐 → like反馈 → 推荐 → dislike反馈 |
| test_history_and_search | 历史搜索 | 记录多条 → 日历 → 时间轴 → 搜索 |
| test_statistics_after_recording | 统计验证 | 记录 → 统计 → 验证花费总和 |
| test_health_check | 健康检查 | GET /api/health |

## 运行测试

```bash
cd backend

# 运行全部测试
pytest tests/ -v

# 运行单元测试
pytest tests/test_users.py tests/test_recommend.py tests/test_records.py tests/test_feedback.py tests/test_statistics.py -v

# 运行 E2E 测试
pytest tests/test_e2e.py -v

# 带覆盖率报告
pip install pytest-cov
pytest tests/ --cov=app --cov-report=term-missing
```

## 测试结果

```
50 passed, 5 warnings in 0.84s
```

| 类型 | 数量 | 通过率 |
|------|------|--------|
| 单元测试 | 43 | 100% |
| E2E 测试 | 7 | 100% |
| **总计** | **50** | **100%** |
