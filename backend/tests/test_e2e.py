"""端到端测试 - 完整用户旅程"""
import pytest
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import aiosqlite
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core import deps


@pytest.fixture
async def e2e_db():
    """E2E 测试用的内存数据库（带种子数据）"""
    conn = await aiosqlite.connect(":memory:")
    conn.row_factory = aiosqlite.Row
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        await conn.executescript(f.read())

    # 插入菜品种子数据
    dishes = [
        ("宫保鸡丁", "川菜", '["辣","下饭"]', 28, 20, 450, None, 1),
        ("白切鸡", "粤菜", '["清淡","鲜"]', 45, 30, 320, None, 1),
        ("日式咖喱饭", "日料", '["微辣","快捷"]', 35, 25, 580, None, 1),
        ("番茄牛腩", "粤菜", '["酸甜","营养"]', 55, 40, 520, None, 1),
        ("酸辣土豆丝", "川菜", '["酸","辣","下饭"]', 15, 15, 200, None, 1),
        ("三文鱼刺身", "日料", '["鲜","清淡"]', 88, 10, 250, None, 1),
        ("麻辣香锅", "川菜", '["辣","下饭"]', 42, 25, 680, None, 1),
        ("皮蛋瘦肉粥", "粤菜", '["清淡","鲜"]', 12, 15, 180, None, 1),
    ]
    for d in dishes:
        await conn.execute(
            "INSERT INTO dishes (name, cuisine, tags, reference_price, prep_time, calories, image_url, is_active) VALUES (?,?,?,?,?,?,?,?)",
            d,
        )
    await conn.commit()

    deps.set_test_db(conn)
    yield conn
    deps.set_test_db(None)
    await conn.close()


