import { useAuthStore } from "@/store/auth_store";

export function useAuth() {
  return useAuthStore();
}
