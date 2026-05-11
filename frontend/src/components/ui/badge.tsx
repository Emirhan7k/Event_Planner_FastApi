import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export function Badge({ className, ...props }: HTMLAttributes<HTMLSpanElement>) {
  return <span className={cn("inline-flex rounded-md bg-emerald-100 px-2 py-1 text-xs font-bold uppercase text-emerald-700", className)} {...props} />;
}
