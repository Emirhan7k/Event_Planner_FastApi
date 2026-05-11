import { create } from "zustand";

import { events } from "@/lib/constants";
import { EventItem } from "@/types/event";

type EventState = {
  events: EventItem[];
};

export const useEventStore = create<EventState>(() => ({ events }));
