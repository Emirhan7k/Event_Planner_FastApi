import { api } from "@/services/api";

export function login(email: string, password: string) {
  return api<{ access_token: string; user_name: string }>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export function register(name: string, email: string, password: string) {
  return api<{ access_token: string; user_name: string }>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password })
  });
}
