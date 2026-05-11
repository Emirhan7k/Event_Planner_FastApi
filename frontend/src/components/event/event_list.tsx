import { EventCard } from "@/components/event/event_card";
import { events } from "@/lib/constants";

export function EventList() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}
