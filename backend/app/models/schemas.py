from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# --- 枚举类型 ---

class MealType(str, Enum):
    BREAKFAST = "早餐"
    LUNCH = "午餐"
    DINNER = "晚餐"
    AFTERNOON_TEA = "下午茶"
    MIDNIGHT_SNACK = "夜宵"


class Cuisine(str, Enum):
    SICHUAN = "川菜"
    CANTONESE = "粤菜"
    HUNANESE = "湘菜"
    JAPANESE = "日料"
    WESTERN = "西餐"
    SOUTHEAST_ASIAN = "东南亚"


class Taste(str, Enum):
    SPICY = "辣"
    NON_SPICY = "不辣"
    SOUR = "酸"
    SWEET = "甜"
    UMAMI = "鲜"


class PriceRange(str, Enum):
    UNDER_20 = "¥20以下"
    RANGE_20_50 = "¥20-50"
    RANGE_50_100 = "¥50-100"
    UNLIMITED = "无限制"


class CalorieRange(str, Enum):
    LOW = "低卡(<400)"
    MEDIUM = "中卡(400-700)"
    HIGH = "高卡(>700)"


class FeedbackAction(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    ACCEPT = "accept"


# --- 用户相关 ---

class UserBase(BaseModel):
    phone: str = Field(..., max_length=20)
    nickname: str = Field(..., max_length=50)
    avatar: Optional[str] = None
    taste_tags: Optional[List[str]] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = None
    taste_tags: Optional[List[str]] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- 菜品相关 ---

class DishBase(BaseModel):
    name: str = Field(..., max_length=100)
    cuisine: Optional[Cuisine] = None
    tags: Optional[List[str]] = None
    reference_price: Optional[float] = None
    prep_time: Optional[int] = None
    calories: Optional[int] = None
    image_url: Optional[str] = None


class DishCreate(DishBase):
    pass


class DishResponse(DishBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- 饮食记录相关 ---

class MealRecordBase(BaseModel):
    dish_name: str = Field(..., max_length=100)
    meal_type: MealType
    location_name: Optional[str] = Field(None, max_length=200)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cost: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    photo_url: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    tags: Optional[List[str]] = None
    meal_date: date
    note: Optional[str] = None


class MealRecordCreate(MealRecordBase):
    pass


class MealRecordUpdate(BaseModel):
    dish_name: Optional[str] = Field(None, max_length=100)
    meal_type: Optional[MealType] = None
    location_name: Optional[str] = Field(None, max_length=200)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cost: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    photo_url: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[List[str]] = None
    meal_date: Optional[date] = None
    note: Optional[str] = None


class MealRecordResponse(MealRecordBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- 推荐相关 ---

class RecommendFilter(BaseModel):
    taste: Optional[Taste] = None
    cuisine: Optional[Cuisine] = None
    meal_type: Optional[MealType] = None
    price_range: Optional[PriceRange] = None
    calorie_range: Optional[CalorieRange] = None


class RecommendResponse(BaseModel):
    dish: DishResponse
    reason: str  # 推荐理由


# --- 用户反馈相关 ---

class FeedbackCreate(BaseModel):
    dish_id: int
    action: FeedbackAction


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    dish_id: int
    action: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- 统计相关 ---

class WeeklyCostItem(BaseModel):
    date: str
    cost: float


class CategoryDistributionItem(BaseModel):
    cuisine: str
    count: int
    percentage: float


class CalorieTrendItem(BaseModel):
    date: str
    calories: int


class TopLocationItem(BaseModel):
    location_name: str
    visit_count: int


class FavoriteDishItem(BaseModel):
    dish_name: str
    avg_rating: float
    count: int


class StatisticsResponse(BaseModel):
    weekly_cost: List[WeeklyCostItem]
    category_distribution: List[CategoryDistributionItem]
    calorie_trend: List[CalorieTrendItem]
    top_locations: List[TopLocationItem]
    favorite_dishes: List[FavoriteDishItem]


# --- 通用响应 ---

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


class MessageResponse(BaseModel):
    message: str
