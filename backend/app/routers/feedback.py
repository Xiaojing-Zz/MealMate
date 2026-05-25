"""用户反馈 API 路由契约"""
from fastapi import APIRouter
from ..models.schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["用户反馈"])


@router.post("", response_model=FeedbackResponse, status_code=201)
async def create_feedback(feedback: FeedbackCreate):
    """提交菜品反馈（喜欢/不喜欢/接受）"""
    ...
