"use client";

import type { MealPlan } from "@/lib/types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Flame,
  DollarSign,
  Store,
  MessageSquare,
  Lightbulb,
} from "lucide-react";

interface RecommendCardProps {
  plan: MealPlan;
  rank: number;
}

export function RecommendCard({ plan, rank }: RecommendCardProps) {
  const matchPercent = Math.round(plan.score * 100);

  return (
    <Card className="overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold">
              {rank}
            </span>
            推荐方案 {rank}
          </CardTitle>
          <Badge variant={matchPercent >= 80 ? "default" : "secondary"}>
            匹配度 {matchPercent}%
          </Badge>
        </div>
        <CardDescription className="flex items-center gap-4 text-sm">
          <span className="flex items-center gap-1">
            <DollarSign className="w-3.5 h-3.5" />¥{plan.total_price}
          </span>
          {plan.total_calories && (
            <span className="flex items-center gap-1">
              <Flame className="w-3.5 h-3.5" />
              约{plan.total_calories}kcal
              <span className="text-xs text-muted-foreground">
                ({plan.calorie_confidence === "high"
                  ? "精确"
                  : plan.calorie_confidence === "medium"
                  ? "估算"
                  : "粗估"})
              </span>
            </span>
          )}
          <span className="flex items-center gap-1">
            <Store className="w-3.5 h-3.5" />
            {plan.shops_count}家店
          </span>
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* 菜品列表 */}
        <div className="space-y-2">
          {plan.items.map((item) => (
            <div
              key={item.product_id}
              className="flex items-center gap-3 p-2 rounded-lg bg-muted/50"
            >
              <div className="w-14 h-14 rounded-md bg-muted flex items-center justify-center text-2xl shrink-0">
                🍽️
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm truncate">{item.name}</p>
                <p className="text-xs text-muted-foreground">
                  {item.shop_name}
                </p>
                {item.nutrients.length > 0 && (
                  <div className="flex gap-1 mt-1 flex-wrap">
                    {item.nutrients.map((n) => (
                      <Badge key={n} variant="outline" className="text-[10px] px-1 py-0">
                        {n}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
              <div className="text-right shrink-0">
                <p className="font-semibold text-sm">¥{item.price}</p>
                {item.estimated_calories && (
                  <p className="text-xs text-muted-foreground">
                    {item.estimated_calories}kcal
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* 配送费明细 */}
        {plan.delivery_fees.length > 0 && (
          <div className="text-xs text-muted-foreground">
            配送费：
            {plan.delivery_fees
              .map((f) => `${f.shop} ¥${f.fee}`)
              .join(" + ")}
          </div>
        )}

        <Separator />

        {/* 营养素概览 */}
        {plan.nutrient_summary && (
          <div className="flex gap-3 text-xs">
            <span>蛋白质: {plan.nutrient_summary.protein}</span>
            <span>脂肪: {plan.nutrient_summary.fat}</span>
            <span>碳水: {plan.nutrient_summary.carbs}</span>
            <span>纤维: {plan.nutrient_summary.fiber}</span>
          </div>
        )}

        {/* 评论摘要 */}
        {plan.review_summary && (
          <div className="flex gap-2 text-sm">
            <MessageSquare className="w-4 h-4 text-muted-foreground shrink-0 mt-0.5" />
            <p className="text-muted-foreground">{plan.review_summary}</p>
          </div>
        )}

        {/* 用餐建议 */}
        {plan.meal_advice && (
          <div className="flex gap-2 text-sm bg-primary/5 rounded-lg p-2">
            <Lightbulb className="w-4 h-4 text-primary shrink-0 mt-0.5" />
            <p>{plan.meal_advice}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
