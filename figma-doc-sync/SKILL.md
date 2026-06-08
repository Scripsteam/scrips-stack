---
name: figma-doc-sync
description: "Keep Figma in sync with locked design decisions and design-map.json. Use when a new decision is added to DESIGN-STATE.md LOCKED, a new component is added to design-map.json, or a graduated component needs to land in the Figma library (bidirectional Figma ↔ design docs sync, part of the design-to-dev-pipeline graduation chain)."
type: procedure
---

# Design Sync — Figma Documentation

Keeps Figma in sync with locked design decisions. Run this whenever:
- A new decision is added to DESIGN-STATE.md LOCKED section
- A new component is added to design-map.json
- Figma components are renamed or reorganised
- Tokens in design-tokens.ts change

This is the workflow that replaces needing a designer to document in Figma.

## Prerequisites

Figma Desktop Bridge must be open:
1. Open Figma Desktop
2. Plugins → Development → Figma Desktop Bridge → Run
3. Call `figma_get_status` with `probe: true` — must return success before proceeding

If not connected, stop and tell Samer to open Desktop Bridge. Do not proceed blind.

## Source files (always read these first)

```bash
# Pull latest from scrips-signal-ds
gh api repos/Scripsteam/scrips-signal-ds/contents/DESIGN-STATE.md \
  --jq '.content' | base64 -d > /tmp/DESIGN-STATE.md

gh api repos/Scripsteam/scrips-signal-ds/contents/tokens/design-map.json \
  --jq '.content' | base64 -d > /tmp/design-map.json
```

Or read locally if the repo is cloned:
- DESIGN-STATE.md — what is locked, what each decision number is
- tokens/design-map.json — every component's figmaNodeId and import path
- tokens/design-tokens.ts — canonical token values

## Step 1 — Check Figma connection

Call `figma_get_status` with `probe: true`.

- If success → proceed
- If fail → stop. Tell Samer: "Open Desktop Bridge in Figma (Plugins → Development → Figma Desktop Bridge), then run this again."

## Step 2 — Sync component descriptions

For every component in design-map.json that has a `figmaNodeId`, call `figma_set_description`:

**Description format:**
```
[Signal DS — locked 2026-04-04]
Hierarchy: {level} (DS-002)
Color: Blue Depth system (DS-001)
Storybook: {storybookId}
Code: scrips-react/{import}
Source of truth: github.com/Scripsteam/scrips-signal-ds
```

Components with confirmed figmaNodeIds (from design-map.json):
- Button → nodeId: 617:2693 → level: Component
- Other components: use `figma_search_components` to find by name, then set description

**Search pattern for components without a nodeId:**
```
figma_search_components(query: "ComponentName")
→ get nodeId from result
→ figma_set_description(nodeId, description)
→ update design-map.json with confirmed nodeId
```

## Step 3 — Verify tokens against Figma variables

Call `figma_get_variables` with `format: "summary"` to get variable list.

Compare against `tokens/design-tokens.ts`:
- blue/500 should be `#0076F8`
- blue/700 should be `#004795`
- blue/900 should be `#0D1B4B`
- green/500 should be `#41AE55`
- red/500 (error) should be `#CD3232`

If any mismatch: call `figma_batch_update_variables` to correct.
If variables don't exist in Figma yet: note as a gap, do not create — variable creation is a manual Figma step.

## Step 4 — Add decision annotations to key frames

For each locked component that has a Figma frame, call `figma_set_annotations`:

```
annotations: [
  {
    label: "DS-001 Blue Depth",
    labelMarkdown: "**Locked 2026-04-04** · Blue Depth color system · [DESIGN-STATE.md](https://github.com/Scripsteam/scrips-signal-ds/blob/main/DESIGN-STATE.md#ds-001)"
  },
  {
    label: "DS-002 Hierarchy",
    labelMarkdown: "**Component level** · Part of: Grid→Atom→**Component**→Card→Block→Template→Frame→Layout"
  }
]
```

## Step 5 — Commit updated design-map.json

If any new nodeIds were discovered in Step 2, update design-map.json:

```bash
cd /tmp/scrips-signal-ds  # or local clone
# Update design-map.json with confirmed nodeIds
git add tokens/design-map.json
git commit -m "sync(figma): confirm nodeIds for {ComponentName(s)} — {date}"
git push
```

## Step 6 — Smoke test

After syncing, verify at least 3 components in Figma Dev Mode:
1. Open a synced component in Figma Dev Mode
2. Confirm description shows `[Signal DS — locked 2026-04-04]` and correct Storybook ID
3. Confirm annotations show DS-001 and DS-002 references

Report: `FIGMA SYNC | Components updated: N | Tokens verified: N/N | Mismatches: N | Annotations set: N`

## When to run

| Trigger | Action |
|---------|--------|
| New decision added to DESIGN-STATE.md LOCKED | Run full sync |
| New component added to design-map.json | Run Step 2 + 5 for that component only |
| Token value changed in design-tokens.ts | Run Step 3 only |
| "Does Figma match the code?" question | Run Steps 1→3 only (read-only check) |
| Weekly, as part of CoS cadence | Run full sync |
