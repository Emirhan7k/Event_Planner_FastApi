import { EventItem } from "@/types/event";
import { api } from "@/services/api";

export function getEvents() {
  return api<EventItem[]>("/api/events");
}
