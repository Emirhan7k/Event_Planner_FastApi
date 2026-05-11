import { Bell, Search } from "lucide-react";

import { Input } from "@/components/ui/input";

export function Navbar() {
  return (
    <header className="flex h-16 items-center gap-4 border-b border-line bg-white px-5">
      <div className="relative max-w-2xl flex-1">
        <Search className="absolute left-3 top-2.5 h-5 w-5 text-zinc-400" />
        <Input className="w-full pl-10" placeholder="Bu hafta sonu teknik yeteneklerimi gelistirebilecegim etkinlikler bul" />
      </div>
      <button className="relative rounded-md p-2 hover:bg-panel" aria-label="Bildirimler">
        <Bell className="h-5 w-5" />
        <span className="absolute right-1 top-0 grid h-5 w-5 place-items-center rounded-full bg-rose-500 text-xs font-bold text-white">3</span>
      </button>
      <div className="flex items-center gap-2 text-sm font-semibold">
        <span className="grid h-9 w-9 place-items-center rounded-full bg-zinc-200">AY</span>
        Ali Yilmaz
      </div>
    </header>
  );
}
