"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuthStore } from "@/store/auth_store";
import { getCurrentUser } from "@/services/user_service";

export function AuthLoader({ children }: { children: ReactNode }) {
  const setToken = useAuthStore((state) => state.setToken);
  const setUser = useAuthStore((state) => state.setUser);
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const router = useRouter();

  useEffect(() => {
    const token = window.localStorage.getItem("event_planner_token");
    if (!token) {
      return;
    }

    setToken(token);
    getCurrentUser()
      .then((user) => setUser(user))
      .catch(() => {
        clearAuth();
        window.localStorage.removeItem("event_planner_token");
        router.push("/login");
      });
  }, [clearAuth, router, setToken, setUser]);

  return <>{children}</>;
}
