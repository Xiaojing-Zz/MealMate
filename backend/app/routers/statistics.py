"""统计分析模块业务逻辑"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from datetime import date, timedelta
import aiosqlite
from ..models.schemas import (
    StatisticsResponse, WeeklyCostItem, CategoryDistributionItem,
    CalorieTrendItem, TopLocationItem, FavoriteDishItem,
)
from ..core.deps import get_db

router = APIRouter(prefix="/api/statistics", tags=["统计分析"])


@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    period: str = Query("week", regex="^(week|month|custom)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    today = date.today()
    if period == "week":
        start = today - timedelta(days=today.weekday())
        end = today
    elif period == "month":
        start = today.replace(day=1)
        end = today
    else:
        start = date.fromisoformat(start_date) if start_date else today - timedelta(days=30)
        end = date.fromisoformat(end_date) if end_date else today

    cursor = await db.execute(
        """SELECT meal_date, SUM(cost) as total_cost
           FROM meal_records
           WHERE meal_date BETWEEN ? AND ? AND cost IS NOT NULL
           GROUP BY meal_date ORDER BY meal_date""",
        (str(start), str(end)),
    )
    cost_rows = await cursor.fetchall()
    weekly_cost = [WeeklyCostItem(date=r["meal_date"], cost=r["total_cost"] or 0) for r in cost_rows]

    cursor = await db.execute(
        """SELECT meal_type as cuisine, COUNT(*) as cnt
           FROM meal_records
           WHERE meal_date BETWEEN ? AND ?
           GROUP BY meal_type ORDER BY cnt DESC""",
        (str(start), str(end)),
    )
    cat_rows = await cursor.fetchall()
    total_records = sum(r["cnt"] for r in cat_rows) or 1
    category_distribution = [
        CategoryDistributionItem(cuisine=r["cuisine"], count=r["cnt"], percentage=round(r["cnt"] / total_records * 100, 1))
        for r in cat_rows
    ]

    cursor = await db.execute(
        """SELECT meal_date, SUM(calories) as total_cal
           FROM meal_records
           WHERE meal_date BETWEEN ? AND ? AND calories IS NOT NULL
           GROUP BY meal_date ORDER BY meal_date""",
        (str(start), str(end)),
    )
    cal_rows = await cursor.fetchall()
    calorie_trend = [CalorieTrendItem(date=r["meal_date"], calories=r["total_cal"] or 0) for r in cal_rows]

    cursor = await db.execute(
        """SELECT location_name, COUNT(*) as visit_count
           FROM meal_records
           WHERE meal_date BETWEEN ? AND ? AND location_name IS NOT NULL AND location_name != ''
           GROUP BY location_name ORDER BY visit_count DESC LIMIT 5""",
        (str(start), str(end)),
    )
    loc_rows = await cursor.fetchall()
    top_locations = [TopLocationItem(location_name=r["location_name"], visit_count=r["visit_count"]) for r in loc_rows]

    cursor = await db.execute(
        """SELECT dish_name, AVG(rating) as avg_rating, COUNT(*) as cnt
           FROM meal_records
           WHERE meal_date BETWEEN ? AND ?
           GROUP BY dish_name ORDER BY avg_rating DESC, cnt DESC LIMIT 5""",
        (str(start), str(end)),
    )
    fav_rows = await cursor.fetchall()
    favorite_dishes = [
        FavoriteDishItem(dish_name=r["dish_name"], avg_rating=round(r["avg_rating"], 1), count=r["cnt"])
        for r in fav_rows
    ]

    return StatisticsResponse(
        weekly_cost=weekly_cost,
        category_distribution=category_distribution,
        calorie_trend=calorie_trend,
        top_locations=top_locations,
        favorite_dishes=favorite_dishes,
    )
