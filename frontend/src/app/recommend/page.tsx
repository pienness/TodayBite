"use client";

import { useRecommendStore } from "@/lib/store";
import Link from "next/link";
import { ArrowLeft, RefreshCw, Settings2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { RecommendCard } from "@/components/RecommendCard";
import { Skeleton } from "@/components/ui/skeleton";

export default function RecommendPage() {
  const { plans, loading, error, message } = useRecommendStore();

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-2xl mx-auto px-4 py-6">
        {/* 顶部导航 */}
        <div className="flex items-center justify-between mb-6">
          <Link href="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-1" />
              调整偏好
            </Button>
          </Link>
          <h1 className="text-lg font-semibold">推荐方案</h1>
          <Button variant="ghost" size="sm" disabled={loading}>
            <RefreshCw className="w-4 h-4 mr-1" />
            换一批
          </Button>
        </div>

        {/* 加载状态 */}
        {loading && (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="rounded-lg border p-4 space-y-3">
                <Skeleton className="h-6 w-1/3" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-2/3" />
                <div className="flex gap-2">
                  <Skeleton className="h-20 w-20 rounded" />
                  <div className="flex-1 space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-1/2" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* 错误状态 */}
        {error && (
          <div className="text-center py-12">
            <p className="text-destructive mb-4">{error}</p>
            <Link href="/">
              <Button variant="outline">
                <Settings2 className="w-4 h-4 mr-1" />
                重新设置偏好
              </Button>
            </Link>
          </div>
        )}

        {/* 无结果 */}
        {!loading && !error && plans.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground mb-2">
              {message || "暂无推荐结果"}
            </p>
            <Link href="/">
              <Button variant="outline">
                <Settings2 className="w-4 h-4 mr-1" />
                调整偏好重试
              </Button>
            </Link>
          </div>
        )}

        {/* 推荐结果 */}
        {!loading && plans.length > 0 && (
          <div className="space-y-4">
            {plans.map((plan, index) => (
              <RecommendCard key={plan.id} plan={plan} rank={index + 1} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
