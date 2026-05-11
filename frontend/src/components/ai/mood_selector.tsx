"use client";

import { useState } from "react";

const moods = ["Akademik Ag Kurma", "Odaklanmis Calisma", "Sosyal & Rahat", "Ilham AI"];

export function MoodSelector() {
  const [selectedMood, setSelectedMood] = useState(moods[0]);

  return (
    <div>
      <div className="flex flex-wrap gap-3">
      {moods.map((mood, index) => (
        <button
          key={mood}
          type="button"
          onClick={() => setSelectedMood(mood)}
          className={`rounded-md border px-4 py-2 text-sm font-semibold transition hover:border-brand hover:bg-blue-50 ${mood === selectedMood ? "border-brand bg-blue-50 text-blue-800" : "border-line bg-white"}`}
          aria-pressed={mood === selectedMood}
        >
          {mood}
        </button>
      ))}
      </div>
      <p className="mt-3 text-sm font-semibold text-zinc-600">Secili mod: {selectedMood}</p>
    </div>
  );
}
