import { events } from "@/lib/constants";

export function useRecommendations() {
  return events.map((event) => ({ event, score: event.matchScore, reason: event.description }));
}
