"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { usePreferencesStore, useRecommendStore } from "@/lib/store";
import { fetchRecommendations } from "@/lib/api";
import { BudgetSlider } from "@/components/BudgetSlider";
import { CalorieSelector } from "@/components/CalorieSelector";
import { NutrientTags } from "@/components/NutrientTags";
import { TasteTags } from "@/components/TasteTags";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { UtensilsCrossed, MapPin, History, Loader2 } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const {
    preferences,
    setBudget,
    setCalorieTarget,
    toggleNutrient,
    toggleTasteLike,
    toggleTasteExclude,
  } = usePreferencesStore();
  const { loading, setLoading, setResult, setError } = useRecommendStore();

  const handleRecommend = async () => {
    setLoading(true);
    try {
      const result = await fetchRecommendations(preferences);
      setResult(result);
      router.push("/recommend");
    } catch (err) {
      setError(err instanceof Error ? err.message : "请求失败");
      router.push("/recommend");
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-2xl mx-auto px-4 py-6">
        {/* 顶部标题 */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <UtensilsCrossed className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-bold">TodayBite</h1>
          </div>
          <Link href="/history">
            <Button variant="ghost" size="sm">
              <History className="w-4 h-4 mr-1" />
              历史
            </Button>
          </Link>
        </div>

        <p className="text-muted-foreground text-sm mb-6">
          告诉我你的偏好，为你推荐最合适的外卖组合
        </p>

        {/* 定位信息 */}
        <Card className="mb-6">
          <CardContent className="flex items-center gap-2 py-3 px-4">
            <MapPin className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">
              {preferences.latitude
                ? `已定位 (${preferences.latitude.toFixed(4)}, ${preferences.longitude?.toFixed(4)})`
                : "使用 Mock 数据 · 无需定位"}
            </span>
          </CardContent>
        </Card>

        {/* 偏好设置 */}
        <div className="space-y-6">
          <BudgetSlider value={preferences.budget} onChange={setBudget} />

          <Separator />

          <CalorieSelector
            value={preferences.calorie_target}
            onChange={setCalorieTarget}
          />

          <Separator />

          <NutrientTags
            selected={preferences.nutrients}
            onToggle={toggleNutrient}
          />

          <Separator />

          <TasteTags
            tasteLike={preferences.taste_like}
            tasteExclude={preferences.taste_exclude}
            onToggleLike={toggleTasteLike}
            onToggleExclude={toggleTasteExclude}
          />
        </div>

        {/* 推荐按钮 */}
        <div className="mt-8 mb-4">
          <Button
            onClick={handleRecommend}
            disabled={loading}
            className="w-full h-12 text-base font-semibold"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                正在为你推荐...
              </>
            ) : (
              <>
                <UtensilsCrossed className="w-5 h-5 mr-2" />
                开始推荐
              </>
            )}
          </Button>
        </div>
      </div>
    </main>
  );
}
