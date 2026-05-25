from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, recommend, records, history, statistics, feedback

app = FastAPI(
    title="MealMate API",
    description="MealMate（餐伴）- 智能饮食决策助手 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(recommend.router)
app.include_router(records.router)
app.include_router(history.router)
app.include_router(statistics.router)
app.include_router(feedback.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
