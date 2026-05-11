"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { RecommendationFeed } from "@/components/ai/recommendation_feed";
import { DashboardLayout } from "@/components/layout/dashboard_layout";
import { useAuthStore } from "@/store/auth_store";

export default function DashboardPage() {
  const router = useRouter();
  const token = useAuthStore((state) => state.token);
  const user = useAuthStore((state) => state.user);

  useEffect(() => {
    if (typeof window !== "undefined" && !window.localStorage.getItem("event_planner_token")) {
      router.push("/login");
    }
  }, [router]);

  return (
    <DashboardLayout>
      <div className="p-6">
        <section className="mb-6 rounded-3xl bg-gradient-to-r from-sky-600 to-cyan-500 p-8 text-white shadow-lg shadow-slate-800/20">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-100/80">Günaydın</p>
          <h1 className="mt-3 text-4xl font-extrabold">{user ? `${user.name}, Hoş geldin` : "Hoş geldin"}</h1>
          <p className="mt-4 max-w-2xl text-base text-cyan-100/90">
            Etkinlik önerilerin senin ilgi alanlarına göre hazırlandı. Bugünün planı için keşfetmeye devam et.
          </p>
        </section>
        <RecommendationFeed />
      </div>
    </DashboardLayout>
  );
}
