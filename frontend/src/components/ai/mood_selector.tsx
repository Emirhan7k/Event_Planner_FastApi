const moods = ["Akademik Ag Kurma", "Odaklanmis Calisma", "Sosyal & Rahat", "Ilham AI"];

export function MoodSelector() {
  return (
    <div className="flex flex-wrap gap-3">
      {moods.map((mood, index) => (
        <button key={mood} className={`rounded-md border px-4 py-2 text-sm font-semibold ${index === 0 ? "border-brand bg-blue-50 text-blue-800" : "border-line bg-white"}`}>
          {mood}
        </button>
      ))}
    </div>
  );
}
