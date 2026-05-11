"use client";

import { Bell, Search, LogOut } from "lucide-react";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { Input } from "@/components/ui/input";
import { NotificationDropdown } from "@/components/notifications/notification_dropdown";
import { useAuthStore } from "@/store/auth_store";

export function Navbar() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [query, setQuery] = useState("");

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const search = query.trim();

    if (search.length > 0) {
      router.push(`/explore?q=${encodeURIComponent(search)}`);
    }
  }

  function handleLogout() {
    window.localStorage.removeItem("event_planner_token");
    clearAuth();
    router.push("/login");
  }

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((segment) => segment[0])
        .slice(0, 2)
        .join("")
        .toUpperCase()
    : "AP";

  return (
    <header className="flex h-16 items-center gap-4 border-b border-line bg-white px-5">
      <form onSubmit={handleSearch} className="relative max-w-2xl flex-1">
        <Search className="absolute left-3 top-2.5 h-5 w-5 text-zinc-400" />
        <Input
          className="w-full pl-10"
          placeholder="Bu hafta sonu teknik yeteneklerimi gelistirebilecegim etkinlikler bul"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </form>
      <div className="relative">
        <button
          type="button"
          className="relative rounded-md p-2 hover:bg-panel"
          aria-label="Bildirimler"
          aria-expanded={isNotificationsOpen}
          onClick={() => setIsNotificationsOpen((isOpen) => !isOpen)}
        >
          <Bell className="h-5 w-5" />
          <span className="absolute right-1 top-0 grid h-5 w-5 place-items-center rounded-full bg-rose-500 text-xs font-bold text-white">3</span>
        </button>
        {isNotificationsOpen ? (
          <div className="absolute right-0 top-12 z-20 w-64">
            <NotificationDropdown />
          </div>
        ) : null}
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-3 rounded-full border border-slate-200 bg-slate-100 px-3 py-2">
          <span className="grid h-9 w-9 place-items-center rounded-full bg-slate-800 text-sm font-bold text-white">{initials}</span>
          <div className="hidden sm:block">
            <p className="text-sm font-semibold text-slate-900">{user?.name ?? "Misafir"}</p>
            <p className="text-xs text-slate-500">{user?.email ?? "Giriş yapılmadı"}</p>
          </div>
        </div>
        <button
          type="button"
          className="rounded-full p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
          onClick={handleLogout}
          aria-label="Çıkış yap"
        >
          <LogOut className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
