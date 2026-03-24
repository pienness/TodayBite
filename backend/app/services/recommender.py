"""核心推荐引擎 - 硬筛选 → LLM分析 → 多维打分 → 组合优化"""

import uuid
from typing import Optional

from app.models.schemas import (
    UserPreferences,
    RecommendResponse,
    MealPlan,
    RecommendedItem,
    DeliveryFee,
    NutrientSummary,
    Shop,
    Product,
)
from app.models.enums import CalorieConfidence, NutrientLevel
from app.services.calorie import calorie_estimator
from app.services.llm_service import llm_service
from app.services.mock_data import load_mock_shops


# 食材排除关键词映射
EXCLUDE_KEYWORDS: dict[str, list[str]] = {
    "不吃猪肉": ["猪", "猪肉", "五花", "排骨", "肘子", "猪蹄", "卤肉", "回锅肉", "红烧肉"],
    "不吃牛肉": ["牛", "牛肉", "牛腩", "牛排", "肥牛"],
    "不吃海鲜": ["虾", "鱼", "蟹", "蛤", "海鲜", "鱿鱼", "三文鱼", "龙虾", "贝"],
    "不吃香菜": ["香菜", "芫荽"],
    "不吃蒜": ["蒜", "大蒜", "蒜蓉"],
    "不吃内脏": ["内脏", "肝", "肠", "肚", "心", "腰子", "鸡胗", "毛肚"],
    "不吃辣": ["辣", "麻辣", "香辣", "辣椒", "剁椒", "泡椒"],
    "素食": ["肉", "鸡", "鸭", "鱼", "虾", "牛", "猪", "羊"],
    "无乳糖": ["奶", "牛奶", "乳", "芝士", "奶酪"],
    "无麸质": ["面", "面条", "馒头", "饺子", "包子", "面包"],
}


