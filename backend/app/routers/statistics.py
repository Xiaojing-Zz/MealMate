"""统计分析 API 路由契约"""
from fastapi import APIRouter, Query
from typing import Optional
from ..models.schemas import StatisticsResponse

router = APIRouter(prefix="/api/statistics", tags=["统计分析"])


@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    period: str = Query("week", regex="^(week|month|custom)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """获取统计数据（本周/本月/自定义）"""
    ...
