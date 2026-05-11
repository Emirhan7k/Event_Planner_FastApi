import { Card } from "@/components/ui/card";
import { DashboardLayout } from "@/components/layout/dashboard_layout";

const metrics = [
  ["Kullanici", "128"],
  ["Etkinlik", "42"],
  ["Ortalama Eslesme", "%86"],
  ["LCV", "391"]
];

export default function AdminPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-3xl font-black">Admin Paneli</h1>
        <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {metrics.map(([label, value]) => (
            <Card key={label} className="p-5">
              <p className="text-sm font-semibold text-zinc-500">{label}</p>
              <p className="mt-2 text-3xl font-black">{value}</p>
            </Card>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
