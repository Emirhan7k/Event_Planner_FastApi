import { AlertTriangle } from "lucide-react";

export function ConflictAlert() {
  return <p className="mt-2 flex items-center gap-2 text-sm font-semibold text-red-600"><AlertTriangle className="h-4 w-4" />Cakisma Riski: Baska bir ilgi alaninla cakisiyor!</p>;
}
