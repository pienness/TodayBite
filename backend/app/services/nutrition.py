"""营养数据库服务 - 食物成分表查询 + 模糊匹配"""

import json
import os
from typing import Optional


class NutritionService:
    """食物营养数据查询服务"""

    def __init__(self):
        self._db: Optional[list[dict]] = None

    def _load_db(self):
        """懒加载营养数据库"""
        if self._db is not None:
            return

        db_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "nutrition_db.json",
        )
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                self._db = json.load(f)
        except FileNotFoundError:
            self._db = []

    def lookup(self, dish_name: str) -> Optional[dict]:
        """
        查询食物营养数据
        返回: {"name", "calories", "protein", "fat", "carbs", "fiber"} 或 None
        """
        self._load_db()

        # 1. 精确匹配
        for item in self._db:
            if item["name"] == dish_name:
                return item

        # 2. 包含匹配（菜名包含数据库中的食物名）
        for item in self._db:
            if item["name"] in dish_name or dish_name in item["name"]:
                return item

        # 3. 关键词模糊匹配
        for item in self._db:
            keywords = item.get("keywords", [])
            for kw in keywords:
                if kw in dish_name:
                    return item

        return None

    def batch_lookup(self, dish_names: list[str]) -> dict[str, Optional[dict]]:
        """批量查询，返回 {菜名: 营养数据或None}"""
        return {name: self.lookup(name) for name in dish_names}


nutrition_service = NutritionService()
