"""LLM 可插拔服务层 - 策略模式，支持运行时切换 LLM 提供商"""

import json
from abc import ABC, abstractmethod
from typing import Optional

from openai import AsyncOpenAI

from app.config import settings
from app.models.schemas import DishAnalysis


class LLMProvider(ABC):
    """LLM 提供商抽象基类"""

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        response_format: Optional[dict] = None,
    ) -> str:
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI / OpenAI 兼容 API 提供商（同时支持 DeepSeek、通义千问等兼容接口）"""

    def __init__(self, api_key: str, model: str, base_url: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        response_format: Optional[dict] = None,
    ) -> str:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format:
            kwargs["response_format"] = response_format

        response = await self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""


class OllamaProvider(LLMProvider):
    """Ollama 本地模型提供商"""

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.client = AsyncOpenAI(api_key="ollama", base_url=f"{base_url}/v1")
        self.model = model

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        response_format: Optional[dict] = None,
    ) -> str:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format:
            kwargs["response_format"] = response_format

        response = await self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""


def create_llm_provider() -> LLMProvider:
    """根据配置创建对应的 LLM Provider"""
    provider = settings.LLM_PROVIDER.lower()

    if provider in ("openai", "deepseek", "qwen"):
        base_url = settings.LLM_API_BASE or None
        # DeepSeek 和通义千问使用 OpenAI 兼容接口
        if provider == "deepseek" and not base_url:
            base_url = "https://api.deepseek.com"
        elif provider == "qwen" and not base_url:
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

        return OpenAIProvider(
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_MODEL,
            base_url=base_url,
        )
    elif provider == "ollama":
        return OllamaProvider(
            model=settings.LLM_MODEL,
            base_url=settings.LLM_API_BASE or "http://localhost:11434",
        )
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")


class LLMService:
    """LLM 高层服务 - 封装业务级别的 LLM 调用"""

    def __init__(self):
        self.provider: Optional[LLMProvider] = None

    def _ensure_provider(self):
        if self.provider is None:
            self.provider = create_llm_provider()

    async def batch_analyze_dishes(
        self, dishes: list[dict]
    ) -> list[DishAnalysis]:
        """批量分析候选菜品：热量估算、食材识别、营养素标签、口味标签"""
        self._ensure_provider()

        prompt = f"""你是一个专业的营养师。请分析以下菜品，为每道菜返回 JSON 数组。

菜品列表：
{json.dumps(dishes, ensure_ascii=False, indent=2)}

对每道菜返回以下字段：
- name: 菜品名称
- estimated_calories: 估算热量(kcal)，基于一份正常外卖的量
- confidence: 估算置信度 "high"/"medium"/"low"
- main_ingredients: 主要食材列表
- nutrients: 营养素水平 {{"protein": "高/中/低", "fat": "高/中/低", "carbs": "高/中/低", "fiber": "高/中/低"}}
- taste_tags: 口味标签 如 ["辣", "咸鲜"]
- contains_allergens: 包含的常见过敏原/禁忌食材

请只返回 JSON 数组，不要其他内容。"""

        response = await self.provider.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        try:
            data = json.loads(response)
            # 兼容 LLM 可能返回 {"dishes": [...]} 或 直接 [...]
            items = data if isinstance(data, list) else data.get("dishes", data.get("items", []))
            return [DishAnalysis(**item) for item in items]
        except (json.JSONDecodeError, Exception):
            return []

    async def generate_review_summary_and_advice(
        self,
        items: list[dict],
        reviews: list[str],
    ) -> dict:
        """生成评论摘要和用餐建议"""
        self._ensure_provider()

        prompt = f"""你是一个饮食顾问。根据以下外卖菜品和用户评论，生成：

已选菜品：
{json.dumps(items, ensure_ascii=False)}

相关评论：
{json.dumps(reviews[:20], ensure_ascii=False)}

请返回 JSON 对象：
{{
  "review_summary": "综合评论摘要（50字以内，提炼正面和负面评价）",
  "meal_advice": "用餐建议（80字以内，从营养均衡角度给出建议）"
}}"""

        response = await self.provider.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "review_summary": "暂无评论摘要",
                "meal_advice": "建议荤素搭配，注意营养均衡。",
            }


llm_service = LLMService()
