import { Recommendation } from "@/types/recommendation";
import { api } from "@/services/api";

export function getRecommendations() {
  return api<Recommendation[]>("/api/recommendations");
}
