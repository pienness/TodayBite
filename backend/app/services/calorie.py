"""热量估算服务 - 数据库优先 + LLM 兜底"""

from typing import Optional

from app.models.enums import CalorieConfidence
from app.services.nutrition import nutrition_service
from app.services.llm_service import llm_service


class CalorieEstimator:
    """热量估算器：食物数据库优先匹配，LLM 兜底"""

    async def estimate_single(
        self, dish_name: str, description: str = "", reviews: list[str] = None
    ) -> dict:
        """
        估算单道菜的热量
        返回: {"calories": int, "confidence": str, "source": str}
        """
        # Step 1: 查询营养数据库
        db_result = nutrition_service.lookup(dish_name)
        if db_result:
            return {
                "calories": db_result["calories"],
                "confidence": CalorieConfidence.HIGH,
                "source": "database",
            }

        # Step 2: LLM 估算（单道菜场景，通常在批量分析中处理）
        return {
            "calories": None,
            "confidence": CalorieConfidence.LOW,
            "source": "pending_llm",
        }

    async def estimate_batch(
        self, dishes: list[dict]
    ) -> dict[str, dict]:
        """
        批量估算热量
        dishes: [{"name": str, "description": str, "reviews": list[str]}]
        返回: {菜名: {"calories": int, "confidence": str, "source": str}}
        """
        results = {}
        pending_llm = []

        # Step 1: 数据库批量匹配
        for dish in dishes:
            name = dish["name"]
            db_result = nutrition_service.lookup(name)
            if db_result:
                results[name] = {
                    "calories": db_result["calories"],
                    "confidence": CalorieConfidence.HIGH,
                    "source": "database",
                }
            else:
                pending_llm.append(dish)

        # Step 2: 未命中的交给 LLM 批量分析
        if pending_llm:
            llm_results = await llm_service.batch_analyze_dishes(pending_llm)
            for analysis in llm_results:
                results[analysis.name] = {
                    "calories": analysis.estimated_calories,
                    "confidence": analysis.confidence,
                    "source": "llm",
                }

        return results


calorie_estimator = CalorieEstimator()
