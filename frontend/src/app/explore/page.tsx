import { EventCard } from "@/components/event/event_card";
import { DashboardLayout } from "@/components/layout/dashboard_layout";
import { events } from "@/lib/constants";

export default function ExplorePage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-black">Etkinlik Kesfet</h1>
        <div className="mt-5 grid gap-5 lg:grid-cols-2">
          {events.map((event) => <EventCard key={event.id} event={event} large />)}
        </div>
      </div>
    </DashboardLayout>
  );
}
