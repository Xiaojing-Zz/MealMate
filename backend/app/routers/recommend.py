"""随机推荐模块业务逻辑"""
import json
import random
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from ..models.schemas import (
    RecommendFilter, RecommendResponse, DishResponse,
    Taste, PriceRange, CalorieRange,
)
from ..core.deps import get_db

router = APIRouter(prefix="/api/recommend", tags=["随机推荐"])

PRICE_RANGES = {
    "¥20以下": (0, 20),
    "¥20-50": (20, 50),
    "¥50-100": (50, 100),
}

CALORIE_RANGES = {
    "低卡(<400)": (0, 400),
    "中卡(400-700)": (400, 700),
    "高卡(>700)": (700, 99999),
}

REASONS = [
    "今天天气适合来点这个！",
    "你已经好久没吃这个了",
    "根据你的口味偏好推荐",
    "营养均衡的好选择",
    "换个口味试试吧",
]


@router.post("", response_model=RecommendResponse)
async def recommend_dish(filters: Optional[RecommendFilter] = None, db: aiosqlite.Connection = Depends(get_db)):
    query = "SELECT * FROM dishes WHERE is_active = 1"
    params = []

    if filters:
        if filters.cuisine:
            query += " AND cuisine = ?"
            params.append(filters.cuisine.value if hasattr(filters.cuisine, 'value') else filters.cuisine)
        if filters.taste:
            taste_val = filters.taste.value if hasattr(filters.taste, 'value') else filters.taste
            query += " AND tags LIKE ?"
            params.append(f"%{taste_val}%")
        if filters.price_range:
            price_range = filters.price_range.value if hasattr(filters.price_range, 'value') else filters.price_range
            if price_range in PRICE_RANGES:
                lo, hi = PRICE_RANGES[price_range]
                query += " AND reference_price >= ? AND reference_price < ?"
                params.extend([lo, hi])
        if filters.calorie_range:
            cal_range = filters.calorie_range.value if hasattr(filters.calorie_range, 'value') else filters.calorie_range
            if cal_range in CALORIE_RANGES:
                lo, hi = CALORIE_RANGES[cal_range]
                query += " AND calories >= ? AND calories < ?"
                params.extend([lo, hi])

    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="没有找到符合条件的菜品")

    row = random.choice(rows)
    dish = _row_to_dish(row)
    return RecommendResponse(dish=dish, reason=random.choice(REASONS))


@router.post("/quick/{scenario}", response_model=RecommendResponse)
async def quick_recommend(scenario: str, db: aiosqlite.Connection = Depends(get_db)):
    query = "SELECT * FROM dishes WHERE is_active = 1"
    params = []

    if scenario == "hungry":
        query += " AND prep_time <= 25"
    elif scenario == "casual":
        pass
    elif scenario == "fridge":
        query += " AND prep_time <= 20"
    else:
        raise HTTPException(status_code=404, detail="未知的场景")

    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    if not rows:
        cursor = await db.execute("SELECT * FROM dishes WHERE is_active = 1")
        rows = await cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="没有可用的菜品")

    row = random.choice(rows)
    dish = _row_to_dish(row)

    scenario_reasons = {
        "hungry": "饿了就要快！这道出餐快",
        "casual": "随便选一个，也许有惊喜",
        "fridge": "简单食材，快速搞定",
    }
    return RecommendResponse(dish=dish, reason=scenario_reasons.get(scenario, random.choice(REASONS)))


def _row_to_dish(row):
    tags = row["tags"]
    if isinstance(tags, str):
        tags = json.loads(tags) if tags else []
    return DishResponse(
        id=row["id"],
        name=row["name"],
        cuisine=row["cuisine"],
        tags=tags or [],
        reference_price=row["reference_price"],
        prep_time=row["prep_time"],
        calories=row["calories"],
        image_url=row["image_url"],
        is_active=bool(row["is_active"]),
        created_at=row["created_at"] or "2024-01-01T00:00:00",
    )
