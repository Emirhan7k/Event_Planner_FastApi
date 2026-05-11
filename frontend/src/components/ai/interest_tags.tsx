const tags = ["Teknoloji verisi", "Girisimcilik", "Veri Bilimi", "Sanat", "Makine Ogrenmesi", "AI"];

export function InterestTags() {
  return (
    <div className="flex flex-wrap gap-2">
      {tags.map((tag) => (
        <span key={tag} className="rounded-md border border-line px-3 py-1 text-sm">
          {tag}
        </span>
      ))}
    </div>
  );
}
