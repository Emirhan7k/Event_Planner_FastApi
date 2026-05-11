"use client";

import { Bell, CalendarPlus, Clock, MapPin, ThumbsDown } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { RecommendationBadge } from "@/components/event/recommendation_badge";
import { EventItem } from "@/types/event";

export function EventCard({ event, large = false }: { event: EventItem; large?: boolean }) {
  const router = useRouter();
  const [status, setStatus] = useState<"idle" | "joined" | "calendar" | "reminder" | "hidden">("idle");
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  return (
    <Card className={large ? "grid gap-4 p-4 lg:grid-cols-[1fr_190px]" : "overflow-hidden p-2"}>
      <div>
        <button
          type="button"
          className="relative block aspect-[16/9] w-full overflow-hidden rounded-md text-left"
          onClick={() => (large ? setIsDetailOpen(true) : router.push(`/event/${event.id}`))}
          aria-label={`${event.title} detayini ac`}
        >
          <Image src={event.image} alt="" fill className="object-cover" sizes={large ? "640px" : "300px"} />
          <div className="absolute left-3 top-3">
            <RecommendationBadge category={event.category} />
          </div>
        </button>
        <button
          type="button"
          className={large ? "mt-4 block text-left text-3xl font-black hover:text-blue-700" : "mt-3 block text-left text-sm font-black hover:text-blue-700"}
          onClick={() => (large ? setIsDetailOpen(true) : router.push(`/event/${event.id}`))}
        >
          <span className={large ? "" : "line-clamp-2"}>{event.title}</span>
        </button>
        <div className="mt-3 flex flex-wrap gap-4 text-zinc-600">
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />{event.date}, {event.time}</span>
          <span className="flex items-center gap-1"><MapPin className="h-4 w-4" />{event.location}</span>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          <Button onClick={() => setStatus("joined")}>{status === "joined" ? "LCV Alindi" : "Hemen LCV (Katil)"}</Button>
          <Button onClick={() => setStatus("calendar")} className="border-zinc-400 bg-white text-ink hover:bg-panel"><CalendarPlus className="h-5 w-5" />{status === "calendar" ? "Takvime Eklendi" : "Takvime Ekle"}</Button>
        </div>
        <div className="mt-4 flex gap-5 border-t border-line pt-3 text-zinc-600">
          <button type="button" onClick={() => setStatus("hidden")} className="flex items-center gap-2 hover:text-rose-600"><ThumbsDown className="h-5 w-5" />{status === "hidden" ? "Gizlendi" : "Begenmedim"}</button>
          <button type="button" onClick={() => setStatus("reminder")} className="flex items-center gap-2 hover:text-blue-700"><Bell className="h-5 w-5" />{status === "reminder" ? "Hatirlatici Kuruldu" : "Daha Sonra Hatirlat"}</button>
        </div>
        {status !== "idle" ? <p className="mt-3 text-sm font-semibold text-emerald-700">Islem guncellendi.</p> : null}
        {isDetailOpen ? (
          <div className="fixed inset-0 z-30 grid place-items-center bg-zinc-950/40 p-4" role="dialog" aria-modal="true">
            <div className="w-full max-w-lg rounded-lg bg-white p-5 shadow-2xl">
              <h2 className="text-xl font-black">{event.title}</h2>
              <p className="mt-3 leading-6 text-zinc-700">{event.description}</p>
              <div className="mt-5 flex justify-end">
                <Button onClick={() => setIsDetailOpen(false)}>Kapat</Button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
      {large ? (
        <aside className="flex flex-col items-center justify-center gap-4">
          <div className="grid h-32 w-32 place-items-center rounded-full border-[12px] border-coral text-center">
            <div><div className="text-3xl font-black">%{event.matchScore}</div><div>Eslesme</div></div>
          </div>
          <p className="rounded-md bg-zinc-900 p-4 text-sm leading-6 text-white shadow-lg">{event.description}</p>
        </aside>
      ) : null}
    </Card>
  );
}
