"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const name = String(formData.get("name") ?? "").trim();
    const email = String(formData.get("email") ?? "").trim();
    const password = String(formData.get("password") ?? "");

    if (!name || !email || !password) {
      setError("Tum alanlari doldurmalisin.");
      return;
    }

    router.push("/dashboard");
  }

  return (
    <main className="grid min-h-screen place-items-center p-6">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-3xl font-black">Kayit Ol</h1>
        <form onSubmit={handleSubmit} className="mt-6 space-y-3">
          <Input name="name" placeholder="Ad Soyad" />
          <Input name="email" placeholder="E-posta" type="email" />
          <Input name="password" placeholder="Sifre" type="password" />
          {error ? <p className="text-sm font-semibold text-rose-600">{error}</p> : null}
          <Button type="submit" className="w-full">Basla</Button>
        </form>
        <Link href="/login" className="mt-4 block text-sm font-semibold text-brand">Zaten hesabim var</Link>
      </Card>
    </main>
  );
}
