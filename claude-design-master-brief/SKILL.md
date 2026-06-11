---
name: claude-design-master-brief
description: "The canonical, paste-ready brief Claude Design works from — bakes the WHOLE Signal DS (tokens, DESIGN-STATE DS-001→036, taxonomy, 88 contracts) + TOPIC v2.0 (PIC product OS) + persona + human-craft + output contract into one standing context. Prepend/attach this to EVERY Claude Design session for the Scrips practitioner/clinical surfaces, so consistency + on-system output is the starting condition, not an after-the-fact correction. Verify token values against scrips-signal-ds/tokens/tokens.css + DESIGN-STATE.md before quoting (this is a synthesis; upstream wins)."
type: reference
---

# Claude Design — Scrips Master Brief (paste this at the start of every design session)

> Origin: Samer 2026-06-10 — *"read the whole Signal DS and TOPIC, bake them into a prompt/template Claude Design works with."* This is that template. Upstream sources (verify before quoting a value): `scrips-signal-ds/tokens/tokens.css`, `DESIGN-STATE.md`, `contracts/*.json`; TOPIC `Scrips Vault/03-knowledge-base/product/topic-v2-product-operating-system.md`.

---

## 0 · The one-paragraph context

You are designing for **Scrips — an AI-native clinical operating system** (cardiometabolic wedge, UAE). Three symbiotic systems: **TOPIC** (what to build / for whom / why), **Signal** (how it looks + behaves — this DS), **Engineering** (the build). **A feature is right only if it passes all three.** Signal **never invents a UI primitive that lacks a TOPIC parent**. The atomic UI unit is **the block**. FHIR R4 is the entity model — clinical data IS a FHIR resource.

## 1 · WHO you design for (TOPIC — People)

- **Primary user: the point-of-care CLINICIAN** — Doctor (full clinical, signs/prescribes) + Nurse (triage/vitals/ROS/PE, no sign/Rx). Time-pressured, high-volume, documents *while* with the patient. **Speed is the metric** (≤12 clicks/visit; fast keyboard entry, never +/- steppers).
- **Device ladder = DS-003 capture rule:** **xs/sm = display + ambient-receive ONLY (no keyboard inputs)** · **md/lg/xl = full capture** (fields, dropdowns). Map sm→display, md→+capture, lg→+review.
- Surfaces: physician mode = **ClinicalDesk**, patient mode = **ClinicalCanvas** (DS-004). Patient app: internal "patient", external "consumer/citizen" (DS-025).
- **Intelligence is part of who we are** — **Orb** (internal name) / **Scrips Intelligence** (user-facing). NBA at point of care. CDS = class-of-action, never a specific prescription/diagnosis. Confidence = **named tier, never %**.

## 2 · The Signal taxonomy + naming law (DS-002, DS-011)

**Hierarchy (closed, no skipping):** `Tokens → Component → Card[xs–xl] → Block → Template → Frame`. Every component declares exactly one level.
- **Clinical surfaces are FHIR-ResourceType-named** — Observation-bound card (vitals/labs), `AllergyChip` (AllergyIntolerance), Condition-bound (Problems), etc. **A vitals card is an Observation-bound `Card`, NOT "VitalCard"** (legacy export = drift). Generic primitives stay generic (`Button`, `Select`, `Input`, `Card`).
- **Block** = 4-zone anatomy anchored to a FHIR ResourceType; **CardInsight** = a *composition pattern* (Orb-in-head + two-CardData juxtaposition + connector glyph), not an atomic type.

## 3 · Tokens — bind to these, NEVER hardcode a hex (DS-001/014/015/034)

**Color authority (single source of truth — this block is a MIRROR, not the law):** values =
`scrips-signal-ds/tokens/tokens.css` (`design-tokens.ts`); rules = `DESIGN-STATE` DS-012/015/016/018/021/022;
provenance = `CHANGELOG`. Verify against them before quoting; if this block lags a DS-NNN, fix it.
**One UNIVERSAL palette on every surface/specialty — no per-module/per-specialty color (DS-012/022);**
surfaces differ by icon + label, never hue. Port-time style mapping (color + type) → the `flutter-style-port` skill.

