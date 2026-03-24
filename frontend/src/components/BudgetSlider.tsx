"use client";

import { Slider } from "@/components/ui/slider";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { DollarSign } from "lucide-react";

interface BudgetSliderProps {
  value: number;
  onChange: (value: number) => void;
}

export function BudgetSlider({ value, onChange }: BudgetSliderProps) {
  return (
    <div className="space-y-3">
      <Label className="flex items-center gap-2 text-sm font-medium">
        <DollarSign className="w-4 h-4" />
        餐标预算
      </Label>
      <div className="flex items-center gap-4">
        <Slider
          value={[value]}
          onValueChange={([v]) => onChange(v)}
          min={5}
          max={100}
          step={1}
          className="flex-1"
        />
        <div className="flex items-center gap-1 shrink-0">
          <span className="text-sm text-muted-foreground">¥</span>
          <Input
            type="number"
            value={value}
            onChange={(e) => {
              const v = Number(e.target.value);
              if (v >= 5 && v <= 100) onChange(v);
            }}
            className="w-16 h-8 text-center text-sm"
            min={5}
            max={100}
          />
        </div>
      </div>
      <p className="text-xs text-muted-foreground">
        系统将在 ¥{Math.max(5, value - 3)} ~ ¥{Math.min(100, value + 3)} 范围内推荐
      </p>
    </div>
  );
}
