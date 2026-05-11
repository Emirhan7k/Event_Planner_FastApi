import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function RegisterPage() {
  return (
    <main className="grid min-h-screen place-items-center p-6">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-3xl font-black">Kayit Ol</h1>
        <div className="mt-6 space-y-3">
          <Input placeholder="Ad Soyad" />
          <Input placeholder="E-posta" />
          <Input placeholder="Sifre" type="password" />
          <Button className="w-full">Basla</Button>
        </div>
        <Link href="/login" className="mt-4 block text-sm font-semibold text-brand">Zaten hesabim var</Link>
      </Card>
    </main>
  );
}
