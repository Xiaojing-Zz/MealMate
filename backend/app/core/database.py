import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "mealmate.db")


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    db = await aiosqlite.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        await db.executescript(f.read())
    await db.commit()
    await db.close()
