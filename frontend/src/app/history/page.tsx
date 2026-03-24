"use client";

import Link from "next/link";
import { ArrowLeft, History } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HistoryPage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-2xl mx-auto px-4 py-6">
        {/* 顶部导航 */}
        <div className="flex items-center gap-3 mb-6">
          <Link href="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-1" />
              返回
            </Button>
          </Link>
          <h1 className="text-lg font-semibold">推荐历史</h1>
        </div>

        {/* 空状态 */}
        <div className="text-center py-16">
          <History className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <p className="text-muted-foreground">暂无推荐历史</p>
          <p className="text-sm text-muted-foreground mt-1">
            使用推荐功能后，历史记录会显示在这里
          </p>
        </div>
      </div>
    </main>
  );
}
