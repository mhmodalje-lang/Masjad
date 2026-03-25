import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        arabic: ["Amiri", "Noto Naskh Arabic", "serif"],
        sans: ["Inter", "Lexend", "IBM Plex Sans Arabic", "sans-serif"],
        display: ["Lexend", "Inter", "sans-serif"],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        islamic: {
          green: "hsl(var(--islamic-green))",
          "green-foreground": "hsl(var(--islamic-green-foreground))",
          gold: "hsl(var(--islamic-gold))",
          "gold-foreground": "hsl(var(--islamic-gold-foreground))",
          navy: "hsl(var(--islamic-navy))",
          "navy-foreground": "hsl(var(--islamic-navy-foreground))",
          teal: "hsl(var(--islamic-teal))",
          "teal-light": "hsl(var(--islamic-teal-light))",
          purple: "hsl(var(--islamic-purple))",
          "purple-light": "hsl(var(--islamic-purple-light))",
          emerald: "hsl(var(--islamic-emerald))",
          "emerald-glow": "hsl(var(--islamic-emerald-glow))",
          rose: "hsl(var(--islamic-rose))",
          copper: "hsl(var(--islamic-copper))",
        },
        mystic: {
          pearl: "hsl(var(--mystic-pearl))",
          mint: "hsl(var(--mystic-mint))",
          moss: "hsl(var(--mystic-moss))",
          amber: "hsl(var(--mystic-amber))",
          mist: "hsl(var(--mystic-mist))",
          glow: "hsl(var(--mystic-glow))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "pulse-glow": {
          "0%, 100%": { opacity: "1", boxShadow: "0 0 20px -4px hsl(var(--islamic-green) / 0.15)" },
          "50%": { opacity: "0.92", boxShadow: "0 0 40px -4px hsl(var(--islamic-green) / 0.3)" },
        },
        "spin-slow": {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(360deg)" },
        },
        "heroZoom": {
          "0%": { transform: "scale(1.08)", opacity: "0.9" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
        "confetti-fall": {
          "0%": { transform: "translateY(-20px) rotate(0deg)", opacity: "1" },
          "100%": { transform: "translateY(100vh) rotate(720deg)", opacity: "0" },
        },
        "mystic-float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-6px)" },
        },
        "mystic-glow-ring": {
          "0%, 100%": { boxShadow: "0 0 0 0 hsl(var(--islamic-green) / 0)" },
          "50%": { boxShadow: "0 0 0 8px hsl(var(--islamic-green) / 0.08)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-glow": "pulse-glow 0.5s ease-out forwards",
        "spin-slow": "spin-slow 8s linear infinite",
        "heroZoom": "heroZoom 2s ease-out forwards",
        "confetti-fall": "confetti-fall 3s ease-in forwards",
        "mystic-float": "mystic-float 4s ease-in-out infinite",
        "glow-ring": "mystic-glow-ring 3s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
