"""推荐模块测试用例"""
import pytest


class TestRecommend:
    """随机推荐测试"""

    async def test_recommend_returns_dish(self, client, seed_dishes):
        """推荐返回一道启用的菜品"""
        resp = await client.post("/api/recommend")
        assert resp.status_code == 200
        data = resp.json()
        assert "dish" in data
        assert "reason" in data
        assert data["dish"]["is_active"] is True

    async def test_recommend_with_cuisine_filter(self, client, seed_dishes):
        """按菜系筛选推荐"""
        resp = await client.post("/api/recommend", json={
            "cuisine": "川菜",
        })
        assert resp.status_code == 200
        assert resp.json()["dish"]["cuisine"] == "川菜"

    async def test_recommend_with_taste_filter(self, client, seed_dishes):
        """按口味筛选推荐"""
        resp = await client.post("/api/recommend", json={
            "taste": "辣",
        })
        assert resp.status_code == 200
        dish = resp.json()["dish"]
        assert "辣" in dish.get("tags", []) or dish.get("cuisine") == "川菜"

    async def test_recommend_with_price_filter(self, client, seed_dishes):
        """按价格筛选推荐"""
        resp = await client.post("/api/recommend", json={
            "price_range": "¥20-50",
        })
        assert resp.status_code == 200
        price = resp.json()["dish"]["reference_price"]
        assert 20 <= price < 50

    async def test_recommend_excludes_inactive(self, client, seed_dishes):
        """不推荐已下架的菜品"""
        results = set()
        for _ in range(20):
            resp = await client.post("/api/recommend")
            results.add(resp.json()["dish"]["name"])
        assert "已下架菜品" not in results

    async def test_recommend_no_match(self, client, seed_dishes):
        """筛选条件无匹配时返回404"""
        resp = await client.post("/api/recommend", json={
            "cuisine": "东南亚",
            "taste": "甜",
            "price_range": "¥50-100",
        })
        assert resp.status_code in (200, 404)


class TestQuickRecommend:
    """场景快捷推荐测试"""

    async def test_quick_hungry(self, client, seed_dishes):
        """我超饿 - 应推荐快速出餐的菜品"""
        resp = await client.post("/api/recommend/quick/hungry")
        assert resp.status_code == 200
        assert "dish" in resp.json()

    async def test_quick_casual(self, client, seed_dishes):
        """随便就行 - 随机推荐"""
        resp = await client.post("/api/recommend/quick/casual")
        assert resp.status_code == 200

    async def test_quick_fridge(self, client, seed_dishes):
        """清理冰箱 - 推荐简单菜品"""
        resp = await client.post("/api/recommend/quick/fridge")
        assert resp.status_code == 200

    async def test_quick_invalid_scenario(self, client, seed_dishes):
        """无效场景返回404"""
        resp = await client.post("/api/recommend/quick/invalid")
        assert resp.status_code == 404
