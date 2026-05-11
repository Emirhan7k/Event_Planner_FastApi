import { api } from "@/services/api";
import { User } from "@/types/auth";

export function getCurrentUser() {
  return api<User>("/api/users/me");
}
