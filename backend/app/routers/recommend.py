"""随机推荐 API 路由契约"""
from fastapi import APIRouter
from typing import Optional
from ..models.schemas import (
    RecommendFilter, RecommendResponse, Cuisine, Taste, MealType, PriceRange, CalorieRange
)

router = APIRouter(prefix="/api/recommend", tags=["随机推荐"])


@router.post("", response_model=RecommendResponse)
async def recommend_dish(filters: Optional[RecommendFilter] = None):
    """随机推荐一道菜（核心功能）"""
    ...


@router.post("/quick/{scenario}", response_model=RecommendResponse)
async def quick_recommend(scenario: str):
    """场景快捷推荐 - 我超饿/随便就行/清理冰箱"""
    ...
