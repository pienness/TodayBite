// ========== 店铺 & 商品 ==========

export interface Review {
  id: string;
  product_id?: string;
  shop_id: string;
  rating: number;
  content: string;
  tags: string[];
}

export interface Product {
  id: string;
  shop_id: string;
  name: string;
  price: number;
  description: string;
  image_url: string;
  category: string;
  monthly_sales: number;
}

export interface Shop {
  id: string;
  name: string;
  rating: number;
  distance: number;
  delivery_fee: number;
  min_order: number;
  delivery_time: string;
  tags: string[];
  products: Product[];
  reviews: Review[];
}

// ========== 用户偏好 ==========

export type MealType =
  | "breakfast"
  | "lunch"
  | "afternoon_tea"
  | "dinner"
  | "late_night";

export interface UserPreferences {
  budget: number;
  budget_flex: number;
  calorie_target: number | null;
  nutrients: string[];
  taste_like: string[];
  taste_exclude: string[];
  meal_type: MealType | null;
  latitude: number | null;
  longitude: number | null;
}

// ========== 推荐结果 ==========

export type CalorieConfidence = "high" | "medium" | "low";

export type NutrientLevel = "高" | "中" | "低";

export interface RecommendedItem {
  product_id: string;
  shop_id: string;
  shop_name: string;
  name: string;
  price: number;
  image_url: string;
  estimated_calories: number | null;
  nutrients: string[];
}

export interface DeliveryFee {
  shop: string;
  fee: number;
}

export interface NutrientSummary {
  protein: NutrientLevel;
  fiber: NutrientLevel;
  fat: NutrientLevel;
  carbs: NutrientLevel;
}

export interface MealPlan {
  id: string;
  score: number;
  total_price: number;
  total_calories: number | null;
  calorie_confidence: CalorieConfidence;
  shops_count: number;
  items: RecommendedItem[];
  delivery_fees: DeliveryFee[];
  nutrient_summary: NutrientSummary | null;
  review_summary: string;
  meal_advice: string;
}

export interface RecommendResponse {
  plans: MealPlan[];
  message: string;
}

// ========== 常量 ==========

export const NUTRIENT_TAGS = [
  "高蛋白",
  "膳食纤维",
  "维生素B族",
  "维生素C",
  "低脂",
  "低碳水",
  "富含铁",
  "富含钙",
  "Omega-3",
] as const;

export const TASTE_LIKE_TAGS = [
  "辣",
  "微辣",
  "清淡",
  "酸甜",
  "咸鲜",
  "麻辣",
] as const;

export const TASTE_EXCLUDE_TAGS = [
  "不吃辣",
  "不吃蒜",
  "不吃香菜",
  "不吃猪肉",
  "不吃牛肉",
  "不吃海鲜",
  "不吃内脏",
  "素食",
  "无乳糖",
  "无麸质",
] as const;

export const CALORIE_PRESETS = [
  { label: "轻食", value: 400 },
  { label: "正常", value: 600 },
  { label: "大餐", value: 800 },
] as const;
