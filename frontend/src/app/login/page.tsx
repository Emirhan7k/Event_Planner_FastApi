"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { login } from "@/services/auth_service";
import { getCurrentUser } from "@/services/user_service";
import { useAuthStore } from "@/store/auth_store";

export default function LoginPage() {
  const router = useRouter();
  const setToken = useAuthStore((state) => state.setToken);
  const setUser = useAuthStore((state) => state.setUser);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    const formData = new FormData(event.currentTarget);
    const email = String(formData.get("email") ?? "").trim();
    const password = String(formData.get("password") ?? "");

    if (!email || !password) {
      setError("E-posta ve şifre gerekli.");
      return;
    }

    setLoading(true);
    try {
      const response = await login(email, password);
      setToken(response.access_token);
      window.localStorage.setItem("event_planner_token", response.access_token);
      const user = await getCurrentUser();
      setUser(user);
      router.push("/dashboard");
    } catch (error) {
      setError("Giriş yapılamadı. E-posta veya şifre hatalı olabilir.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 px-6 py-12 text-slate-100">
      <Card className="w-full max-w-md space-y-6 border border-slate-800 bg-slate-900 p-8 shadow-xl shadow-slate-950/20">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand">Hoş geldiniz</p>
          <h1 className="mt-4 text-4xl font-extrabold">Hesabınıza giriş yapın</h1>
          <p className="mt-2 text-sm text-slate-400">Etkinliklerinizi yönetmek için e-posta ve şifrenizle giriş yapın.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input name="email" placeholder="E-posta" type="email" autoComplete="email" />
          <Input name="password" placeholder="Şifre" type="password" autoComplete="current-password" />
          {error ? <p className="text-sm font-semibold text-rose-500">{error}</p> : null}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Bekleyin..." : "Giriş Yap"}
          </Button>
        </form>

        <p className="text-center text-sm text-slate-400">
          Hesabın yok mu?{' '}
          <Link href="/register" className="font-semibold text-brand hover:underline">
            Kayıt ol
          </Link>
        </p>
      </Card>
    </main>
  );
}
