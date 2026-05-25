"""用户反馈模块业务逻辑"""
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from ..models.schemas import FeedbackCreate, FeedbackResponse
from ..core.deps import get_db

router = APIRouter(prefix="/api/feedback", tags=["用户反馈"])


@router.post("", response_model=FeedbackResponse, status_code=201)
async def create_feedback(feedback: FeedbackCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM dishes WHERE id = ?", (feedback.dish_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="菜品不存在")

    cursor = await db.execute(
        "INSERT INTO user_feedback (user_id, dish_id, action) VALUES (?,?,?)",
        (1, feedback.dish_id, feedback.action.value),
    )
    await db.commit()
    return FeedbackResponse(
        id=cursor.lastrowid,
        user_id=1,
        dish_id=feedback.dish_id,
        action=feedback.action.value,
        created_at="2024-01-01T00:00:00",
    )
