import { MoodSelector } from "@/components/ai/mood_selector";
import { EventList } from "@/components/event/event_list";

export function RecommendationFeed() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-black">Hos Geldin, Ali!<br />Senin Icin Sectiklerimiz.</h1>
      <h2 className="mt-6 text-lg font-black">Bugun Hangi Moddasin?</h2>
      <div className="mt-3"><MoodSelector /></div>
      <h2 className="mt-6 text-lg font-black">Sana Ozel Oneriler</h2>
      <div className="mt-3"><EventList /></div>
    </div>
  );
}
