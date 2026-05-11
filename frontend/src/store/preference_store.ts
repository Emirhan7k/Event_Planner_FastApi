import { create } from "zustand";

type PreferenceState = {
  interests: Record<string, number>;
};

export const usePreferenceStore = create<PreferenceState>(() => ({
  interests: { Teknoloji: 0.9, Sanat: 0.3, Girisimcilik: 0.6 }
}));