@pytest.fixture
async def app_client(e2e_db):
    """E2E HTTP 客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestFullUserJourney:
    """完整用户旅程 E2E 测试"""

    async def test_register_and_profile(self, app_client):
        """旅程1: 用户注册 → 查看信息 → 更新偏好"""
        # 1. 注册
        resp = await app_client.post("/api/users/register", json={
            "phone": "13900001234",
            "nickname": "吃货小王",
            "taste_tags": ["辣", "下饭"],
        })
        assert resp.status_code == 201
        user = resp.json()
        assert user["nickname"] == "吃货小王"
        assert "辣" in user["taste_tags"]

        # 2. 查看个人信息
        resp = await app_client.get("/api/users/me")
        assert resp.status_code == 200
        assert resp.json()["phone"] == "13900001234"

        # 3. 更新偏好
        resp = await app_client.put("/api/users/me", json={
            "nickname": "美食家小王",
            "taste_tags": ["辣", "鲜", "下饭"],
        })
        assert resp.status_code == 200
        assert resp.json()["nickname"] == "美食家小王"
        assert len(resp.json()["taste_tags"]) == 3

    async def test_recommend_flow(self, app_client):
        """旅程2: 随机推荐 → 筛选推荐 → 快捷推荐"""
        # 1. 无筛选推荐
        resp = await app_client.post("/api/recommend")
        assert resp.status_code == 200
        data = resp.json()
        assert data["dish"]["is_active"] is True
        assert len(data["reason"]) > 0

        # 2. 按菜系筛选
        resp = await app_client.post("/api/recommend", json={"cuisine": "川菜"})
        assert resp.status_code == 200
        assert resp.json()["dish"]["cuisine"] == "川菜"

        # 3. 按价格筛选
        resp = await app_client.post("/api/recommend", json={"price_range": "¥20-50"})
        assert resp.status_code == 200
        price = resp.json()["dish"]["reference_price"]
        assert 20 <= price < 50

        # 4. 快捷推荐 - 我超饿
        resp = await app_client.post("/api/recommend/quick/hungry")
        assert resp.status_code == 200
        assert resp.json()["dish"]["prep_time"] <= 25

        # 5. 快捷推荐 - 清理冰箱
        resp = await app_client.post("/api/recommend/quick/fridge")
        assert resp.status_code == 200

    async def test_record_meal_journey(self, app_client):
        """旅程3: 记录饮食 → 查看 → 修改 → 删除"""
        today = str(date.today())

        # 1. 记录早餐
        resp = await app_client.post("/api/records", json={
            "dish_name": "皮蛋瘦肉粥",
            "meal_type": "早餐",
            "location_name": "永和豆浆",
            "cost": 12,
            "calories": 180,
            "rating": 5,
            "meal_date": today,
        })
        assert resp.status_code == 201
        breakfast_id = resp.json()["id"]

        # 2. 记录午餐
        resp = await app_client.post("/api/records", json={
            "dish_name": "宫保鸡丁",
            "meal_type": "午餐",
            "location_name": "川味小馆",
            "cost": 28,
            "calories": 450,
            "rating": 4,
            "meal_date": today,
            "note": "微辣，好吃",
        })
        assert resp.status_code == 201
        lunch_id = resp.json()["id"]

        # 3. 查看单条记录
        resp = await app_client.get(f"/api/records/{breakfast_id}")
        assert resp.status_code == 200
        assert resp.json()["dish_name"] == "皮蛋瘦肉粥"

        # 4. 修改记录
        resp = await app_client.put(f"/api/records/{lunch_id}", json={
            "rating": 5,
            "note": "非常好吃！下次还来",
        })
        assert resp.status_code == 200
        assert resp.json()["rating"] == 5

        # 5. 查看列表（应有2条）
        resp = await app_client.get("/api/records")
        assert resp.json()["total"] == 2

        # 6. 删除早餐记录
        resp = await app_client.delete(f"/api/records/{breakfast_id}")
        assert resp.status_code == 204

        # 7. 确认只剩1条
        resp = await app_client.get("/api/records")
        assert resp.json()["total"] == 1

    async def test_feedback_and_recommend_optimize(self, app_client):
        """旅程4: 对推荐菜品反馈 → 影响后续推荐"""
        # 1. 推荐一道菜
        resp = await app_client.post("/api/recommend")
        dish = resp.json()["dish"]

        # 2. 提交喜欢反馈
        resp = await app_client.post("/api/feedback", json={
            "dish_id": dish["id"],
            "action": "like",
        })
        assert resp.status_code == 201

        # 3. 再推荐一道
        resp = await app_client.post("/api/recommend")
        dish2 = resp.json()["dish"]

        # 4. 提交不喜欢反馈
        resp = await app_client.post("/api/feedback", json={
            "dish_id": dish2["id"],
            "action": "dislike",
        })
        assert resp.status_code == 201

    async def test_history_and_search(self, app_client):
        """旅程5: 记录多条 → 查看日历 → 时间轴 → 搜索"""
        # 1. 记录跨日期的多条数据
        dates = [
            str(date.today()),
            str(date.today() - timedelta(days=1)),
            str(date.today() - timedelta(days=2)),
        ]
        for i, d in enumerate(dates):
            await app_client.post("/api/records", json={
                "dish_name": f"测试菜{i}",
                "meal_type": "午餐",
                "location_name": "测试餐厅",
                "cost": 30,
                "rating": 4,
                "meal_date": d,
            })

        # 2. 查看日历
        today = date.today()
        resp = await app_client.get(f"/api/history/calendar?year={today.year}&month={today.month}")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        # 3. 查看时间轴
        resp = await app_client.get("/api/history/timeline")
        assert resp.status_code == 200
        assert resp.json()["total"] >= 3

        # 4. 搜索
        resp = await app_client.get("/api/history/search?keyword=测试菜")
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

        # 5. 按地点搜索
        resp = await app_client.get("/api/history/search?location=测试餐厅")
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    async def test_statistics_after_recording(self, app_client):
        """旅程6: 记录数据后查看统计"""
        today = str(date.today())

        # 1. 记录几条数据
        meals = [
            ("宫保鸡丁", "午餐", "川味小馆", 28, 450, 4),
            ("白切鸡", "晚餐", "粤菜馆", 45, 320, 5),
            ("日式咖喱饭", "午餐", "一兰拉面", 35, 580, 4),
        ]
        for name, meal_type, loc, cost, cal, rating in meals:
            await app_client.post("/api/records", json={
                "dish_name": name,
                "meal_type": meal_type,
                "location_name": loc,
                "cost": cost,
                "calories": cal,
                "rating": rating,
                "meal_date": today,
            })

        # 2. 查看本周统计
        resp = await app_client.get("/api/statistics?period=week")
        assert resp.status_code == 200
        stats = resp.json()

        # 3. 验证统计有数据
        assert len(stats["weekly_cost"]) >= 1
        assert len(stats["category_distribution"]) >= 1
        assert len(stats["favorite_dishes"]) >= 1
        assert len(stats["top_locations"]) >= 1

        # 4. 验证花费总和
        total_cost = sum(item["cost"] for item in stats["weekly_cost"])
        assert total_cost == 28 + 45 + 35

    async def test_health_check(self, app_client):
        """健康检查接口"""
        resp = await app_client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
