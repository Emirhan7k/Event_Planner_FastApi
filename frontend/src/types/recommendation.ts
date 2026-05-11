import { EventItem } from "@/types/event";

export type Recommendation = {
  event: EventItem;
  score: number;
  reason: string;
};
