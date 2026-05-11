import "@/styles/globals.css";
import type { Metadata } from "next";

import { AuthLoader } from "@/components/auth/auth_loader";

export const metadata: Metadata = {
  title: "AI Event Planner",
  description: "AI destekli etkinlik planlama ve oneriler"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="tr">
      <body>
        <AuthLoader>{children}</AuthLoader>
      </body>
    </html>
  );
}
