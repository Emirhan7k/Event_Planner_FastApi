import { Database, RefreshCw, Settings, Users } from "lucide-react";

import { InterestTags } from "@/components/ai/interest_tags";
import { Card } from "@/components/ui/card";
import { DashboardLayout } from "@/components/layout/dashboard_layout";

export default function PreferencesPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-black">Yapay Zeka Onerilerini Kisellestir</h1>
        <div className="mt-5 grid gap-5 lg:grid-cols-2">
          <Card className="p-5">
            <h2 className="text-lg font-black">Ilgi Alanlarim</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="rounded-md bg-emerald-100 px-3 py-2 text-sm font-semibold text-emerald-800">Teknoloji (Yuksek Agirlik)</span>
              <span className="rounded-md bg-red-100 px-3 py-2 text-sm font-semibold text-red-800">Sanat (Dusuk Agirlik)</span>
              <span className="rounded-md bg-amber-100 px-3 py-2 text-sm font-semibold text-amber-800">Girisimcilik (Orta Agirlik)</span>
            </div>
            <h2 className="mt-8 text-lg font-black">Anahtar Kelimeler</h2>
            <div className="mt-3"><InterestTags /></div>
          </Card>
          <Card className="p-5">
            <h2 className="text-lg font-black">Sistem Nasil Calisir?</h2>
            <div className="mt-8 grid place-items-center">
              <div className="relative grid h-72 w-72 place-items-center rounded-full border-4 border-blue-200">
                <div className="text-center text-xl font-black">AI<br />Algoritmasi</div>
                <Users className="absolute left-1 top-28 h-9 w-9 text-blue-600" />
                <RefreshCw className="absolute right-3 top-12 h-9 w-9 text-blue-600" />
                <Database className="absolute bottom-3 h-9 w-9 text-blue-600" />
                <Settings className="absolute top-3 h-9 w-9 text-blue-600" />
              </div>
            </div>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