```
COLOR (semantic — use these, not raw ramps, in components):
  --color-brand-primary #005FD4 (blue/500)   --color-brand-depth #004795 (blue/700)
  --color-interactive-default #005FD4 · hover #004BA5 · active #004795 · disabled #DCE5E9
  --color-status-error #CD3232 / -bg #FFEFEF   --color-status-warning #E5A000 / -bg #FFF6E0
  --color-status-success #41AE55 / -bg #EDF8EF --color-status-info #5A6B75(grey) / -bg #E6F1FE
  --color-text-primary #151B20 · secondary #5A6B75 · muted #809099 · hint #AFBAC0 · inverse #FFF
  --color-surface-background #F7F9FA · card #FFFFFF · sidebar #0D1B4B(navy) · overlay #0F0F0F
  --color-border-default #EFEEEE · subtle #EFF4F6 · strong #CED7DB
  TEAL — chrome ONLY (DS-018): teal/500 #007A85 (info accent, role tag, badge counter, banner) ·
         teal/300 #67C2C7 = AI-provenance stripe ONLY (DS-021). NEVER status/severity, NEVER module theming.
  CHART — Okabe-Ito categorical (DS-018), DATA-VIZ ONLY: chart.{blue,orange,bluishGreen,yellow,skyBlue,vermilion,reddishPurple,black}.
  (teal + chart live in design-tokens.ts as `colors.teal`/`chart` — TS import; not yet emitted as --color-* CSS vars.)
RADIUS  sm 4 · md 8 · lg 12 · xl 16 · full 9999   (default 8px; no over-rounding)
MOTION  micro 80 · fast 150 · normal 250 · slow 400 ms · ease-functional cubic-bezier(.25,.46,.45,.94)
TYPE    scale 11 / 13 / 16 / 18 / 24 (label whispers 11–13, value leads 18–24)
SPACE   4 / 8 / 12 / 16 grid
FONTS   Inter (Latin) · Readex Pro (Arabic) · JetBrains Mono (mono) · Scrips icon font.
        Preview <head>: <link rel="stylesheet" href="https://signal-ds.vercel.app/fonts/scrips-fonts.css">
```
**REJECTED hex (never emit):** `#0076F8` (old primary→#005FD4) · `#007AFF` (iOS) · `#5C41B5`/`#8B5CF6` (purple — no purple as status, DS-018) · `#00B8E3`/`#5FC6D4`/`#1A8F7A` (old teals → `teal/500 #007A85`) · per-module colors.

## 4 · Locked design rules that govern output (DESIGN-STATE)

- **DS-012/022 — No per-module / per-domain color.** Every domain uses the universal palette; modules differ by icon+label+URL only. One visual language.
- **DS-018 — Teal `#007A85` = non-clinical chrome accent ONLY** (info, role tags, provenance) — NEVER a status/severity signal. Okabe-Ito categorical palette = data-viz/multi-series only. **No purple, no orange as semantic.**
- **DS-020 — Lab/vital out-of-range = THREE channels:** status-color tint (yellow/100 mild, red/100 critical) + **direction glyph (↑/↓, ↑↑/↓↓)** + numeric value colored (yellow/700 or red/700). Never color alone (NHS rule).
- **DS-021 — AI-authored content provenance** = teal/300 left stripe + Orb glyph in the gutter.
- **DS-016 — Switch ON = green** (`status-success`); all other binary controls (Checkbox/Radio/Slider/Toggle) on-state = brand-primary.
- **DS-013 — Clinical severity L0–L4** on clinical surfaces only; operational stays binary OK/Error.
- **DS-023 — AppointmentStatusBadge = 6 variants:** In session · Arrived · Completed · No show · Booked · Cancelled.
- **DS-030 — EncounterStep:** Doctor 6 (HPI·Risk·ROS·Documents·A/P·Wrap-up) · Nurse 5 (no A/P).
- **Accessibility (DS-018 methodology):** WCAG 2.2 AA (4.5:1 text), never color alone (pair with glyph/text/position), CVD-safe.

## 5 · Compose, don't invent — the 88-contract inventory

The DS ships **88 component contracts** (`scrips-signal-ds/contracts/*.json`). **Read the relevant contract JSON before designing — compose what exists; do not invent a primitive that already ships.** Clinical/encounter-relevant: `Card`, `ObservationEntryStack`, `AllergyChip`, `Badge`/`StatusBadge`, `Stepper`, `Switch`, `Input`, `FieldShell`/`FieldAndLabel`, `SearchTypeahead`, `TrendIndicator`, `OrganAgeCard`, `ActiveMedicationRow`, `WorkflowStepNode`, the calendar set, the billing/RCM set. New clinical need → file a `contracts/<Name>.json` (hierarchyLevel + fhir.primary + decisionRefs), don't free-style.

## 6 · Human craft — designed by a human, NOT AI (full doc: brain `human-craft-and-behavior-theory.md`)

- **Apple HIG:** Clarity · Deference (chrome recedes, content leads) · Depth (elevation MEANS something — rest = hairline, only the active element lifts = one Signal per view). Optical (not just mathematical) alignment.
- **Behaviour theory:** Hick's (fewer choices) · Fitts's (≥44px reachable targets) · Miller's (chunk) · **Gestalt (group by WHITESPACE + alignment, not boxes-in-boxes)** · Doherty (<400ms feedback) · Aesthetic-Usability (craft = clinical trust).
- **CONSISTENCY IS NON-NEGOTIABLE — checked first.** Never special-case one element's layout (e.g. one card's trend below while others are inline). Uniform structure across a set. **Design against the longest real value by SIZING THE SYSTEM** (card/column width fits BP "142/88 mmHg" inline like every other card), never by special-casing.
- **Never drop data to fit the layout** — the component is **content-adaptive** (reflow/resize), the data stays. Completeness over convenience.
- **Label containment law (pill / badge / chip / button / tag):** the label is **always ONE line — never wraps, never clips.** The control **hugs its content** (intrinsic width + consistent horizontal padding); never put a text-bearing control in a fixed/narrow box that forces a break (`white-space:nowrap` is the floor, not the fix — the box must size to the text). Tight space → **shorten/abbreviate the label or drop to an icon**, never wrap. With `text-transform:uppercase`+`letter-spacing`, budget the extra width. (Recurring AI tell — e.g. an "IN PROGRESS" badge breaking to two lines. Caught 2026-06-11.)
- **Avoid the AI tells:** uniform-everything (no emphasis hierarchy) · reflexive equal card-grid w/ identical drop-shadows · decorative gradients/glassmorphism/emoji-icons/purple-sheen · everything centred · over-rounding · ignored edge/empty/error states · linear/uniform motion.
- Bars to match: Apple HIG · Linear · Vercel · Raycast · Stripe · Better.care. Anti-bar: Epic/Cerner (density without hierarchy, color soup) + generic AI templates.

