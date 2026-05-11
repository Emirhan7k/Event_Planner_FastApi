import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen place-items-center p-6">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-3xl font-black">Giris Yap</h1>
        <div className="mt-6 space-y-3">
          <Input placeholder="E-posta" />
          <Input placeholder="Sifre" type="password" />
          <Button className="w-full">Giris Yap</Button>
        </div>
        <Link href="/register" className="mt-4 block text-sm font-semibold text-brand">Hesap olustur</Link>
      </Card>
    </main>
  );
}
