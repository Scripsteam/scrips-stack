---
name: practitioner-flutter-to-react
description: >
  Per-surface wrapper for porting any Practitioner App (PA) screen from Flutter to React.
  Carries the PA surface specifics (source repos, target repo, Signal DS package + version,
  Storybook, DS consumption rule) and invokes the GENERIC engines — flutter-style-port,
  flutter-parity, design-parity-judge — plus scrips-verify before handback. Use when porting
  any practitioner screen (encounter, today list, patient, calendar) from Flutter to React.
  Do NOT bake practitioner specifics into the generic engines — they live here.
type: procedure
---

# practitioner-flutter-to-react — the PA surface layer over the generic port engines

**Why this skill exists.** The port/parity skills are intentionally GENERIC (one owner each,
per MECE skill ownership): `flutter-style-port` knows *how* to port, `design-parity-judge`
knows *how* to measure a render against a source — neither knows *which* surface. The
surface-specific knowledge (which repos, which DS version, which conventions) belongs in a thin
per-surface wrapper. This is the Practitioner (PA) instance of that pattern. PM and UA own their
own equivalents (`pm-flutter-to-react`, `ua-flutter-to-react`); never clone the engines per surface.

Origin: a ported PA encounter screen drifted from its Flutter source (patient summary on the wrong
side, an impoverished side-rail, no frame) because the agent had a generic engine and a source file
but **no surface layer** telling it "this is the practitioner encounter, here's the contract, here's
the DS version." This skill is that layer.

---

## PA surface facts (verified 2026-06-19 — re-verify before pinning)

| Fact | Value | Source |
|---|---|---|
| Flutter app (source) | `scrips_msp1_pa` | repo map |
| Flutter shared features (source) | `scrips_msp1_flutter_shared` — encounter, etc. live here, NOT in the app repo | verified: `encounter_screen.dart` is under `scrips_shared_features/.../encounter_module/` |
| React app (target) | `scrips-practitioner-react` | repo map |
| Signal DS package | `@scripsteam/scrips-signal-ds` `^1.13.0` | verified 2026-06-19: `scrips-practitioner-react/package.json` (was `^1.11.0` in the original draft — re-verify before pinning, it moves) |
| DS style consumption | Tailwind v4 `@source` the DS dist — NEVER import the bundle `styles.css` (utilities layer collides, zeroes `px-*`) | DS-styles consumption rule |
| Storybook | confirm the port in the target repo (memory: 6006) | UNVERIFIED — check before citing |

Paths are relative to each repo root. On Windows, use the local checkout path (not a mac `/Users/...`
path) and run any bash tooling under WSL or git-bash.

---

## The port protocol (run in order; do not skip)

1. **Anchor on the Flutter source — read it before writing React.** The source app is the layout
   source of truth. State the file path you read.
2. **Extract a STATE TABLE / frame contract first.** For each view-state: region → position → the
   Signal DS component. Discover states from the code (don't assume names). For every row, quote the
   one line of code (file:line) that proves it. List any region with no DS export as a MISSING BLOCK.
   Save it (e.g. `docs/<screen>-frame-contract.md`).
3. **A missing block is the work — build it as a DS block.** Never hand-build a div where a block
   belongs. Stop and report missing bricks; do not improvise the layout around them.
4. **Build to a declarative frame, not hand-wired layout.** Compose named, state-aware slots (per the
   "Frame as Declarative Intent" DS decision). The page fills slots; it positions nothing.
5. **Port visual tokens with `flutter-style-port`** (signal-DS-aware) and **map parity with
   `flutter-parity`** against the Flutter render.
6. **No "done" without `design-parity-judge`.** Run it against BOTH the Flutter source (its G6
   parity-vs-source gate) and the frame contract. "Done" is blocked until the measured gate table
   passes with screenshots of each state.
7. **Before handback / PR, run `scrips-verify`** (integration + security; conditional frontend).

## Hard rules

- **Generic engines, surface inputs.** This wrapper supplies the repos/DS-version/contract; the
  engines do the work. If you find yourself editing `flutter-style-port` or `design-parity-judge` to
  add "practitioner" logic — stop; it belongs here or in the contract.
- **The contract is the per-screen source of truth the agent reads at build time** — not the brain,
  not chat, not a screenshot. If a layout fact only lives in your head, write it into the contract.
- **Fidelity to the Flutter source is the first gate, before any DS knowledge.** A faithful port
  preserves source behavior unless explicitly told otherwise.

## MECE / cross-references

- `flutter-style-port` — the shared visual-token port engine (generic).
- `flutter-parity` — the shared parity-mapping engine (generic).
- `design-parity-judge` — the measured render-vs-source visual gate (generic); G6 = parity-vs-source.
- `scrips-verify` — pre-handback verification (generic).
- `finishing-a-development-branch` — runs `scrips-verify` at Step 1.5.
- Sibling surfaces: `pm-flutter-to-react` (→ `dev-scrips-pm-react`), `ua-flutter-to-react`
  (→ `scrips_msp1_ua`). Same pattern, different surface facts.
