"""Mock 数据加载服务 - MVP 阶段使用"""

import json
import os
from typing import Optional

from app.models.schemas import Shop


_mock_shops: Optional[list[Shop]] = None


def load_mock_shops() -> list[Shop]:
    """加载 Mock 店铺数据"""
    global _mock_shops
    if _mock_shops is not None:
        return _mock_shops

    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "mock_shops.json",
    )
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _mock_shops = [Shop(**shop) for shop in data]
    except FileNotFoundError:
        _mock_shops = []

    return _mock_shops
