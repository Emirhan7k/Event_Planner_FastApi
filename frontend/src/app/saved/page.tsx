import { EventList } from "@/components/event/event_list";
import { DashboardLayout } from "@/components/layout/dashboard_layout";

export default function SavedPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-black">Kaydedilen Etkinlikler</h1>
        <div className="mt-5"><EventList /></div>
      </div>
    </DashboardLayout>
  );
}
