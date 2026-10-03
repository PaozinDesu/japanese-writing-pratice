# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Kaku** — a platform for practicing Japanese writing and reading (hiragana, katakana and the 2,136 Jōyō kanji), Portuguese-speaking author, UI in pt-BR. The repo is a monorepo with **no root `package.json`** — two independent npm projects, each run from its own directory:

- `www/` — Next.js frontend.
- `server/` — Express backend.
- `docs/handoff/kaku-handoff/` — the full design handoff package (see **Design source of truth** below). This is the spec; nothing here should be invented from scratch.

**Current state:** `www/` has the full Kaku product — all ~10 screens from the handoff, wired to real (client-side) data and business logic, following the MVVM structure below. `server/` is still an untouched scaffold:

- `server/src` only has `app.ts` (health check + 404/error handlers) and `index.ts` (listens on `PORT` or 3333) — no `config/`, `controllers/`, `services/`, `repositories/`, etc. yet, and no database. `www/` does **not** talk to it: auth, lists, practice/reading history and stats all live client-side in `localStorage`, ported from the prototype's `source/js/*.js` (see **Design source of truth**) — this was a deliberate scoping decision, not an oversight. Wiring a real backend (auth, persistence, sync across devices) is future work; when it happens, only `www/src/models/{auth,user-data,lists,practice-session}.model.ts` should need to change shape (swap the `localStorage`-backed calls for `fetch`s), everything above them (view-models, views) should be unaffected.
- `www/` builds real functionality into the layered structure below — don't add new scaffolding patterns; follow what's already there (e.g. `www/src/views/caracteres/` or `www/src/view-models/use-praticar-view-model.ts`) as the reference for a new screen.

## Commands

```bash
# www/ (frontend)
npm run dev     # next dev
npm run build   # next build
npm run start   # next start
npm run lint    # eslint (flat config, eslint.config.mjs)

# server/ (backend)
npm run dev       # tsx watch src/index.ts
npm run build     # tsc -> dist/
npm run start     # node dist/index.js
npm run typecheck # tsc --noEmit
```

Run these from inside `www/` or `server/` respectively — there is no root script that runs both. No test framework is configured in either project.

## Stack

