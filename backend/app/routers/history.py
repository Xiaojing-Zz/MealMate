"""历史回顾模块业务逻辑"""
import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
import aiosqlite
from ..models.schemas import PaginatedResponse
from ..core.deps import get_db

router = APIRouter(prefix="/api/history", tags=["历史回顾"])


@router.get("/calendar")
async def get_calendar_records(year: int, month: int, db: aiosqlite.Connection = Depends(get_db)):
    start = f"{year}-{month:02d}-01"
    if month == 12:
        end = f"{year + 1}-01-01"
    else:
        end = f"{year}-{month + 1:02d}-01"

    cursor = await db.execute(
        """SELECT meal_date, COUNT(*) as count, GROUP_CONCAT(dish_name) as dishes
           FROM meal_records
           WHERE meal_date >= ? AND meal_date < ?
           GROUP BY meal_date ORDER BY meal_date""",
        (start, end),
    )
    rows = await cursor.fetchall()
    return [
        {"date": r["meal_date"], "count": r["count"], "dishes": r["dishes"].split(",") if r["dishes"] else []}
        for r in rows
    ]


@router.get("/timeline")
async def get_timeline(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db),
):
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM meal_records")
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        "SELECT * FROM meal_records ORDER BY meal_date DESC, created_at DESC LIMIT ? OFFSET ?",
        (page_size, (page - 1) * page_size),
    )
    rows = await cursor.fetchall()
    items = [_row_to_dict(r) for r in rows]
    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/search")
async def search_records(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db),
):
    where = ["1=1"]
    params = []
    if keyword:
        where.append("dish_name LIKE ?")
        params.append(f"%{keyword}%")
    if location:
        where.append("location_name LIKE ?")
        params.append(f"%{location}%")
    if start_date:
        where.append("meal_date >= ?")
        params.append(start_date)
    if end_date:
        where.append("meal_date <= ?")
        params.append(end_date)

    where_clause = " AND ".join(where)
    cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM meal_records WHERE {where_clause}", params)
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        f"SELECT * FROM meal_records WHERE {where_clause} ORDER BY meal_date DESC LIMIT ? OFFSET ?",
        params + [page_size, (page - 1) * page_size],
    )
    rows = await cursor.fetchall()
    items = [_row_to_dict(r) for r in rows]
    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)


def _row_to_dict(row):
    tags = row["tags"]
    if isinstance(tags, str):
        tags = json.loads(tags) if tags else []
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "dish_name": row["dish_name"],
        "meal_type": row["meal_type"],
        "location_name": row["location_name"],
        "cost": row["cost"],
        "calories": row["calories"],
        "rating": row["rating"],
        "tags": tags or [],
        "meal_date": row["meal_date"],
        "note": row["note"],
        "created_at": row["created_at"],
    }
