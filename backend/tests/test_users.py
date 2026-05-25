"""用户模块测试用例"""
import pytest


class TestUserRegister:
    """用户注册测试"""

    async def test_register_success(self, client):
        """注册成功返回201和用户信息"""
        resp = await client.post("/api/users/register", json={
            "phone": "13800001111",
            "nickname": "测试用户",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["phone"] == "13800001111"
        assert data["nickname"] == "测试用户"
        assert "id" in data

    async def test_register_duplicate_phone(self, client):
        """重复手机号注册返回400"""
        await client.post("/api/users/register", json={
            "phone": "13800002222",
            "nickname": "用户A",
        })
        resp = await client.post("/api/users/register", json={
            "phone": "13800002222",
            "nickname": "用户B",
        })
        assert resp.status_code == 400

    async def test_register_missing_fields(self, client):
        """缺少必填字段返回422"""
        resp = await client.post("/api/users/register", json={
            "phone": "13800003333",
        })
        assert resp.status_code == 422

    async def test_register_with_taste_tags(self, client):
        """注册时可携带口味标签"""
        resp = await client.post("/api/users/register", json={
            "phone": "13800004444",
            "nickname": "吃货",
            "taste_tags": ["辣", "下饭"],
        })
        assert resp.status_code == 201
        assert resp.json()["taste_tags"] == ["辣", "下饭"]


class TestUserProfile:
    """用户信息测试"""

    async def test_get_current_user(self, client):
        """获取当前用户信息"""
        # 先注册
        await client.post("/api/users/register", json={
            "phone": "13800005555",
            "nickname": "用户C",
        })
        resp = await client.get("/api/users/me")
        assert resp.status_code == 200
        assert resp.json()["nickname"] == "用户C"

    async def test_update_user(self, client):
        """更新用户信息"""
        await client.post("/api/users/register", json={
            "phone": "13800006666",
            "nickname": "旧昵称",
        })
        resp = await client.put("/api/users/me", json={
            "nickname": "新昵称",
            "taste_tags": ["甜"],
        })
        assert resp.status_code == 200
        assert resp.json()["nickname"] == "新昵称"
        assert resp.json()["taste_tags"] == ["甜"]
