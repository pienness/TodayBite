import type { UserPreferences, RecommendResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export async function fetchRecommendations(
  preferences: UserPreferences
): Promise<RecommendResponse> {
  const response = await fetch(`${API_BASE}/api/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(preferences),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`推荐请求失败: ${error}`);
  }

  return response.json();
}
