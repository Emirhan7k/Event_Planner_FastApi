export function MatchScore({ score }: { score: number }) {
  return (
    <div className="grid h-28 w-28 place-items-center rounded-full border-[10px] border-coral bg-white text-center">
      <div>
        <div className="text-2xl font-black">%{score}</div>
        <div className="text-sm">Eslesme</div>
      </div>
    </div>
  );
}
