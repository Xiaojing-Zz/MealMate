"""用户反馈模块测试用例"""
import pytest


class TestFeedback:
    """用户反馈测试"""

    async def test_create_like_feedback(self, client, seed_dishes):
        """提交喜欢反馈"""
        resp = await client.post("/api/feedback", json={
            "dish_id": 1,
            "action": "like",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["dish_id"] == 1
        assert data["action"] == "like"

    async def test_create_dislike_feedback(self, client, seed_dishes):
        """提交不喜欢反馈"""
        resp = await client.post("/api/feedback", json={
            "dish_id": 1,
            "action": "dislike",
        })
        assert resp.status_code == 201
        assert resp.json()["action"] == "dislike"

    async def test_create_accept_feedback(self, client, seed_dishes):
        """提交接受反馈"""
        resp = await client.post("/api/feedback", json={
            "dish_id": 1,
            "action": "accept",
        })
        assert resp.status_code == 201
        assert resp.json()["action"] == "accept"

    async def test_feedback_invalid_dish(self, client, seed_dishes):
        """菜品不存在返回404"""
        resp = await client.post("/api/feedback", json={
            "dish_id": 999,
            "action": "like",
        })
        assert resp.status_code == 404

    async def test_feedback_invalid_action(self, client, seed_dishes):
        """无效的反馈动作返回422"""
        resp = await client.post("/api/feedback", json={
            "dish_id": 1,
            "action": "superlike",
        })
        assert resp.status_code == 422