class RecommenderService:
    """推荐引擎主服务"""

    async def recommend(self, preferences: UserPreferences) -> RecommendResponse:
        """执行完整推荐流程"""
        # Step 0: 加载店铺数据（MVP 阶段使用 Mock 数据）
        shops = load_mock_shops()
        if not shops:
            return RecommendResponse(plans=[], message="附近暂无店铺数据")

        # Step 1: 硬筛选
        candidates = self._hard_filter(shops, preferences)
        if not candidates:
            return RecommendResponse(plans=[], message="没有符合条件的菜品，请尝试调整偏好")

        # Step 2: 热量估算（数据库 + LLM）
        dish_data = []
        for shop in candidates:
            for product in shop.products:
                dish_data.append({
                    "name": product.name,
                    "description": product.description,
                    "reviews": [r.content for r in shop.reviews[:5]],
                })

        calorie_results = await calorie_estimator.estimate_batch(dish_data)

        # Step 3: 多维打分
        scored_items = self._score_products(candidates, preferences, calorie_results)

        # Step 4: 组合优化
        plans = self._optimize_combinations(scored_items, candidates, preferences, calorie_results)

        if not plans:
            return RecommendResponse(plans=[], message="无法生成满足条件的推荐方案")

        # Step 5: 为 Top 方案生成评论摘要和用餐建议
        for plan in plans[:3]:
            try:
                items_info = [{"name": item.name, "price": item.price} for item in plan.items]
                reviews = self._collect_reviews_for_plan(plan, candidates)
                result = await llm_service.generate_review_summary_and_advice(
                    items_info, reviews
                )
                plan.review_summary = result.get("review_summary", "")
                plan.meal_advice = result.get("meal_advice", "")
            except Exception:
                plan.review_summary = "暂无评论摘要"
                plan.meal_advice = "建议荤素搭配，注意营养均衡。"

        return RecommendResponse(plans=plans[:3])

    def _hard_filter(
        self, shops: list[Shop], prefs: UserPreferences
    ) -> list[Shop]:
        """硬约束过滤：排除禁忌食材、明显超出预算的菜品"""
        budget_max = prefs.budget + prefs.budget_flex
        filtered_shops = []

        for shop in shops:
            filtered_products = []
            for product in shop.products:
                # 价格粗筛（单品不能超过预算上限）
                if product.price > budget_max:
                    continue

                # 食材/口味排除
                if self._should_exclude(product, prefs.taste_exclude):
                    continue

                filtered_products.append(product)

            if filtered_products:
                shop_copy = shop.model_copy()
                shop_copy.products = filtered_products
                filtered_shops.append(shop_copy)

        return filtered_shops

    def _should_exclude(self, product: Product, excludes: list[str]) -> bool:
        """检查菜品是否包含排除项"""
        text = f"{product.name} {product.description}".lower()
        for exclude in excludes:
            keywords = EXCLUDE_KEYWORDS.get(exclude, [])
            if keywords:
                for kw in keywords:
                    if kw in text:
                        return True
            else:
                # 自定义排除项，直接关键词匹配
                if exclude.replace("不吃", "") in text:
                    return True
        return False

    def _score_products(
        self,
        shops: list[Shop],
        prefs: UserPreferences,
        calorie_results: dict,
    ) -> list[dict]:
        """多维度打分"""
        scored = []
        budget_target = prefs.budget

        for shop in shops:
            for product in shop.products:
                score = 0.0

                # 价格匹配度 (20%)
                price_diff = abs(product.price - budget_target)
                price_score = max(0, 1 - price_diff / budget_target)
                score += price_score * 0.20

                # 店铺评分 (15%)
                rating_score = shop.rating / 5.0
                score += rating_score * 0.15

                # 距离分数 (15%)
                distance_score = max(0, 1 - shop.distance / 5000)
                score += distance_score * 0.15

                # 热量匹配度 (30%)
                cal_info = calorie_results.get(product.name)
                if cal_info and cal_info.get("calories") and prefs.calorie_target:
                    cal_diff = abs(cal_info["calories"] - prefs.calorie_target)
                    cal_score = max(0, 1 - cal_diff / prefs.calorie_target)
                    score += cal_score * 0.30
                else:
                    score += 0.15  # 无热量数据时给中间分

                # 营养素匹配度 (20%) - 简化版，后续可扩展
                score += 0.10  # 基础分

                scored.append({
                    "product": product,
                    "shop": shop,
                    "score": round(score, 3),
                    "calories": cal_info.get("calories") if cal_info else None,
                    "calorie_confidence": cal_info.get("confidence", CalorieConfidence.LOW) if cal_info else CalorieConfidence.LOW,
                })

        # 按分数降序排列
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def _optimize_combinations(
        self,
        scored_items: list[dict],
        shops: list[Shop],
        prefs: UserPreferences,
        calorie_results: dict,
    ) -> list[MealPlan]:
        """组合优化：单店优先 → 双店 → 三店"""
        budget_min = prefs.budget - prefs.budget_flex
        budget_max = prefs.budget + prefs.budget_flex
        plans: list[MealPlan] = []

        # 按店铺分组
        shop_items: dict[str, list[dict]] = {}
        shop_map: dict[str, Shop] = {}
        for item in scored_items:
            sid = item["shop"].id
            if sid not in shop_items:
                shop_items[sid] = []
                shop_map[sid] = item["shop"]
            shop_items[sid].append(item)

        # 1. 单店方案
        for sid, items in shop_items.items():
            shop = shop_map[sid]
            for item in items[:5]:  # 每店只取 top 5
                total_price = item["product"].price + shop.delivery_fee
                if budget_min <= total_price <= budget_max:
                    plan = self._build_plan(
                        items=[item],
                        shops_involved=[shop],
                        calorie_results=calorie_results,
                    )
                    plans.append(plan)

        # 2. 双店方案（取 top 品互补）
        shop_ids = list(shop_items.keys())
        for i in range(min(len(shop_ids), 5)):
            for j in range(i + 1, min(len(shop_ids), 5)):
                s1, s2 = shop_ids[i], shop_ids[j]
                shop1, shop2 = shop_map[s1], shop_map[s2]
                for item1 in shop_items[s1][:3]:
                    for item2 in shop_items[s2][:3]:
                        total_price = (
                            item1["product"].price
                            + item2["product"].price
                            + shop1.delivery_fee
                            + shop2.delivery_fee
                        )
                        if budget_min <= total_price <= budget_max:
                            plan = self._build_plan(
                                items=[item1, item2],
                                shops_involved=[shop1, shop2],
                                calorie_results=calorie_results,
                            )
                            plans.append(plan)

        # 按总分排序，去重
        plans.sort(key=lambda p: p.score, reverse=True)
        return plans[:10]  # 返回 top 10，最终取 top 3

    def _build_plan(
        self,
        items: list[dict],
        shops_involved: list[Shop],
        calorie_results: dict,
    ) -> MealPlan:
        """构建推荐方案"""
        rec_items = []
        total_calories = 0
        has_calories = True
        min_confidence = CalorieConfidence.HIGH

        for item_data in items:
            product = item_data["product"]
            shop = item_data["shop"]
            cal = item_data.get("calories")

            if cal:
                total_calories += cal
            else:
                has_calories = False

            conf = item_data.get("calorie_confidence", CalorieConfidence.LOW)
            if conf == CalorieConfidence.LOW:
                min_confidence = CalorieConfidence.LOW
            elif conf == CalorieConfidence.MEDIUM and min_confidence == CalorieConfidence.HIGH:
                min_confidence = CalorieConfidence.MEDIUM

            rec_items.append(
                RecommendedItem(
                    product_id=product.id,
                    shop_id=shop.id,
                    shop_name=shop.name,
                    name=product.name,
                    price=product.price,
                    image_url=product.image_url,
                    estimated_calories=cal,
                    nutrients=[],
                )
            )

        delivery_fees = [
            DeliveryFee(shop=s.name, fee=s.delivery_fee) for s in shops_involved
        ]
        total_delivery = sum(s.delivery_fee for s in shops_involved)
        total_price = sum(i["product"].price for i in items) + total_delivery

        avg_score = sum(i["score"] for i in items) / len(items) if items else 0

        return MealPlan(
            id=f"plan_{uuid.uuid4().hex[:8]}",
            score=round(avg_score, 2),
            total_price=round(total_price, 1),
            total_calories=total_calories if has_calories else None,
            calorie_confidence=min_confidence,
            shops_count=len(shops_involved),
            items=rec_items,
            delivery_fees=delivery_fees,
            nutrient_summary=NutrientSummary(),
            review_summary="",
            meal_advice="",
        )

    def _collect_reviews_for_plan(
        self, plan: MealPlan, shops: list[Shop]
    ) -> list[str]:
        """收集方案涉及的店铺评论"""
        shop_ids = {item.shop_id for item in plan.items}
        reviews = []
        for shop in shops:
            if shop.id in shop_ids:
                for review in shop.reviews[:10]:
                    reviews.append(review.content)
        return reviews
