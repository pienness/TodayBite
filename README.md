# 🍱 TodayBite — 智能外卖推荐助手

基于用户位置获取附近外卖信息，结合预算、热量、营养素、口味偏好，智能推荐最优外卖组合。

## 功能特性

- **预算控制**：设定餐标价格，系统在 ±3 元范围内智能筛选
- **热量估算**：AI + 食物营养数据库双重估算菜品热量
- **营养素偏好**：支持高蛋白、膳食纤维、低脂等多种营养素标签
- **口味偏好**：支持正向偏好和排除项（不吃辣、不吃香菜等）
- **智能组合**：优先单店推荐，支持最多 3 家店联合搭配
- **用餐建议**：AI 生成营养分析和饮食建议

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Next.js 14 + TailwindCSS + shadcn/ui |
| 后端 | Python FastAPI |
| LLM | 可插拔设计（OpenAI / DeepSeek / 通义千问 / Ollama） |
| 数据库 | SQLite (MVP) |

## 项目结构

```
TodayBite/
├── docs/           # 产品 & 技术文档
├── frontend/       # Next.js 前端 + BFF
└── backend/        # Python FastAPI 推荐引擎
```

## 快速开始

> 🚧 项目开发中，敬请期待...

## 文档

- [产品需求文档 (PRD)](./docs/PRD.md)
- [技术设计文档](./docs/TECH_DESIGN.md)

## License

MIT