**`www/`**
- Next.js 16 (App Router, `src/app/`) with React 19 and TypeScript (strict)
- Tailwind CSS v4 via `@tailwindcss/postcss` — configured in CSS (`@import "tailwindcss"` and `@theme inline` in `src/app/globals.css`), no `tailwind.config` file. Every color/spacing/font token used by the design system (see below) is declared there as a CSS variable, aliased 1:1 to the handoff's `tailwind.config.js` names (`background`, `surface`, `primary`, `text-primary`, `hiragana`/`katakana`/`kanji`, etc.) — this is intentional so `design-system/components.ts`'s class strings can be copied over near-verbatim.
- `class-variance-authority` + `clsx` for the component variant system, ported from the handoff's `design-system/components.ts` into `src/components/ui/variants.ts`
- `lucide-react` for icons (see [[design-system]] — it's the only icon source allowed)
- Path alias `@/*` maps to `www/src/` (e.g. `@/models/...`, `@/components/...`)
- Fonts: `Zen Kaku Gothic New` (`--font-sans`), `Shippori Mincho` (`--font-serif`), `Klee One` (`--font-jp`, Japanese characters and the handwriting-recognition glyph rendering) via `next/font/google`, set up in `src/app/layout.tsx`
- Light-only theming (the handoff has no dark palette) via CSS variables in `globals.css`; see [[design-system]] for the full token list
- The character database (`docs/handoff/kaku-handoff/source/data/out/kaku-caracteres.json`, ~5.5 MB) is copied to `public/data/kaku-caracteres.json` and fetched once client-side via `models/characters.model.ts#loadCharacters()` — it's too large to bundle into JS. Re-copy it if the handoff's data ever regenerates.
- Stroke-order animations come from [animCJK](https://github.com/parsimonhi/animCJK) (Copyright FM-SH), not from the handoff. `public/stroke-svgs/{codePoint}.svg` holds one SVG per character actually used by the site (~2,300 files, fetched on demand, never bundled — see `models/stroke-svg.model.ts`); `scripts/fetch-stroke-svgs.mjs` (re-runnable) sparse-clones animCJK and copies only the needed files plus its license texts into `public/stroke-svgs/LICENSES/`. Kanji SVGs (`svgsJa/`) are Arphic Public License; kana SVGs (`svgsJaKana/`) are LGPL — both notices ship in that folder. Never pull from `svgsZh*`/`svgsKo*`/`Special`/`Zoo` — different stroke conventions or non-Japanese licensing.

**`server/`**
- Express 5, TypeScript (strict, `commonjs`, target `ES2022`)
- `tsx watch` for dev, plain `tsc` build to `dist/`
- No ORM/database wired up yet — `models/`/`repositories/` in the structure below are for when one is added

Next.js 16, React 19 and Express 5 differ from older major versions; check `node_modules/*/dist` or official docs rather than relying on older API knowledge.

## Architecture

Both projects have mandatory layered structures, enforced by rule files under `.claude/rules/` (path-scoped, auto-applied when editing matching files):

- **`www/` — MVVM.** `app/` (routing only) → `view-models/` (`use{Name}ViewModel` hooks, state/logic) → `models/` (types, business logic ported from the prototype's `source/js/*.js`, `localStorage` access) and `views/` (presentational components, props only) → `components/` (generic reusable UI). Full rule, naming and dependency direction: `@./rules/frontend-structure.md`
- **`server/` — layered backend.** `routes/` → `controllers/` → `services/` → `repositories/`; `config/`, `middlewares/`, `utils/` alongside. Controllers never touch the database directly. Full rule: `@./rules/backend-structure.md`. Still empty — see **Current state**.
- **DTOs**, in either project (`*.dto.ts`): naming (`{Action}{Scope}DTO`), no constructor, static `create()` factory, params typed via `I{Action}{Scope}DTOParams`. Full rule: `@./rules/create-dto.md`. `www/` mostly doesn't need these yet — there's no request/response boundary while everything is `localStorage`-backed.

`www/src/models/` today: `characters.{model,type}.ts` (the character database), `auth.model.ts`, `user-data.model.ts`, `lists.model.ts`, `practice-session.model.ts`, `stats.model.ts`, `reading.model.ts`, `recognition.model.ts` (canvas stroke drawing + chamfer-distance recognition, client-only), `stroke-svg.model.ts` (fetches/prepares the animCJK stroke-order SVGs — see **Design source of truth**), `local-store.model.ts` (the shared `localStorage` wrapper), `intent.model.ts` (cross-screen "practice this character" handoff). One `use{Screen}ViewModel` per route in `view-models/`; one `views/<route>/` folder per route, with `<sub-state>-view.tsx` files for a screen's internal states (e.g. `views/praticar/{setup,session,summary}-view.tsx`) rather than separate routes — this mirrors the prototype's own `view: "setup" | "session" | "summary"` state machines.

## Design source of truth

The design lives **in the repo**, at `docs/handoff/kaku-handoff/` (untracked as of this writing — `git add` it along with any commit that references it). It is a full handoff package generated from a 24-frame design canvas (10 desktop screens 1920×1080, 12 mobile screens 390×844, 2 Design System boards). Read `docs/handoff/kaku-handoff/README.md` first; it indexes everything below.

- **`design-system/`** — the visual source of truth, built entirely on **Tailwind CSS v3.4** defaults (no arbitrary hex, no `mt-[13px]`-style values):
  - `tailwind.config.js` — semantic aliases (`primary`, `secondary`, `accent`, `surface`, `background`, `text-*`, status colors), fonts, radii, shadows, breakpoints.
  - `components.ts` — every component's variants via **class-variance-authority** (button, input, select, card, modal, badge, tabs, navbar, table, etc.).
  - `tokens.json` — the same tokens as plain JSON.
  - `LEIAME.md` — full rationale: 60/30/10 color rule, spacing hierarchy, type roles, states, accessibility.
  - Palette: background `stone-100`, surfaces white with `stone-200/300` borders, text `stone-900/700/600`, accent `red-600` (CTAs/links/active states only). Fonts: `Zen Kaku Gothic New` (UI), `Shippori Mincho` (display titles), `Klee One` (Japanese characters and handwriting recognition strokes).
  - `www/`'s `globals.css` already carries this exact palette and these fonts as CSS variables (see **Stack** above) — the [[design-system]] rule (60/30/10 via CSS variables, no arbitrary Tailwind values, `lucide-react`-only icons) and this handoff are kept in sync; update both together if either changes.
- **`screenshots/`** — PNG captures of every screen (`desktop/visitante`, `desktop/logado`, `mobile/visitante`, `mobile/logado`) plus interaction-only states under `estados/` (writing session/feedback/summary, reading question/feedback/result, login/signup validation, user menu). Use as the visual gabarito.
- **`screens-static/`** — same folder structure, one rendered `.html` per screen with inline styles and **no script** (the drawing `<canvas>` is a placeholder). Open directly in a browser to inspect exact structure/spacing/`aria-*`. This is the implementation spec — e.g. "implement `screens-static/mobile/logado/Progresso.html` as a React component with the design-system classes." Desktop frames are drawn at 1440×810 and scaled ×1.333 to fit 1920×1080 canvases; implement at the real 1440 width (`max-w-7xl`), without the scale transform.
- **`source/`** — everything that generated the prototype:
  - `project/` — the 24 canvas frames (`.dc.html`) + `data/kaku-data.js`.
  - `js/` — the prototype's business logic, portable as reference for the real implementation: `account.js` (auth/session/lists/history/stats, `computeStats`, `PERIODS`), `rec.js` (stroke recognition — chamfer-distance score, `OK = 0.6`, `ID_MIN = 0.33` — and reading validation `readingOk`/`canonRo`, accepts romaji or kana, any registered on/kun reading), `practice.js` (writing session flow), `reading.js` (reading quiz flow, `readingOrder`).
  - `data/out/` — the generated character database: `kaku-caracteres.json` (or per-category `hiragana.json`/`katakana.json`/`kanji.json`), `schema.json`, `LEIAME.md`. This is the real data source for the app — don't hand-roll character data.
  - `tools/` — the Playwright script that generated `screenshots/` and `screens-static/`.
- **Known limitations, carried over from the prototype** (per the handoff's README §6) — don't silently replicate these in the real product without flagging it:
  - Auth is prototype-only (`localStorage`, client-side PBKDF2 hash) — needs a real backend/session in `server/`.
  - Stroke recognition compares shape only, not stroke order/direction, calibrated on few examples — manual correction UI is expected to stay.
  - Character data (meanings, examples, history) was assembled manually and needs review by a fluent speaker before production; ~1,451 N2/N1 kanji have only a minimal entry.
  - The handoff's own `strokeOrder` field (real vector paths for only ~30 characters) is **not** what the app uses for animation anymore — that's been superseded by the animCJK integration above, which covers essentially the whole current character set (single-character match or a two-character combination like きゃ). The `strokeOrder` field may still be present in the JSON but nothing reads it; don't resurrect it as a data source without checking `models/stroke-svg.model.ts` first.

**Never build a screen, component or flow that has no counterpart in `docs/handoff/kaku-handoff/`.** If something is requested that isn't there yet, ask before inventing layout, copy or visual design — the handoff (or a rule under `.claude/rules/`) is the spec, not a starting point to riff on.

**Responsive strategy (deliberate deviation from the handoff's file layout):** the handoff ships each screen as two separate frames (desktop `screens-static/desktop/…` and mobile `…Mobile.html`). The real app does **not** mirror that as two component trees — each route in `www/src/app/` is a single responsive React tree (mobile-first Tailwind classes, `lg:`/`xl:` overrides for the desktop layout), reading both frame variants as the two ends of one breakpoint range. `components/layout/header.tsx` is the clearest example: a `hidden md:flex` desktop navbar and a `md:hidden` mobile top bar + fixed bottom nav live in the same component. Keep new screens consistent with this — don't fork a screen into `*-mobile.tsx`/`*-desktop.tsx` components.

**Routes implemented** (`www/src/app/`): `/` (Main), `/login`, `/cadastro`, `/caracteres` + `/caracteres/[id]` (kana vs. kanji detail chosen by `category`, not two routes), `/praticar` and `/leitura` (the handoff's Escrita/Leitura tab pair — `components/layout/practice-mode-tabs.tsx`), `/progresso`, `/listas`, `/perfil`. `/progresso`, `/listas` and `/perfil` require login and render a "entrar" empty state otherwise, matching the prototype's `guest`/`logged` branching.

## Language

UI copy and user-facing error messages are **pt-BR** (matches the handoff, which is entirely in Portuguese). Identifiers — files, variables, types, props, route segments — stay in English. Don't translate identifiers, don't write English copy into a screen.
