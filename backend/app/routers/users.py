"""用户相关 API 路由契约"""
from fastapi import APIRouter
from ..models.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/users", tags=["用户"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate):
    """用户注册"""
    ...


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """获取当前用户信息"""
    ...


@router.put("/me", response_model=UserResponse)
async def update_user(user: UserUpdate):
    """更新用户信息"""
    ...
