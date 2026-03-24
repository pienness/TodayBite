from fastapi import APIRouter, HTTPException

from app.models.schemas import UserPreferences, RecommendResponse
from app.services.recommender import RecommenderService

router = APIRouter()
recommender = RecommenderService()


@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendations(preferences: UserPreferences):
    """根据用户偏好生成外卖推荐方案"""
    try:
        result = await recommender.recommend(preferences)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
