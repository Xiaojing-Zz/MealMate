"""饮食记录模块测试用例"""
import pytest
from datetime import date


class TestCreateRecord:
    """创建饮食记录测试"""

    async def test_create_record_success(self, client):
        """创建记录成功"""
        resp = await client.post("/api/records", json={
            "dish_name": "宫保鸡丁",
            "meal_type": "午餐",
            "rating": 4,
            "meal_date": str(date.today()),
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["dish_name"] == "宫保鸡丁"
        assert data["meal_type"] == "午餐"
        assert data["rating"] == 4

    async def test_create_record_full_fields(self, client):
        """创建完整记录"""
        resp = await client.post("/api/records", json={
            "dish_name": "日式拉面",
            "meal_type": "晚餐",
            "location_name": "一兰拉面",
            "cost": 58,
            "calories": 650,
            "rating": 5,
            "meal_date": str(date.today()),
            "note": "很好吃",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["cost"] == 58
        assert data["calories"] == 650
        assert data["location_name"] == "一兰拉面"

    async def test_create_record_missing_required(self, client):
        """缺少必填字段返回422"""
        resp = await client.post("/api/records", json={
            "dish_name": "测试菜",
            # 缺少 meal_type, rating, meal_date
        })
        assert resp.status_code == 422

    async def test_create_record_invalid_rating(self, client):
        """评分超出范围返回422"""
        resp = await client.post("/api/records", json={
            "dish_name": "测试菜",
            "meal_type": "午餐",
            "rating": 6,  # 超出1-5
            "meal_date": str(date.today()),
        })
        assert resp.status_code == 422

    async def test_create_record_invalid_meal_type(self, client):
        """无效用餐类型返回422"""
        resp = await client.post("/api/records", json={
            "dish_name": "测试菜",
            "meal_type": "下午茶会",
            "rating": 3,
            "meal_date": str(date.today()),
        })
        assert resp.status_code == 422


class TestListRecords:
    """获取记录列表测试"""

    async def test_list_records_empty(self, client):
        """无记录时返回空列表"""
        resp = await client.get("/api/records")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_list_records_with_data(self, client):
        """有数据时正确返回"""
        # 先创建两条记录
        for i in range(2):
            await client.post("/api/records", json={
                "dish_name": f"菜品{i}",
                "meal_type": "午餐",
                "rating": 3,
                "meal_date": str(date.today()),
            })
        resp = await client.get("/api/records")
        assert resp.json()["total"] == 2

    async def test_list_records_pagination(self, client):
        """分页功能"""
        for i in range(5):
            await client.post("/api/records", json={
                "dish_name": f"菜品{i}",
                "meal_type": "午餐",
                "rating": 3,
                "meal_date": str(date.today()),
            })
        resp = await client.get("/api/records?page=1&page_size=2")
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2

    async def test_list_records_filter_by_date(self, client):
        """按日期筛选"""
        await client.post("/api/records", json={
            "dish_name": "今天的菜",
            "meal_type": "午餐",
            "rating": 3,
            "meal_date": "2024-01-15",
        })
        resp = await client.get("/api/records?start_date=2024-01-15&end_date=2024-01-15")
        assert resp.json()["total"] == 1


class TestRecordCRUD:
    """单条记录 CRUD 测试"""

    async def test_get_record(self, client):
        """获取单条记录"""
        create_resp = await client.post("/api/records", json={
            "dish_name": "红烧肉",
            "meal_type": "晚餐",
            "rating": 5,
            "meal_date": str(date.today()),
        })
        record_id = create_resp.json()["id"]
        resp = await client.get(f"/api/records/{record_id}")
        assert resp.status_code == 200
        assert resp.json()["dish_name"] == "红烧肉"

    async def test_get_record_not_found(self, client):
        """记录不存在返回404"""
        resp = await client.get("/api/records/999")
        assert resp.status_code == 404

    async def test_update_record(self, client):
        """更新记录"""
        create_resp = await client.post("/api/records", json={
            "dish_name": "旧名称",
            "meal_type": "午餐",
            "rating": 3,
            "meal_date": str(date.today()),
        })
        record_id = create_resp.json()["id"]
        resp = await client.put(f"/api/records/{record_id}", json={
            "dish_name": "新名称",
            "rating": 5,
        })
        assert resp.status_code == 200
        assert resp.json()["dish_name"] == "新名称"
        assert resp.json()["rating"] == 5

    async def test_delete_record(self, client):
        """删除记录"""
        create_resp = await client.post("/api/records", json={
            "dish_name": "待删除",
            "meal_type": "午餐",
            "rating": 3,
            "meal_date": str(date.today()),
        })
        record_id = create_resp.json()["id"]
        resp = await client.delete(f"/api/records/{record_id}")
        assert resp.status_code == 204
        # 确认已删除
        get_resp = await client.get(f"/api/records/{record_id}")
        assert get_resp.status_code == 404
