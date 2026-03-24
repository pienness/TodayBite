"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Flame } from "lucide-react";
import { CALORIE_PRESETS } from "@/lib/types";

interface CalorieSelectorProps {
  value: number | null;
  onChange: (value: number | null) => void;
}

export function CalorieSelector({ value, onChange }: CalorieSelectorProps) {
  const presetValue = CALORIE_PRESETS.find((p) => p.value === value)?.label;

  return (
    <div className="space-y-3">
      <Label className="flex items-center gap-2 text-sm font-medium">
        <Flame className="w-4 h-4" />
        热量控制
      </Label>
      <ToggleGroup
        type="single"
        value={presetValue || ""}
        onValueChange={(v) => {
          if (!v) {
            onChange(null);
            return;
          }
          const preset = CALORIE_PRESETS.find((p) => p.label === v);
          if (preset) onChange(preset.value);
        }}
        className="justify-start"
      >
        {CALORIE_PRESETS.map((preset) => (
          <ToggleGroupItem
            key={preset.label}
            value={preset.label}
            size="sm"
            className="text-xs"
          >
            {preset.label} ~{preset.value}kcal
          </ToggleGroupItem>
        ))}
      </ToggleGroup>
      <div className="flex items-center gap-2">
        <span className="text-xs text-muted-foreground">自定义:</span>
        <Input
          type="number"
          placeholder="输入目标热量"
          value={value && !presetValue ? value : ""}
          onChange={(e) => {
            const v = e.target.value ? Number(e.target.value) : null;
            onChange(v);
          }}
          className="w-32 h-8 text-sm"
          min={200}
          max={1500}
        />
        <span className="text-xs text-muted-foreground">kcal</span>
      </div>
      <p className="text-xs text-muted-foreground">
        ⚠️ 热量为 AI 估算值，仅供参考
      </p>
    </div>
  );
}
