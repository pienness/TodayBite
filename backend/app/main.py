from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import recommend

app = FastAPI(
    title="TodayBite 推荐引擎",
    description="智能外卖推荐助手 - AI 推荐引擎后端",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api", tags=["recommend"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
