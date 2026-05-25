"""统计分析模块测试用例"""
import pytest
from datetime import date


class TestStatistics:
    """统计数据测试"""

    async def test_get_statistics_empty(self, client):
        """无数据时返回空统计"""
        resp = await client.get("/api/statistics")
        assert resp.status_code == 200
        data = resp.json()
        assert "weekly_cost" in data
        assert "category_distribution" in data
        assert "calorie_trend" in data
        assert "top_locations" in data
        assert "favorite_dishes" in data

    async def test_get_statistics_week(self, client):
        """本周统计数据"""
        # 先创建几条记录
        for i in range(3):
            await client.post("/api/records", json={
                "dish_name": f"测试菜{i}",
                "meal_type": "午餐",
                "location_name": "测试餐厅",
                "cost": 30 + i * 10,
                "calories": 400,
                "rating": 4,
                "meal_date": str(date.today()),
            })
        resp = await client.get("/api/statistics?period=week")
        assert resp.status_code == 200

    async def test_get_statistics_month(self, client):
        """本月统计数据"""
        resp = await client.get("/api/statistics?period=month")
        assert resp.status_code == 200

    async def test_get_statistics_custom(self, client):
        """自定义周期统计"""
        resp = await client.get("/api/statistics?period=custom&start_date=2024-01-01&end_date=2024-01-31")
        assert resp.status_code == 200


class TestHistory:
    """历史回顾测试"""

    async def test_get_calendar(self, client):
        """日历视图"""
        resp = await client.get("/api/history/calendar?year=2024&month=1")
        assert resp.status_code == 200

    async def test_get_timeline(self, client):
        """时间轴视图"""
        resp = await client.get("/api/history/timeline")
        assert resp.status_code == 200

    async def test_get_timeline_pagination(self, client):
        """时间轴分页"""
        resp = await client.get("/api/history/timeline?page=1&page_size=5")
        assert resp.status_code == 200

    async def test_search_records(self, client):
        """搜索记录"""
        await client.post("/api/records", json={
            "dish_name": "宫保鸡丁",
            "meal_type": "午餐",
            "rating": 4,
            "meal_date": str(date.today()),
        })
        resp = await client.get("/api/history/search?keyword=宫保")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) >= 1

    async def test_search_by_location(self, client):
        """按地点搜索"""
        await client.post("/api/records", json={
            "dish_name": "测试菜",
            "meal_type": "午餐",
            "location_name": "川味小馆",
            "rating": 3,
            "meal_date": str(date.today()),
        })
        resp = await client.get("/api/history/search?location=川味")
        assert resp.status_code == 200
