---
name: flutter-color-port
description: Port-time color governance for taking a Flutter/Figma (Vlad) screen to React on Signal DS. Use whenever porting or auditing a Flutter widget/screen to React and you hit a color — every legacy Flutter color maps by ROLE to the UNIVERSAL Signal DS palette (DS-012/DS-022 — same palette on every surface, no per-specialty/per-module color), bound to a semantic TOKEN, never to white and never to a raw hex. Auto-fires on "port this Flutter screen", "convert the .dart", "why is this grey/white", "map the colors", "match Flutter parity". Owns ONE thing: Flutter color → Signal DS token at port time. The governing model lives upstream (DESIGN-STATE DS-NNN + tokens); this is the port slice of it, not the authority.
---

# flutter-color-port

**The one rule:** porting Flutter → React does **not** mean stripping color to white. Vlad's
Flutter/Figma design encoded *semantic* color. Those exact hexes are rejected (WCAG/brand), but their
**meaning** is preserved — every one maps by **role** to the universal Signal DS palette, bound to a
semantic **token**. **Map the color; never drop it, never hardcode the hex.**

> Why this skill exists: ports kept rendering monochrome because the engineer/agent applied the
> color *prohibitions* (no purple/orange, no per-module color, no raw hex) without applying the color
> *governance*. Calm neutral base + mapped semantic color = the product Vlad designed. (Samer, 2026-06-11.)

## This is the PORT SLICE, not the authority (read first — prevents drift)

The **single source of truth for color** is upstream, and it wins over this file if they ever disagree:

