"use client";

import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Apple } from "lucide-react";
import { NUTRIENT_TAGS } from "@/lib/types";

interface NutrientTagsProps {
  selected: string[];
  onToggle: (tag: string) => void;
}

export function NutrientTags({ selected, onToggle }: NutrientTagsProps) {
  return (
    <div className="space-y-3">
      <Label className="flex items-center gap-2 text-sm font-medium">
        <Apple className="w-4 h-4" />
        营养素偏好
      </Label>
      <div className="flex flex-wrap gap-2">
        {NUTRIENT_TAGS.map((tag) => {
          const isSelected = selected.includes(tag);
          return (
            <Badge
              key={tag}
              variant={isSelected ? "default" : "outline"}
              className="cursor-pointer select-none transition-colors"
              onClick={() => onToggle(tag)}
            >
              {tag}
            </Badge>
          );
        })}
      </div>
      <p className="text-xs text-muted-foreground">
        选择你希望这餐包含的营养素（可多选）
      </p>
    </div>
  );
}
