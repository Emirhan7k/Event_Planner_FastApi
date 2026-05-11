import { EventCard } from "@/components/event/event_card";
import { DashboardLayout } from "@/components/layout/dashboard_layout";
import { events } from "@/lib/constants";

export default async function EventDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const event = events.find((item) => item.id === Number(id)) ?? events[0];
  return (
    <DashboardLayout>
      <div className="p-6">
        <EventCard event={event} large />
      </div>
    </DashboardLayout>
  );
}
