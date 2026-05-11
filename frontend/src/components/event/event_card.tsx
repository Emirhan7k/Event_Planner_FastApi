import { Bell, CalendarPlus, Clock, MapPin, ThumbsDown } from "lucide-react";
import Image from "next/image";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { RecommendationBadge } from "@/components/event/recommendation_badge";
import { EventItem } from "@/types/event";

export function EventCard({ event, large = false }: { event: EventItem; large?: boolean }) {
  return (
    <Card className={large ? "grid gap-4 p-4 lg:grid-cols-[1fr_190px]" : "overflow-hidden p-2"}>
      <div>
        <div className="relative aspect-[16/9] overflow-hidden rounded-md">
          <Image src={event.image} alt="" fill className="object-cover" sizes={large ? "640px" : "300px"} />
          <div className="absolute left-3 top-3">
            <RecommendationBadge category={event.category} />
          </div>
        </div>
        <h3 className={large ? "mt-4 text-3xl font-black" : "mt-3 line-clamp-2 text-sm font-black"}>{event.title}</h3>
        <div className="mt-3 flex flex-wrap gap-4 text-zinc-600">
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />{event.date}, {event.time}</span>
          <span className="flex items-center gap-1"><MapPin className="h-4 w-4" />{event.location}</span>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          <Button>Hemen LCV (Katil)</Button>
          <Button className="border-zinc-400 bg-white text-ink hover:bg-panel"><CalendarPlus className="h-5 w-5" />Takvime Ekle</Button>
        </div>
        <div className="mt-4 flex gap-5 border-t border-line pt-3 text-zinc-600">
          <button className="flex items-center gap-2"><ThumbsDown className="h-5 w-5" />Begenmedim</button>
          <button className="flex items-center gap-2"><Bell className="h-5 w-5" />Daha Sonra Hatirlat</button>
        </div>
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
