---
name: flutter-style-port
description: Port-time VISUAL-TOKEN governance for taking a Flutter/Figma (Vlad) screen to React on Signal DS — color AND typography/text. Use whenever porting or auditing a Flutter widget/screen to React and you hit a color, a font, a text size/weight, or a title/label alignment. Everything maps by ROLE to the universal Signal DS palette + type system, bound to a semantic TOKEN — never a raw hex, never a one-off font/size, never stripped to white, never a wrapped label. Auto-fires on "port this Flutter screen", "convert the .dart", "why is this grey/white", "map the colors/fonts", "fix the type", "title alignment", "match Flutter parity". Owns ONE thing: Flutter visual style → Signal DS token at port time. The governing model lives upstream (DESIGN-STATE DS-NNN + tokens); this is the port slice of it, not the authority.
---

# flutter-style-port

**The one rule:** porting Flutter → React does **not** mean stripping style to a generic white template.
Vlad's Flutter/Figma design encoded *semantics* — color (teal = action), type (size/weight = hierarchy),
alignment. The exact hexes/fonts are rejected (WCAG/brand), but their **meaning** is preserved — every
one maps by **role** to the universal Signal DS palette + type system, bound to a semantic **token**.
**Map it; never drop it, never hardcode a hex/px, never let a label wrap.**

> Why this skill exists: ports kept looking AI-generated — color stripped to white, fonts/sizes
> freelanced, labels wrapping — because the *prohibitions* were applied without the *mapping*. Calm
> neutral base + mapped semantic color + the locked type scale = the product Vlad designed. (Samer, 2026-06-11.)

## This is the PORT SLICE, not the authority (read first — prevents drift)

The **single source of truth** is upstream and wins over this file:

- **Values:** `scrips-signal-ds/tokens/design-tokens.ts` → `@scripsteam/scrips-signal-ds/tokens.css`.
- **Rules:** `DESIGN-STATE.md` — color = DS-012/015/016/018/021/022; **fonts = DS-017**; type/line-height = the `typography` const (S2/D-001). `CHANGELOG.md` = dated record.
- **Rejected-hex find-targets:** `REJECTED_COLORS` in `design-tokens.ts`. Grep it; never inline a rejected hex (it won't cascade when a token moves — that is how blue drifted).

**Confirm against the above before quoting** (source-of-truth discipline). If this file lags a new DS-NNN, fix it.

---

# PART A · COLOR

## Governing model (DS-012 / DS-022) — ONE universal palette, every surface

All domains/specialties consume the **same** palette. **No surface gets its own color family; they
differ by icon + label, never hue.** Color is **not** limited to 3–4 and is **not** specialty-scoped.

| Family | Token(s) | When (role) |
|---|---|---|
| **Brand — action** | `--color-brand-primary` (blue/500 `#005FD4`) | buttons, links, interactive, active nav |
| **Brand — depth** | `--color-brand-depth` (blue/700 `#004795`) | titles, payer/patient-name emphasis |
| **Status — success** | `--color-status-success` (green/500 `#41AE55`) | paid · fulfilled · checked-in · active |
| **Status — error** | `--color-status-error` (red/500 `#CD3232`) | cancelled · failed · destructive · **allergy alert** |
| **Status — warning** | `--color-status-warning` (yellow/500 `#E5A000`) | **out-of-range vital** · overdue · pending · patient flag |
| **Neutral (slate ramp)** | `--color-text-*` / `--color-surface-*` / `--color-border-default` | text, surfaces, borders, muted/booked/disabled |
| **Teal — chrome (DS-018)** | `colors.teal[500]` = `#007A85` (TS import — **no CSS var yet**) | **non-clinical CHROME ONLY**: info accents, role-identity tags, badge counters, banners. **NEVER status/severity. NEVER module theming** (DS-022). |
| **Teal/300 — AI provenance (DS-021)** | `colors.teal[300]` = `#67C2C7` | **reserved exclusively** for the AI-provenance stripe (+ Orb glyph). |
| **Okabe-Ito categorical (DS-018)** | `chart.{blue,orange,bluishGreen,…}` (TS import — **no CSS var yet**) | **data-viz ONLY** (chart fills, multi-series, cohorts). NOT body text, NOT status. |
| **Surface navy** | `--color-surface-sidebar` (`#0D1B4B`) | app-bar / side-nav background |
| **Disabled** | `--color-interactive-disabled` (grey/400 `#CED7DB`) | disabled controls · pending · waitlist |

**No purple, no orange as semantic** (DS-018). **Switch ON = green** (DS-016). **Clinical severity L0–L4**
(DS-013) = clinical surfaces only.

> **Token-layer gap (2026-06-11):** brand/status/neutral/surface ARE `--color-*` CSS vars — use `var(--color-*)`.
> Teal + Okabe-Ito are **TS-only** (`colors.teal`, `chart`) — `import { colors, chart } from '@scripsteam/scrips-signal-ds/tokens'`, or flag the CSS-var plumbing as a DS gap; never freelance a `--color-teal-*` that doesn't exist.

## Legacy Flutter color → token (BY ROLE)

The same legacy teal maps to **different** targets by role — classify first.

| Flutter/Vlad (rejected) | alias | role in screen | → token |
|---|---|---|---|
| teal | `enabledBtnBGColor`, `primary` | a primary **action** | `--color-brand-primary` |
| teal | tag/badge/info chrome | non-clinical **chrome** | `colors.teal[500]` (DS-018) |
| old deep blue | `appBarColor`, title | emphasis/title | `--color-brand-depth` |
| salmon | error/cancel | error | `--color-status-error` |
| lime / checked-in | success | success | `--color-status-success` |
| bright yellow/orange | warning | warning | `--color-status-warning` |
| lavender grey | label/hint, Booked | muted | `--color-text-muted` |
| disabled grey | disabled | disabled | `--color-interactive-disabled` |
| app bg | scaffold | page bg | `--color-surface-background` |
| card/white | card | surface | `--color-surface-card` |
| input border | border | border | `--color-border-default` |
| sidebar navy | nav | app-bar/side-nav | `--color-surface-sidebar` |

(Exact rejected hexes for the grep: `REJECTED_COLORS` in `design-tokens.ts`.) Status: 7 Flutter colors collapse to 5 (`success/error/warning/info/neutral`) via `StatusChip`, text-only.

---

# PART B · TYPOGRAPHY & TEXT

## Fonts (DS-017, locked 2026-05-16) — map, never pick a new one

| Script | Font | Use |
|---|---|---|
| Latin | **Inter Variable** | all UI text |
| Arabic / RTL | **Readex Pro Variable** | Arabic content (+ `dir="rtl"` + logical properties) |
| Mono | **JetBrains Mono Variable** | codes, MRN, IDs, numeric tabular |

Self-hosted: `https://signal-ds.vercel.app/fonts/scrips-fonts.css` (DS-017 single import point). Tokens:
`typography.fontFamily` (`sans`=Inter, `mono`=JetBrains). **A Flutter screen's font → map to these by
script.** Never introduce a Flutter/system font into the port.

## Type scale — snap to the tokens, never freelance a px

Tokens (CSS vars, emitted): `--text-xs · --text-sm · --text-md · --text-lg · --text-base`, each with a paired
`--text-*--line-height` companion (**1.4 body / 1.25 headings**, S2/D-001). Scale = **11 / 13 / 16 / 18 / 24**.

| Role | size | token | note |
|---|---|---|---|
| label / whisper | 11–13 | `--text-xs` / `--text-sm` | muted color, uppercase optional |
| body | 16 | `--text-md` | default reading |
| value / lead | 18–24 | `--text-lg` / display | **value leads, label whispers** — the hierarchy |

Map every Flutter `TextStyle.fontSize` to the nearest scale token by ROLE — **never bind an arbitrary px**.
Weights: Inter Variable — regular (400) body, **500/600 for value/emphasis**; don't bold everything (no hierarchy = an AI tell).

## Text-intent color

`--color-text-primary` (#151B20, value/lead) · `secondary` · `muted` (#809099, label/hint) · `hint` · `inverse` (on dark).
Pair size + color: lead = primary + 18–24; label = muted + 11–13.

## Text & alignment rules (craft — checked on every text element)

- **Label containment (pill/badge/chip/button/tag):** the label is **ONE line, never wraps, never clips.**
  The control **hugs its content** (intrinsic width + padding); never a fixed/narrow box that forces a break.
  Tight space → shorten/abbreviate or use an icon. Budget extra width for `uppercase`+`letter-spacing`.
  (Recurring AI tell — an "IN PROGRESS" badge breaking to two lines. Codified in master-brief §6 + the closing gate.)
- **Alignment:** left-align body + titles (LTR) / right-align (RTL Arabic via Readex + `dir="rtl"`). **Never
  center long text or form labels** (centering everything is an AI tell). Use **optical** alignment, not just mathematical.
- **Letter-spacing:** tight on large display values (`-0.01…-0.03em`); slight positive on small uppercase labels.
- **Hierarchy by type, not decoration:** establish rank with size/weight/color, not boxes or color blocks.
- **RTL:** Arabic strings → Readex Pro, `dir="rtl"`, CSS logical properties (`margin-inline`, `text-align: start`).
- **Truncate, don't reflow, in fixed rows:** ellipsis a too-long value in a fixed-height row (e.g. a vital tile) rather than break layout — but never drop the unit (content-parity).

---

## Procedure (Flutter → React port)

1. **Grep the `.dart`** for color (`Color(0xFF…)`, theme aliases, `colors.*`) AND text (`TextStyle`, `fontSize`, `fontWeight`, `fontFamily`, `textAlign`, `letterSpacing`, `height`). List every distinct style.
2. **Classify by ROLE, not value** — color: action/status/chrome/data-viz/surface/border/muted; type: display/title/body/label/mono. Role picks the token.
3. **Bind to the token** — `var(--color-*)` / `var(--text-*)` (CSS) or `semantic`/`typography`/`colors`/`chart` (TS import). **Zero raw hex, zero arbitrary px, zero new fonts.**
4. **Universal palette + locked type** — no per-specialty color (DS-012/022); no off-scale sizes; Inter/Readex/JetBrains only (DS-017).
5. **Run the text rules** — every label one-line + hugged; no centered long text; RTL handled; value-leads hierarchy.
6. **Verify gate-clean** — `grep` the diff for `#` in color positions and raw `px` font-sizes → none; no rejected hex; no per-module color; no wrapped labels at the real rendered size.
7. **No role match? Don't invent** — flag to the DS owner (may need a new token/ADR), never freelance.

## Boundaries (MECE)

- **This skill owns:** Flutter visual style → Signal DS token at port time (color + typography + text rules).
- **`flutter-parity`** = compose-vs-port register; **`flutter-to-react`** = full port pre-flight + parity audit + verification (both invoke this at the style step).
- **`claude-design-master-brief`** carries the *design-time* slice of the SAME governance (one model, two consumers).
- **`scrips-signal-ds`** (tokens + DESIGN-STATE DS-NNN + CHANGELOG) is the authority. Disagreement → token/DS wins; fix this file.

**Origin:** 2026-06-11 — Samer: the Flutter→Signal mapping must be a team skill used on every port, covering **color AND fonts/text/alignment** in ONE skill (renamed from `flutter-color-port`). Color corrected same day after the 2026-05-15 map proved stale (teal→blue); typography (DS-017) + text/alignment rules added so the whole visual-token port is governed in one place, deferring to the upstream authority.
