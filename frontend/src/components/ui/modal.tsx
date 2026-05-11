import { ReactNode } from "react";

export function Modal({ children }: { children: ReactNode }) {
  return <div className="rounded-lg border border-line bg-white p-4 shadow-xl">{children}</div>;
}
