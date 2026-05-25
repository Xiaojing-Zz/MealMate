"""数据库依赖注入"""
import aiosqlite
import json
import os

DB_PATH = os.environ.get("MEALMATE_DB", os.path.join(os.path.dirname(__file__), "..", "..", "mealmate.db"))

# 可被测试覆盖的数据库连接
_test_db = None


def set_test_db(db):
    """测试时设置共享的内存数据库连接"""
    global _test_db
    _test_db = db


def _make_row_factory(cursor, row):
    result = {}
    for i, col in enumerate(cursor.description):
        val = row[i]
        name = col[0]
        if name in ("tags", "taste_tags") and val and isinstance(val, str):
            val = json.loads(val)
        elif name == "is_active":
            val = bool(val) if val is not None else val
        result[name] = val
    return result


async def get_db():
    if _test_db is not None:
        _test_db.row_factory = _make_row_factory
        yield _test_db
    else:
        db = await aiosqlite.connect(DB_PATH)
        db.row_factory = _make_row_factory
        try:
            yield db
        finally:
            await db.close()


async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = await aiosqlite.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        await db.executescript(f.read())
    await db.commit()
    await db.close()
