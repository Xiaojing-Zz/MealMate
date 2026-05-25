"""饮食记录 API 路由契约"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date
from ..models.schemas import (
    MealRecordCreate, MealRecordUpdate, MealRecordResponse, PaginatedResponse
)

router = APIRouter(prefix="/api/records", tags=["饮食记录"])


@router.post("", response_model=MealRecordResponse, status_code=201)
async def create_record(record: MealRecordCreate):
    """创建饮食记录"""
    ...


@router.get("", response_model=PaginatedResponse)
async def list_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    meal_type: Optional[str] = None,
):
    """获取饮食记录列表（支持分页和筛选）"""
    ...


@router.get("/{record_id}", response_model=MealRecordResponse)
async def get_record(record_id: int):
    """获取单条饮食记录"""
    ...


@router.put("/{record_id}", response_model=MealRecordResponse)
async def update_record(record_id: int, record: MealRecordUpdate):
    """更新饮食记录"""
    ...


@router.delete("/{record_id}", status_code=204)
async def delete_record(record_id: int):
    """删除饮食记录"""
    ...
