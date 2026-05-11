import { useEventStore } from "@/store/event_store";

export function useEvents() {
  return useEventStore((state) => state.events);
}
