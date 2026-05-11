import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="grid min-h-screen place-items-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-850 px-6 py-12 text-slate-100">
      <section className="mx-auto flex w-full max-w-4xl flex-col gap-10 rounded-3xl border border-slate-800 bg-slate-900/80 p-10 shadow-2xl shadow-slate-950/40 backdrop-blur-xl">
        <div className="space-y-6">
          <span className="inline-flex rounded-full bg-brand/10 px-4 py-2 text-sm font-semibold uppercase tracking-[0.32em] text-brand">
            Etkinlik Planlayıcı
          </span>
          <h1 className="text-5xl font-black tracking-tight sm:text-6xl">
            Kendi etkinlik takviminizi hızla yönetin.
          </h1>
          <p className="max-w-3xl text-lg leading-8 text-slate-400">
            Randevularınızı, tercihlerinizle uyumlu önerileri ve kayıtlı etkinliklerinizi tek bir noktadan takip edin.
            Hızlı giriş yapın veya yeni kullanıcı olarak hemen başlayın.
          </p>
        </div>

        <div className="flex flex-col gap-4 sm:flex-row">
          <Link href="/login">
            <Button className="min-w-[160px]">Giriş Yap</Button>
          </Link>
          <Link href="/register">
            <Button className="min-w-[160px] bg-white text-slate-900 hover:bg-slate-100 text-brand">
              Kayıt Ol
            </Button>
          </Link>
        </div>
      </section>
    </main>
  );
}
