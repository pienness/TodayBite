import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  UserPreferences,
  MealPlan,
  MealType,
  RecommendResponse,
} from "./types";

// ========== 偏好 Store ==========

interface PreferencesState {
  preferences: UserPreferences;
  setBudget: (budget: number) => void;
  setCalorieTarget: (target: number | null) => void;
  toggleNutrient: (tag: string) => void;
  toggleTasteLike: (tag: string) => void;
  toggleTasteExclude: (tag: string) => void;
  setMealType: (type: MealType | null) => void;
  setLocation: (lat: number, lng: number) => void;
  resetPreferences: () => void;
}

const defaultPreferences: UserPreferences = {
  budget: 25,
  budget_flex: 3,
  calorie_target: null,
  nutrients: [],
  taste_like: [],
  taste_exclude: [],
  meal_type: null,
  latitude: null,
  longitude: null,
};

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      preferences: { ...defaultPreferences },

      setBudget: (budget) =>
        set((state) => ({
          preferences: { ...state.preferences, budget },
        })),

      setCalorieTarget: (target) =>
        set((state) => ({
          preferences: { ...state.preferences, calorie_target: target },
        })),

      toggleNutrient: (tag) =>
        set((state) => {
          const nutrients = state.preferences.nutrients.includes(tag)
            ? state.preferences.nutrients.filter((t) => t !== tag)
            : [...state.preferences.nutrients, tag];
          return { preferences: { ...state.preferences, nutrients } };
        }),

      toggleTasteLike: (tag) =>
        set((state) => {
          const taste_like = state.preferences.taste_like.includes(tag)
            ? state.preferences.taste_like.filter((t) => t !== tag)
            : [...state.preferences.taste_like, tag];
          return { preferences: { ...state.preferences, taste_like } };
        }),

      toggleTasteExclude: (tag) =>
        set((state) => {
          const taste_exclude = state.preferences.taste_exclude.includes(tag)
            ? state.preferences.taste_exclude.filter((t) => t !== tag)
            : [...state.preferences.taste_exclude, tag];
          return { preferences: { ...state.preferences, taste_exclude } };
        }),

      setMealType: (type) =>
        set((state) => ({
          preferences: { ...state.preferences, meal_type: type },
        })),

      setLocation: (lat, lng) =>
        set((state) => ({
          preferences: {
            ...state.preferences,
            latitude: lat,
            longitude: lng,
          },
        })),

      resetPreferences: () =>
        set({ preferences: { ...defaultPreferences } }),
    }),
    {
      name: "todaybite-preferences",
    }
  )
);

// ========== 推荐结果 Store ==========

interface RecommendState {
  plans: MealPlan[];
  loading: boolean;
  error: string | null;
  message: string;
  setResult: (result: RecommendResponse) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearResult: () => void;
}

export const useRecommendStore = create<RecommendState>((set) => ({
  plans: [],
  loading: false,
  error: null,
  message: "",

  setResult: (result) =>
    set({
      plans: result.plans,
      message: result.message,
      loading: false,
      error: null,
    }),

  setLoading: (loading) => set({ loading, error: null }),

  setError: (error) => set({ error, loading: false }),

  clearResult: () =>
    set({ plans: [], message: "", error: null }),
}));
