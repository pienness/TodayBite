# TodayBite — 技术设计文档

> 版本: v0.1 | 日期: 2026-03-24

---

## 1. 技术选型

### 1.1 总览

| 层级 | 技术 | 版本 | 理由 |
|---|---|---|---|
| **前端框架** | Next.js (App Router) | 14.x | React 生态、SSR、API Routes 一体化 |
| **UI 框架** | TailwindCSS + shadcn/ui | 最新 | 现代化组件库，开发效率高 |
| **图标** | Lucide React | 最新 | 轻量、风格统一 |
| **后端** | Next.js API Routes + Python FastAPI | 14.x / 0.110+ | 前端路由用 Next.js，AI 推荐引擎用 Python |
| **LLM 接口** | 可插拔设计 | - | 支持 OpenAI / DeepSeek / 通义千问 / Ollama |
| **数据库** | SQLite (better-sqlite3) | - | MVP 阶段轻量，无需额外部署 |
| **食物营养库** | 中国食物成分表数据 | - | 内置常见食物营养数据 |
| **定位** | 浏览器 Geolocation API | - | 获取经纬度 |
| **状态管理** | Zustand | 最新 | 轻量、简洁 |
| **包管理器** | pnpm | 最新 | 速度快、磁盘效率高 |

### 1.2 为什么选择 Next.js + Python 双后端？

- **Next.js API Routes**：处理前端页面渲染、用户偏好存取、Mock 数据服务等轻量逻辑
- **Python FastAPI**：处理 AI 推荐引擎的核心逻辑（LLM 调用、热量估算、组合优化）
  - Python 的 AI/ML 生态远优于 Node.js
  - 方便后续扩展（接入食物识别、更复杂的推荐算法等）
