"""饮食记录模块业务逻辑"""
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
import aiosqlite
from ..models.schemas import (
    MealRecordCreate, MealRecordUpdate, MealRecordResponse, PaginatedResponse,
)
from ..core.deps import get_db

router = APIRouter(prefix="/api/records", tags=["饮食记录"])


@router.post("", response_model=MealRecordResponse, status_code=201)
async def create_record(record: MealRecordCreate, db: aiosqlite.Connection = Depends(get_db)):
    tags_json = json.dumps(record.tags) if record.tags else None
    cursor = await db.execute(
        """INSERT INTO meal_records
           (user_id, dish_name, meal_type, location_name, latitude, longitude,
            cost, calories, photo_url, rating, tags, meal_date, note)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (1, record.dish_name, record.meal_type.value, record.location_name,
         record.latitude, record.longitude, record.cost, record.calories,
         record.photo_url, record.rating, tags_json, str(record.meal_date), record.note),
    )
    await db.commit()
    return MealRecordResponse(
        id=cursor.lastrowid,
        user_id=1,
        dish_name=record.dish_name,
        meal_type=record.meal_type.value,
        location_name=record.location_name,
        latitude=record.latitude,
        longitude=record.longitude,
        cost=record.cost,
        calories=record.calories,
        photo_url=record.photo_url,
        rating=record.rating,
        tags=record.tags or [],
        meal_date=record.meal_date,
        note=record.note,
        created_at="2024-01-01T00:00:00",
    )


@router.get("", response_model=PaginatedResponse)
async def list_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    meal_type: Optional[str] = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    where = ["1=1"]
    params = []
    if start_date:
        where.append("meal_date >= ?")
        params.append(start_date)
    if end_date:
        where.append("meal_date <= ?")
        params.append(end_date)
    if meal_type:
        where.append("meal_type = ?")
        params.append(meal_type)

    where_clause = " AND ".join(where)
    cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM meal_records WHERE {where_clause}", params)
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        f"SELECT * FROM meal_records WHERE {where_clause} ORDER BY meal_date DESC, created_at DESC LIMIT ? OFFSET ?",
        params + [page_size, (page - 1) * page_size],
    )
    rows = await cursor.fetchall()
    items = [_row_to_record(r) for r in rows]

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{record_id}", response_model=MealRecordResponse)
async def get_record(record_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM meal_records WHERE id = ?", (record_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="记录不存在")
    return _row_to_record(row)


@router.put("/{record_id}", response_model=MealRecordResponse)
async def update_record(record_id: int, record: MealRecordUpdate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM meal_records WHERE id = ?", (record_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="记录不存在")

    updates = []
    values = []
    for field, value in record.model_dump(exclude_none=True).items():
        col = field
        if field == "meal_type" and hasattr(value, "value"):
            value = value.value
        elif field == "tags" and isinstance(value, list):
            value = json.dumps(value)
        elif field == "meal_date":
            value = str(value)
        updates.append(f"{col} = ?")
        values.append(value)

    if updates:
        values.append(record_id)
        await db.execute(f"UPDATE meal_records SET {', '.join(updates)} WHERE id = ?", values)
        await db.commit()

    cursor = await db.execute("SELECT * FROM meal_records WHERE id = ?", (record_id,))
    row = await cursor.fetchone()
    return _row_to_record(row)


@router.delete("/{record_id}", status_code=204)
async def delete_record(record_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM meal_records WHERE id = ?", (record_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="记录不存在")
    await db.execute("DELETE FROM meal_records WHERE id = ?", (record_id,))
    await db.commit()


def _row_to_record(row):
    tags = row["tags"]
    if isinstance(tags, str):
        tags = json.loads(tags) if tags else []
    from datetime import date
    meal_date = row["meal_date"]
    if isinstance(meal_date, str):
        meal_date = date.fromisoformat(meal_date)
    return MealRecordResponse(
        id=row["id"],
        user_id=row["user_id"],
        dish_name=row["dish_name"],
        meal_type=row["meal_type"],
        location_name=row["location_name"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        cost=row["cost"],
        calories=row["calories"],
        photo_url=row["photo_url"],
        rating=row["rating"],
        tags=tags or [],
        meal_date=meal_date,
        note=row["note"],
        created_at=row["created_at"] or "2024-01-01T00:00:00",
    )
