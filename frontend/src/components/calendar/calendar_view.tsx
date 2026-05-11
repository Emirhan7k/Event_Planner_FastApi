import { ScheduleCard } from "@/components/calendar/schedule_card";

export function CalendarView() {
  return (
    <div className="relative h-[560px] overflow-hidden rounded-lg border border-line bg-white">
      <div className="grid grid-cols-[70px_repeat(5,1fr)] border-b border-line text-center text-sm font-bold">
        <span />
        {["Mon", "Tue", "Wed", "Thu", "Fri"].map((day) => <span key={day} className="border-l border-line py-3">{day}</span>)}
      </div>
      <div className="grid h-full grid-cols-[70px_repeat(5,1fr)]">
        <div className="space-y-14 pt-4 text-center text-sm text-zinc-500">{["10:00", "13:00", "15:00", "16:00", "17:00"].map((time) => <div key={time}>{time}</div>)}</div>
        {Array.from({ length: 5 }).map((_, index) => <div key={index} className="border-l border-line bg-[linear-gradient(#e5e7eb_1px,transparent_1px)] bg-[length:100%_72px]" />)}
      </div>
      <ScheduleCard />
    </div>
  );
}
