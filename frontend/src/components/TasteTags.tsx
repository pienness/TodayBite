"use client";

import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Heart, Ban } from "lucide-react";
import { TASTE_LIKE_TAGS, TASTE_EXCLUDE_TAGS } from "@/lib/types";

interface TasteTagsProps {
  tasteLike: string[];
  tasteExclude: string[];
  onToggleLike: (tag: string) => void;
  onToggleExclude: (tag: string) => void;
}

export function TasteTags({
  tasteLike,
  tasteExclude,
  onToggleLike,
  onToggleExclude,
}: TasteTagsProps) {
  return (
    <div className="space-y-4">
      {/* 正向偏好 */}
      <div className="space-y-3">
        <Label className="flex items-center gap-2 text-sm font-medium">
          <Heart className="w-4 h-4" />
          口味偏好
        </Label>
        <div className="flex flex-wrap gap-2">
          {TASTE_LIKE_TAGS.map((tag) => {
            const isSelected = tasteLike.includes(tag);
            return (
              <Badge
                key={tag}
                variant={isSelected ? "default" : "outline"}
                className="cursor-pointer select-none transition-colors"
                onClick={() => onToggleLike(tag)}
              >
                {tag}
              </Badge>
            );
          })}
        </div>
      </div>

      <Separator />

      {/* 排除项 */}
      <div className="space-y-3">
        <Label className="flex items-center gap-2 text-sm font-medium">
          <Ban className="w-4 h-4" />
          饮食禁忌
        </Label>
        <div className="flex flex-wrap gap-2">
          {TASTE_EXCLUDE_TAGS.map((tag) => {
            const isSelected = tasteExclude.includes(tag);
            return (
              <Badge
                key={tag}
                variant={isSelected ? "destructive" : "outline"}
                className="cursor-pointer select-none transition-colors"
                onClick={() => onToggleExclude(tag)}
              >
                {tag}
              </Badge>
            );
          })}
        </div>
        <p className="text-xs text-muted-foreground">
          选择的禁忌项将被严格排除，不会出现在推荐中
        </p>
      </div>
    </div>
  );
}
