"use client";

import { MoodSelector } from "@/components/ai/mood_selector";
import { EventList } from "@/components/event/event_list";
import { useAuthStore } from "@/store/auth_store";

export function RecommendationFeed() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-black">
        Hoş geldin{user ? `, ${user.name}` : ", keşifçimiz"}! <br />
        Senin için seçtiklerimiz.
      </h1>
      <p className="mt-4 max-w-3xl text-base text-slate-600">
        İlgi alanlarına uygun etkinlik önerileri, kayıtlı tercihlerin ve yaklaşan takvimine göre hazırlandı.
      </p>
      <h2 className="mt-8 text-lg font-black">Bugün Hangi Moddasın?</h2>
      <div className="mt-3"><MoodSelector /></div>
      <h2 className="mt-8 text-lg font-black">Sana Özel Öneriler</h2>
      <div className="mt-3"><EventList /></div>
    </div>
  );
}
