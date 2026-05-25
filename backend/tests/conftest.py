import pytest
import pytest_asyncio
import aiosqlite
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core import deps


@pytest_asyncio.fixture
async def db():
    """创建内存数据库，每个测试独立"""
    conn = await aiosqlite.connect(":memory:")
    conn.row_factory = aiosqlite.Row
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        await conn.executescript(f.read())
    await conn.commit()

    deps.set_test_db(conn)
    yield conn
    deps.set_test_db(None)
    await conn.close()


@pytest_asyncio.fixture
async def client(db):
    """HTTP 测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def seed_dishes(db):
    """插入测试菜品数据"""
    dishes = [
        ("宫保鸡丁", "川菜", '["辣","下饭"]', 28, 20, 450, None, 1),
        ("白切鸡", "粤菜", '["清淡","鲜"]', 45, 30, 320, None, 1),
        ("日式咖喱饭", "日料", '["微辣","快捷"]', 35, 25, 580, None, 1),
        ("番茄牛腩", "粤菜", '["酸甜","营养"]', 55, 40, 520, None, 1),
        ("已下架菜品", "川菜", '["辣"]', 20, 15, 400, None, 0),
    ]
    for d in dishes:
        await db.execute(
            "INSERT INTO dishes (name, cuisine, tags, reference_price, prep_time, calories, image_url, is_active) VALUES (?,?,?,?,?,?,?,?)",
            d,
        )
    await db.commit()