- **Values:** `scrips-signal-ds/tokens/design-tokens.ts` → `@scripsteam/scrips-signal-ds/tokens.css`.
- **Rules (the governing decisions):** `DESIGN-STATE.md` — **DS-012, DS-015, DS-016, DS-018, DS-021, DS-022** (+ DS-013). `CHANGELOG.md` is the dated record.
- **Exact rejected-hex find-targets:** `REJECTED_COLORS` in `design-tokens.ts`. Grep it for the Flutter value you found; never copy a rejected hex into new code/docs (the DS color gate blocks it — raw hex doesn't cascade when a token moves, which is how blue drifted).

**Before quoting any value or rule here, confirm it against the above** (source-of-truth discipline).
This table is convenience; the tokens + DS-NNN are law. If this file lags a new DS-NNN, fix it.

## The governing model (DS-012 / DS-022) — ONE universal palette, every surface

All domains and specialties — Scheduling, Patients, Billing, Clinical, Admin, every specialty —
consume the **same** palette. **No surface gets its own color family; they differ by icon + label,
never by hue.** Color is **not** limited to 3–4 and is **not** specialty-scoped. The full families:

| Family | Token(s) | When (role) |
|---|---|---|
| **Brand — action** | `--color-brand-primary` (blue/500 `#005FD4`) | buttons, links, interactive, active nav |
| **Brand — depth** | `--color-brand-depth` (blue/700 `#004795`) | titles, payer/patient-name emphasis |
| **Status — success** | `--color-status-success` (green/500 `#41AE55`) | paid · fulfilled · checked-in · active |
| **Status — error** | `--color-status-error` (red/500 `#CD3232`) | cancelled · failed · destructive · **allergy alert** |
| **Status — warning** | `--color-status-warning` (yellow/500 `#E5A000`) | **out-of-range vital** · overdue · pending · patient flag |
| **Neutral (slate ramp)** | `--color-text-*` / `--color-surface-*` / `--color-border-default` | text, surfaces, borders, muted/booked/disabled |
| **Teal — chrome (DS-018)** | `colors.teal[500]` = `#007A85` (TS import — **no CSS var**, see gap note) | **non-clinical CHROME ONLY**: info accents, role-identity tags, badge counters, system banners. **NEVER status/severity. NEVER module theming** (DS-022). |
| **Teal/300 — AI provenance (DS-021)** | `colors.teal[300]` = `#67C2C7` | **reserved exclusively** for the AI-authored-content provenance stripe (+ Orb glyph). Nothing else. |
| **Okabe-Ito categorical (DS-018)** | `chart.{blue,orange,bluishGreen,…}` (TS import — **no CSS var**) | **data-viz ONLY** (chart fills, multi-series, cohorts). NOT body text, NOT status. |
| **Surface navy** | `--color-surface-sidebar` (`#0D1B4B`) | app-bar / side-nav background |
| **Disabled** | `--color-interactive-disabled` (grey/400 `#CED7DB`) | disabled controls · pending · waitlist |

**No purple, no orange as semantic** (DS-018 — neither has a CVD-safe AA-passing variant distinct from
blue/red). **Switch ON = green** (DS-016). **Clinical severity L0–L4** (DS-013) is a *clinical-surface-only*
pilot scale — don't apply it to scheduling/billing.

> **Token-layer gap (verified 2026-06-11):** the brand/status/neutral/surface families ARE emitted as
> `--color-*` CSS vars in `tokens.css` — use `var(--color-*)` on CSS-Module surfaces. But the **teal ramp
> (DS-018) and Okabe-Ito `chart` palette (DS-018) live ONLY in `design-tokens.ts`** (`colors.teal`, `chart`)
> — they are **not** plumbed to CSS vars. On a CSS-Module surface you must `import { colors, chart } from
> '@scripsteam/scrips-signal-ds/tokens'` and inline the value, OR flag it: the CSS-var plumbing for teal +
> chart is a DS gap to close (file it; don't freelance a `--color-teal-*` that doesn't exist).

## Legacy Flutter/Vlad hex → token (port-time lookup, BY ROLE)

Replace by role; bind to the token. The same legacy teal maps to **different** targets by role —
classify first.

| Flutter/Vlad source (rejected) | Common alias | Role in the Flutter screen | → token |
|---|---|---|---|
| teal | `enabledBtnBGColor`, `primary` | a primary **action** (button/link) | `--color-brand-primary` |
| teal | accent / tag / badge / info chrome | non-clinical **chrome** | `--color-teal-500` (DS-018) |
| old deep blue | `appBarColor`, title | emphasis / title | `--color-brand-depth` |
| salmon | error/cancel | error/destructive | `--color-status-error` |
| lime / checked-in green | success | success/paid | `--color-status-success` |
| bright yellow / orange | warning/pending | warning/attention | `--color-status-warning` |
| lavender grey | label/hint, "Booked" | muted text / neutral | `--color-text-muted` |
| disabled grey | disabled | disabled/pending | `--color-interactive-disabled` |
| app background | scaffold bg | page bg | `--color-surface-background` (cool-slate, not white) |
| card / white | card | surface | `--color-surface-card` |
| input border | border | border/divider | `--color-border-default` |
| sidebar navy | nav bg | app-bar / side-nav | `--color-surface-sidebar` (`#0D1B4B`) |

(Exact rejected hex values for the grep: see `REJECTED_COLORS` in `design-tokens.ts`.)

## Status — 7 Flutter status colors collapse to 5 (DS-023 maps appt status)

`StatusChip`, text-only (no leading dot/glyph — color carries it):

| Flutter status color | → Signal status | Used for |
|---|---|---|
| green | `success` | Fulfilled · Checked-in · Paid · Active · Submitted |
| red | `error` | Cancelled · No-show · Payment failed · Claim rejected |
| orange **→ merges into** yellow | `warning` | Out-of-range vital · Overdue · Drug interaction · Flag |
| blue | `info` (`brand.primary`) | In session · Arrived · Processing · In-flight |
| light blue **→** blue/300 | soft-info | Proposed · Draft · Pending review |
| grey | `neutral` | Booked · Archived · Inactive |
| disabled grey | `disabled` | Pending · Waitlist · Awaiting approval |

## Procedure (during a Flutter → React port)

1. **Grep the `.dart` for color.** `Color(0xFF…)`, theme aliases (`enabledBtnBGColor`, `appBarColor`), `colors.*`. List every distinct color the widget uses.
2. **Classify by ROLE, not hue** — action / status / chrome / data-viz / surface / border / muted / disabled. Role picks the token (the same legacy teal → blue if action, teal/500 if chrome).
3. **Bind to the token** — `var(--color-*)` (CSS) or `semantic.*` (TS import from `@scripsteam/scrips-signal-ds/tokens`). **Zero raw hex in new React.**
4. **Universal palette** — never give this specialty/module its own color (DS-012/022). Differ by icon + label.
5. **Clinical color is meaning** — allergies → error, out-of-range vital → warning; never color a chronic-problem chip the same as an allergy. Severity must be scannable. Teal is chrome, never severity.
6. **Verify gate-clean** — `grep` the diff for `#` in color positions → none; no rejected hex; no per-module color.
7. **No role match? Don't invent** — flag to the DS owner; it may need a new semantic token (ADR), not a freelanced hex.

## Boundaries (MECE)

- **This skill owns:** Flutter color → Signal DS token at port time.
- **`flutter-parity`** owns the compose-vs-port register; **`flutter-to-react`** owns the full port pre-flight + parity audit + verification (both invoke this at the color step).
- **`claude-design-master-brief`** carries the *design-time* slice of the SAME governance (so Claude Design designs in-palette and the coding agent ports in-palette — one model, two consumers).
- **`scrips-signal-ds` (tokens + DESIGN-STATE DS-NNN + CHANGELOG)** is the authority. Disagreement → token/DS wins; fix this file.

**Origin:** 2026-06-11 — Samer: the Flutter→Signal color map must be a skill the whole team uses on every port. Corrected same day after Samer caught that the 2026-05-15 6-row map was a stale subset (teal → blue) — DS-018 (teal ramp), DS-012/DS-022 (universal palette, no per-specialty color), DS-021 (provenance teal) govern, and this skill must defer to them.
