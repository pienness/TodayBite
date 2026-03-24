from pydantic import BaseModel, Field
from typing import Optional

from app.models.enums import (
    MealType,
    CalorieConfidence,
    NutrientLevel,
)


# ========== 店铺 & 商品数据模型 ==========

class Review(BaseModel):
    id: str
    product_id: Optional[str] = None
    shop_id: str
    rating: float = Field(ge=1, le=5)
    content: str
    tags: list[str] = []


class Product(BaseModel):
    id: str
    shop_id: str
    name: str
    price: float
    description: str = ""
    image_url: str = ""
    category: str = ""
    monthly_sales: int = 0


class Shop(BaseModel):
    id: str
    name: str
    rating: float = Field(ge=1, le=5)
    distance: int  # 米
    delivery_fee: float
    min_order: float
    delivery_time: str = ""
    tags: list[str] = []
    products: list[Product] = []
    reviews: list[Review] = []


# ========== 用户偏好 ==========

class UserPreferences(BaseModel):
    budget: float = Field(ge=5, le=100, description="餐标预算(元)")
    budget_flex: float = Field(default=3, description="预算弹性(元)")
    calorie_target: Optional[int] = Field(default=None, description="目标热量(kcal)")
    nutrients: list[str] = Field(default=[], description="营养素偏好标签")
    taste_like: list[str] = Field(default=[], description="口味正向偏好")
    taste_exclude: list[str] = Field(default=[], description="口味排除项")
    meal_type: Optional[MealType] = Field(default=None, description="用餐场景")
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ========== 推荐结果 ==========

class RecommendedItem(BaseModel):
    product_id: str
    shop_id: str
    shop_name: str
    name: str
    price: float
    image_url: str = ""
    estimated_calories: Optional[int] = None
    nutrients: list[str] = []


class DeliveryFee(BaseModel):
    shop: str
    fee: float


class NutrientSummary(BaseModel):
    protein: NutrientLevel = NutrientLevel.MEDIUM
    fiber: NutrientLevel = NutrientLevel.MEDIUM
    fat: NutrientLevel = NutrientLevel.MEDIUM
    carbs: NutrientLevel = NutrientLevel.MEDIUM


class MealPlan(BaseModel):
    id: str
    score: float = Field(ge=0, le=1, description="综合匹配度")
    total_price: float
    total_calories: Optional[int] = None
    calorie_confidence: CalorieConfidence = CalorieConfidence.MEDIUM
    shops_count: int = 1
    items: list[RecommendedItem] = []
    delivery_fees: list[DeliveryFee] = []
    nutrient_summary: Optional[NutrientSummary] = None
    review_summary: str = ""
    meal_advice: str = ""


class RecommendResponse(BaseModel):
    plans: list[MealPlan] = []
    message: str = ""


# ========== LLM 分析结果 ==========

class DishAnalysis(BaseModel):
    name: str
    estimated_calories: int
    confidence: CalorieConfidence = CalorieConfidence.MEDIUM
    main_ingredients: list[str] = []
    nutrients: dict[str, str] = {}
    taste_tags: list[str] = []
    contains_allergens: list[str] = []