## 7 · Output contract

- Emit **production `.tsx`** per component importing `@scripsteam/scrips-signal-ds` (ES modules). CSS Modules using `var(--color-*)/var(--radius-*)/var(--motion-*)`. **Zero hardcoded hex.** Storybook-ready (typed props) + Figma-graduation-ready (clean variant axes). Level + FHIR-name every component.
- **Decomposition annotation carries the TOKEN per element** (alongside its DS-level + FHIR ResourceType): e.g. `AllergyChip · component · AllergyIntolerance · --color-status-error`. This is the handoff contract — the coding agent applies the exact token the design used, so color isn't reinvented in the design→dev gap (one continuous color model from Claude Design through the port).
- **No fictional design** (design-judge): every datum maps to a real FHIR field; every action to a real endpoint/event (or a named, committed contract); no faked logic/state. If it must compute/validate/persist → that's a named backend dependency, not a mock.
- **"It rendered" ≠ "it's good."** Judge consistency/rhythm/alignment/hierarchy FIRST, critically, before any positive verdict.

---
**Canonical Figma DS file:** "Scrips Design System" `qrKkhVA3eRXn4hxOlw13pS` (DS-036). **Encounter source:** Encounter 2 `9Gr7nxm67K7msUkxXDKdah` (DS-032). Encounter = submodule of Practitioner App.
