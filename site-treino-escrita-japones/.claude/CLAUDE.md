# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`site-treino-escrita-japones` — intended as a Japanese writing practice site (Portuguese-speaking author). Currently it is an unmodified `create-next-app` scaffold: `app/page.tsx` is still the default Next.js starter page and `app/layout.tsx` still has the default "Create Next App" metadata and `lang="en"`. No app-specific logic exists yet.

## Commands

```bash
npm run dev     # dev server at http://localhost:3000
npm run build   # production build
npm run start   # serve production build
npm run lint    # eslint (flat config, eslint.config.mjs)
```

No test framework is configured.

## Stack

- Next.js 16 (App Router, `app/` directory) with React 19 and TypeScript (strict)
- Tailwind CSS v4 via `@tailwindcss/postcss` — configured in CSS (`@import "tailwindcss"` and `@theme inline` in `app/globals.css`), there is no `tailwind.config` file
- Fonts: Geist / Geist Mono loaded through `next/font/google` in `app/layout.tsx`, exposed as `--font-geist-sans` / `--font-geist-mono` CSS variables
- Path alias `@/*` maps to the repo root (e.g. `@/app/...`)
- Light/dark theming is driven by `prefers-color-scheme` via `--background`/`--foreground` variables in `globals.css`

Next.js 16 and React 19 differ from older versions; check `node_modules/next/dist/docs` or the official docs rather than relying on older API knowledge.