- 两者通过 HTTP 内部通信，Next.js 作为 BFF (Backend For Frontend) 层

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      客户端 (浏览器)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │  定位模块    │  │  偏好输入 UI  │  │  推荐结果展示 UI  │   │
│  │ Geolocation │  │  Tags/Slider │  │  Cards/Charts    │   │
│  └─────────────┘  └──────────────┘  └───────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────────┐
│               Next.js 应用 (BFF + SSR)                       │
│                                                              │
│  ┌─────────────────┐  ┌──────────────────────────────────┐  │
│  │  页面路由 (SSR)  │  │  API Routes (/api/*)             │  │
│  │  /              │  │  /api/shops     → Mock 数据服务    │  │
│  │  /recommend     │  │  /api/recommend → 转发到推荐引擎   │  │
│  │  /history       │  │  /api/prefs     → 偏好存取        │  │
│  └─────────────────┘  └──────────────┬───────────────────┘  │
│                                       │                      │
└───────────────────────────────────────┼──────────────────────┘
                                        │ HTTP (内部)
┌───────────────────────────────────────▼──────────────────────┐
│              Python FastAPI 推荐引擎                          │
│                                                              │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐  │
│  │  LLM 服务层   │  │  推荐算法模块  │  │  营养数据库模块  │  │
│  │              │  │              │  │                  │  │
│  │ · 热量估算   │  │ · 硬筛选     │  │ · 食物成分表    │  │
│  │ · 食材识别   │  │ · 多维打分   │  │ · 营养素映射    │  │
│  │ · 评论摘要   │  │ · 组合优化   │  │ · 匹配查询     │  │
│  │ · 用餐建议   │  │ · 方案排序   │  │                  │  │
│  └──────────────┘  └───────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            LLM Provider (可插拔)                       │   │
│  │  OpenAI │ DeepSeek │ 通义千问 │ Ollama (本地)         │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. 目录结构

```
TodayBite/
├── docs/                        # 文档
│   ├── PRD.md                   # 产品需求文档
│   └── TECH_DESIGN.md           # 技术设计文档 (本文件)
│
├── frontend/                    # Next.js 前端 + BFF
│   ├── app/                     # App Router 页面
│   │   ├── layout.tsx           # 根布局
│   │   ├── page.tsx             # 首页（偏好输入）
│   │   ├── recommend/
│   │   │   └── page.tsx         # 推荐结果页
│   │   └── history/
│   │       └── page.tsx         # 推荐历史页
│   ├── components/              # UI 组件
│   │   ├── ui/                  # shadcn/ui 基础组件
│   │   ├── LocationPicker.tsx   # 定位组件
│   │   ├── BudgetSlider.tsx     # 预算滑块
│   │   ├── CalorieSelector.tsx  # 热量选择
│   │   ├── NutrientTags.tsx     # 营养素标签
│   │   ├── TasteTags.tsx        # 口味标签（正向+排除）
│   │   ├── RecommendCard.tsx    # 推荐方案卡片
│   │   └── MealSummary.tsx      # 用餐摘要
│   ├── lib/                     # 工具函数
│   │   ├── api.ts               # API 调用封装
│   │   ├── store.ts             # Zustand 状态管理
│   │   └── types.ts             # TypeScript 类型定义
│   ├── api/                     # Next.js API Routes
│   │   ├── shops/route.ts       # Mock 店铺数据
│   │   ├── recommend/route.ts   # 推荐接口（转发）
│   │   └── prefs/route.ts       # 偏好存取
│   ├── public/                  # 静态资源
│   │   └── mock-images/         # Mock 菜品图片
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.js
│
├── backend/                     # Python 推荐引擎
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── routers/
│   │   │   └── recommend.py     # 推荐接口路由
│   │   ├── services/
│   │   │   ├── llm_service.py   # LLM 可插拔服务层
│   │   │   ├── recommender.py   # 核心推荐算法
│   │   │   ├── nutrition.py     # 营养数据查询
│   │   │   └── calorie.py       # 热量估算
│   │   ├── models/
│   │   │   ├── schemas.py       # Pydantic 数据模型
│   │   │   └── enums.py         # 枚举定义
│   │   ├── data/
│   │   │   ├── nutrition_db.json # 食物营养数据库
│   │   │   └── mock_shops.json  # Mock 店铺数据
│   │   └── config.py            # 配置（LLM key 等）
│   ├── requirements.txt
│   └── .env.example             # 环境变量模板
│
├── .gitignore
├── .env.example                 # 全局环境变量模板
└── README.md                    # 项目说明
```

---

## 4. 核心模块设计

### 4.1 LLM 可插拔服务层

```python
# 设计思路：策略模式，运行时切换 LLM 提供商

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], temperature: float) -> str:
        pass

class OpenAIProvider(LLMProvider): ...
class DeepSeekProvider(LLMProvider): ...
class QwenProvider(LLMProvider): ...
class OllamaProvider(LLMProvider): ...

class LLMService:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def estimate_calories(self, dish_name, description, reviews) -> CalorieEstimate: ...
    async def analyze_ingredients(self, dish_name, description) -> list[str]: ...
    async def summarize_reviews(self, reviews: list[str]) -> str: ...
    async def generate_meal_advice(self, meal_plan: MealPlan) -> str: ...
```

### 4.2 推荐算法核心

```python
class Recommender:
    """核心推荐引擎"""

    async def recommend(self, preferences: UserPreferences, shops: list[Shop]) -> list[MealPlan]:
        # Step 1: 硬筛选
        candidates = self._hard_filter(shops, preferences)

        # Step 2: LLM 分析（批量）
        analyzed = await self._llm_analyze(candidates)

        # Step 3: 多维打分
        scored = self._score(analyzed, preferences)

        # Step 4: 组合优化（背包问题变体）
        plans = self._optimize_combinations(scored, preferences)

        # Step 5: 生成用餐建议
        for plan in plans:
            plan.advice = await self.llm.generate_meal_advice(plan)

        return plans[:3]  # 返回 Top 3

    def _hard_filter(self, shops, prefs):
        """硬约束过滤：排除禁忌食材、超出预算范围"""
        ...

    def _score(self, candidates, prefs):
        """多维度加权评分"""
        weights = {
            'calorie_match': 0.30,
            'nutrient_match': 0.20,
            'price_match': 0.20,
            'shop_rating': 0.15,
            'distance': 0.15,
        }
        ...

    def _optimize_combinations(self, scored, prefs):
        """组合优化：单店优先，考虑起送价和配送费"""
        # 1. 尝试单店方案
        single_plans = self._find_single_shop_plans(scored, prefs)

        # 2. 如果单店方案不够好，尝试双店
        dual_plans = self._find_dual_shop_plans(scored, prefs)

        # 3. 最后尝试三店
        triple_plans = self._find_triple_shop_plans(scored, prefs)

        # 合并排序
        all_plans = single_plans + dual_plans + triple_plans
        return sorted(all_plans, key=lambda p: p.total_score, reverse=True)
```

### 4.3 热量估算策略

```
热量估算流程：
    │
    ▼
1. 先查询内置食物营养数据库（精确匹配/模糊匹配）
    │
    ├── 命中 → 直接返回数据库中的热量值（精度高）
    │
    └── 未命中 → 进入 Step 2
    │
    ▼
2. LLM 估算（基于菜名 + 描述 + 评论）
    │
    ▼
3. 返回估算值，标注数据来源和置信度
    │
    ├── 数据库命中: 置信度 高 (±10%)
    └── LLM 估算:  置信度 中 (±30%)
```

---

## 5. API 设计

### 5.1 前端 → Next.js BFF

#### GET /api/shops
获取附近店铺及菜品（MVP 阶段返回 Mock 数据）

**请求参数：**
```json
{
  "latitude": 31.2304,
  "longitude": 121.4737
}
```

**响应：**
```json
{
  "shops": [
    {
      "id": "shop_001",
      "name": "XX黄焖鸡",
      "rating": 4.5,
      "distance": 800,
      "delivery_fee": 3,
      "min_order": 20,
      "delivery_time": "30-40分钟",
      "tags": ["快餐", "米饭"],
      "products": [
        {
          "id": "prod_001",
          "name": "黄焖鸡米饭(大份)",
          "price": 22,
          "description": "鸡腿肉搭配土豆、青椒，酱香浓郁",
          "image_url": "/mock-images/hmj.jpg",
          "category": "主食",
          "monthly_sales": 356
        }
      ],
      "reviews": [
        {
          "rating": 5,
          "content": "份量很大，鸡肉很嫩，推荐！",
          "tags": ["份量大", "味道好"]
        }
      ]
    }
  ]
}
```

#### POST /api/recommend
请求智能推荐

**请求体：**
```json
{
  "budget": 25,
  "budget_flex": 3,
  "calorie_target": 600,
  "nutrients": ["高蛋白", "膳食纤维"],
  "taste_like": ["微辣"],
  "taste_exclude": ["不吃香菜", "不吃内脏"],
  "meal_type": "lunch",
  "latitude": 31.2304,
  "longitude": 121.4737
}
```

**响应：**
```json
{
  "plans": [
    {
      "id": "plan_001",
      "score": 0.92,
      "total_price": 26,
      "total_calories": 580,
      "calorie_confidence": "medium",
      "shops_count": 1,
      "items": [
        {
          "product_id": "prod_001",
          "shop_id": "shop_001",
          "shop_name": "XX黄焖鸡",
          "name": "黄焖鸡米饭(大份)",
          "price": 22,
          "image_url": "/mock-images/hmj.jpg",
          "estimated_calories": 580,
          "nutrients": ["高蛋白", "碳水"]
        }
      ],
      "delivery_fees": [{"shop": "XX黄焖鸡", "fee": 3}],
      "nutrient_summary": {
        "protein": "高",
        "fiber": "低",
        "fat": "中",
        "carbs": "高"
      },
      "review_summary": "多数用户评价份量足、味道好、鸡肉嫩滑，少数反映偶尔偏咸。",
      "meal_advice": "此餐蛋白质充足但蔬菜偏少，建议餐后补充一份水果。"
    }
  ]
}
```

### 5.2 Next.js BFF → Python 推荐引擎

#### POST http://localhost:8000/recommend
与前端接口相同的请求/响应结构，BFF 层负责透传 + 缓存。

---

## 6. 开发阶段规划

### P0 - 核心验证 (第 1-2 周)

| 任务 | 优先级 | 预估工时 |
|---|---|---|
| 项目脚手架搭建 (Next.js + FastAPI) | 高 | 0.5 天 |
| Mock 数据设计与生成 (15-20 家店) | 高 | 1 天 |
| 食物营养数据库整理 (500+ 常见食物) | 高 | 1 天 |
| 用户偏好输入 UI | 高 | 2 天 |
| LLM 可插拔服务层 | 高 | 1 天 |
| 推荐引擎核心算法 | 高 | 3 天 |
| 推荐结果展示 UI | 高 | 2 天 |
| 联调 & 基础测试 | 高 | 1.5 天 |

### P1 - 体验完善 (第 3-4 周)

| 任务 | 优先级 |
|---|---|
| 浏览器定位功能 | 中 |
| 时段感知逻辑 | 中 |
| "换一批" & "不喜欢" 交互 | 中 |
| 偏好 localStorage 记忆 | 中 |
| 推荐历史页 | 中 |
| 响应式移动端适配 | 中 |
| 性能优化 (LLM 流式输出) | 中 |

### P2 - 真实数据 (第 5-6 周)

| 任务 | 优先级 |
|---|---|
| 调研真实数据接入方案 | 高 |
| 数据适配层开发 | 高 |
| 用户反馈系统 | 低 |
| 推荐算法调优 | 中 |

---

## 7. 环境变量

```env
# LLM 配置
LLM_PROVIDER=openai          # openai / deepseek / qwen / ollama
LLM_API_KEY=your_api_key
LLM_API_BASE=                # 可选，自定义 API 地址
LLM_MODEL=gpt-4o-mini        # 使用的模型名

# 服务配置
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 8. 风险与应对

| 风险 | 影响 | 应对措施 |
|---|---|---|
| LLM 响应慢 (>5s) | 用户体验差 | 流式输出 + 骨架屏加载 |
| LLM 热量估算偏差大 | 误导用户 | 标注置信度 + 数据库优先 + 免责声明 |
| LLM 服务不可用 | 核心功能瘫痪 | 降级为纯规则推荐(无热量/评论摘要) |
| Mock 数据不够真实 | MVP 演示效果差 | 参考真实外卖平台精心构造 |
| 多店组合计算量大 | 响应超时 | 限制候选集 + 贪心算法剪枝 |
