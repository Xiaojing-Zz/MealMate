"""历史回顾 API 路由契约"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

router = APIRouter(prefix="/api/history", tags=["历史回顾"])


@router.get("/calendar")
async def get_calendar_records(year: int, month: int):
    """日历视图 - 获取某月每天的饮食记录摘要"""
    ...


@router.get("/timeline")
async def get_timeline(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """时间轴浏览 - 按时间倒序展示记录"""
    ...


@router.get("/search")
async def search_records(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """搜索/筛选记录"""
    ...
