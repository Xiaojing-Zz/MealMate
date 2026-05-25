"""用户模块业务逻辑"""
import json
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from ..models.schemas import UserCreate, UserUpdate, UserResponse
from ..core.deps import get_db

router = APIRouter(prefix="/api/users", tags=["用户"])

# 简单内存存储当前用户（后续替换为JWT）
_current_user_id = None


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: aiosqlite.Connection = Depends(get_db)):
    global _current_user_id
    try:
        tags_json = json.dumps(user.taste_tags) if user.taste_tags else None
        cursor = await db.execute(
            "INSERT INTO users (phone, nickname, avatar, taste_tags) VALUES (?,?,?,?)",
            (user.phone, user.nickname, user.avatar, tags_json),
        )
        await db.commit()
        _current_user_id = cursor.lastrowid
        return UserResponse(
            id=cursor.lastrowid,
            phone=user.phone,
            nickname=user.nickname,
            avatar=user.avatar,
            taste_tags=user.taste_tags or [],
            created_at="2024-01-01T00:00:00",
        )
    except aiosqlite.IntegrityError:
        raise HTTPException(status_code=400, detail="手机号已注册")


@router.get("/me", response_model=UserResponse)
async def get_current_user(db: aiosqlite.Connection = Depends(get_db)):
    if not _current_user_id:
        raise HTTPException(status_code=401, detail="未登录")
    cursor = await db.execute("SELECT * FROM users WHERE id = ?", (_current_user_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="用户不存在")
    return _row_to_user(row)


@router.put("/me", response_model=UserResponse)
async def update_user(user: UserUpdate, db: aiosqlite.Connection = Depends(get_db)):
    if not _current_user_id:
        raise HTTPException(status_code=401, detail="未登录")
    updates = []
    values = []
    if user.nickname is not None:
        updates.append("nickname = ?")
        values.append(user.nickname)
    if user.avatar is not None:
        updates.append("avatar = ?")
        values.append(user.avatar)
    if user.taste_tags is not None:
        updates.append("taste_tags = ?")
        values.append(json.dumps(user.taste_tags))
    if updates:
        values.append(_current_user_id)
        await db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", values)
        await db.commit()
    cursor = await db.execute("SELECT * FROM users WHERE id = ?", (_current_user_id,))
    row = await cursor.fetchone()
    return _row_to_user(row)


def _row_to_user(row):
    tags = row["taste_tags"]
    if isinstance(tags, str):
        tags = json.loads(tags) if tags else []
    return UserResponse(
        id=row["id"],
        phone=row["phone"],
        nickname=row["nickname"],
        avatar=row["avatar"],
        taste_tags=tags or [],
        created_at=row["created_at"] or "2024-01-01T00:00:00",
    )
