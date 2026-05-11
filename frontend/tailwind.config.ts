import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#18181b",
        panel: "#f8fafc",
        line: "#dbe3ef",
        brand: "#2563eb",
        mint: "#16a34a",
        coral: "#f97357"
      }
    }
  },
  plugins: []
};

export default config;
