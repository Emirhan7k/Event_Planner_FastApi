import { CalendarDays, Compass, Settings, Star } from "lucide-react";
import Link from "next/link";

const items = [
  { href: "/explore", label: "Kesfet", icon: Compass },
  { href: "/calendar", label: "Akilli Takvim", icon: CalendarDays },
  { href: "/saved", label: "Kaydedilenler", icon: Star },
  { href: "/preferences", label: "Tercihlerim", icon: Settings }
];

export function Sidebar() {
  return (
    <aside className="hidden w-56 shrink-0 border-r border-line bg-white p-4 md:block">
      <Link href="/dashboard" className="mb-8 block text-3xl font-black tracking-normal">
        <span className="text-blue-600">A</span><span className="text-emerald-500">I</span>
      </Link>
      <nav className="space-y-2">
        {items.map((item) => (
          <Link key={item.href} href={item.href} className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-semibold text-zinc-700 hover:bg-blue-50 hover:text-blue-700">
            <item.icon className="h-5 w-5" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
