import { api } from "@/services/api";

export function getCalendar() {
  return api<{ events: unknown[] }>("/api/calendar");
}
