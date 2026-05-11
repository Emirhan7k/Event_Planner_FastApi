import { ConflictAlert } from "@/components/calendar/conflict_alert";

export function ScheduleCard() {
  return (
    <div className="absolute left-[28%] top-[30%] w-72 rounded-md border-l-4 border-red-500 bg-blue-50 p-3 shadow">
      <h3 className="font-bold">Yazilim Mimari Atolyesi</h3>
      <ConflictAlert />
    </div>
  );
}
