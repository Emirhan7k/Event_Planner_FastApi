import { CalendarView } from "@/components/calendar/calendar_view";
import { DashboardLayout } from "@/components/layout/dashboard_layout";

export default function CalendarPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-black">Akilli Takvim</h1>
        <div className="mt-5"><CalendarView /></div>
      </div>
    </DashboardLayout>
  );
}
