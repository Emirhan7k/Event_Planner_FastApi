import { ReactNode } from "react";

import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";

export function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <main className="mx-auto my-8 flex min-h-[780px] w-[min(1180px,calc(100%-32px))] overflow-hidden rounded-lg border border-line bg-white shadow-2xl">
      <Sidebar />
      <section className="min-w-0 flex-1">
        <Navbar />
        {children}
      </section>
    </main>
  );
}
