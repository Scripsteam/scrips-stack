---
name: flutter-parity
description: Produce a Flutter→React port parity register for a module — what to COMPOSE from graduated Signal DS, what's already DONE in the React target, and what's a genuine PORT gap. Use before porting a module so you build the gaps and compose the rest, instead of re-porting components that already exist. Grounded in real files only — never guess.
---

# /flutter-parity — module parity register (compose vs port)

Most of the Scrips UI is already graduated into Signal DS. Porting blind re-builds
things that exist. This skill produces a grounded register so a dev knows, per
unit: **compose it (it's graduated), it's done (already in React), or port it
(genuine gap).**

## Hard rule — grounded only, no guessing

Every row cites a real file or a real export. If you can't cite it, it doesn't go
in the register. This skill exists precisely because the failure mode is confident
wrong answers from narrow searches (see the canonical source map in
`scrips-stack/CLAUDE.md`). State search scope; never write "missing" without
having checked the authority.

## Inputs

- A Flutter module path (e.g. `scrips_msp1_flutter_shared/.../features/settings_module`
  and/or `scrips_msp1_pa/lib/features/settings`).
- The React target repo (e.g. `scrips-practitioner-react`).

## Method

1. **Enumerate the Flutter surface units.** List the real widget files in the
   module: `find <module> -name "*widget*.dart" -o -name "*screen*.dart" -o -name "*page*.dart"`.
   Each is a candidate unit. Note the obvious leaf widgets vs screens.
2. **For each unit, check the authority in order:**
   a. **Graduated in Signal DS?** Grep the package exports
      (`node_modules/@scripsteam/scrips-signal-ds/dist/index.d.ts`) and
      `scrips-signal-ds/coverage-matrix.md` for a matching component. If yes →
      **COMPOSE** (name the exact export).
   b. **Already built in the React target?** Grep the target repo's `src/`. If
      yes → **DONE** (cite the file).
   c. **Neither** → **PORT** (genuine gap). This is where the read-the-`.dart` →
      Signal-DS-atoms → component + story → screenshot loop applies.
3. **Emit the register** (table below). Order: PORT gaps first (the actual work),
   then COMPOSE, then DONE.
4. **Sanity line:** count units, and state what you did NOT check (scope honesty).

## Output format

```
# <Module> — Flutter→React parity (<date>)
Source: <flutter module path>  ·  Target: <react repo>

| Flutter unit (file) | Status | Action |
|---|---|---|
| allergies_list_widget.dart | COMPOSE | import `AllergiesChartTab` (graduated) |
| <leaf>.dart | PORT | gap — read .dart → Signal DS atoms → component + story |
| <x>.dart | DONE | already at src/.../x.tsx |

Coverage: N units — P port / C compose / D done. Not checked: <e.g. sub-widgets under X>.
```

## When NOT to use

If the module is tiny (1–2 widgets), just check Signal DS inline — don't ceremony
it. This earns its keep on module-sized surfaces (settings, encounter, scheduling).
