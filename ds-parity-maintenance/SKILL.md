---
name: ds-parity-maintenance
description: Daily Figma↔code design-parity maintenance for the Signal DS. Runs the headless parity engine, reports the asymmetry + day-over-day delta, alarms on regressions (anchor lost / ungoverned component), and drives the unanchored backlog 78→0. Weekly (Mon) adds a live-Figma bridge reconcile + team digest. Use on the daily schedule, on-demand ("parity check", "design asymmetry", "what's the graduation backlog"), or before/after graduating a component.
---

# ds-parity-maintenance

**Goal it serves:** keep the Figma↔code design asymmetry measured, owned, and shrinking —
never silently regrowing. Closure = unanchored count trends to 0 on a tracked cadence.

Owns the *coverage parity* axis (which components are graduated to Figma). Sister skills:
`signal-system-sweep` (token/decision consistency, event-driven), `weekly-signal-diff`
(shipped-vs-pending), `design-to-dev-pipeline` + `signal-ds-graduation` (the graduation act),
`figma-doc-sync`. Do not duplicate their scope.

## The engine (deterministic, headless, branch-safe)

```
python3 ~/.claude/hooks/lib/ds-parity-audit.py
```

- Reads `scrips-signal-ds/tokens/design-map.json` **from `origin/main`** (never the working
  tree — immune to the stale-branch trap, 2026-06-06).
- Emits JSON: total / anchored / unanchored, by status·scope·category, `locked_no_frame`
  (priority-1), ranked `top10`, full `unanchored_list`, and a `delta` vs the last snapshot.
- Writes a dated snapshot to `~/.claude/state/ds-parity-<date>.json` for day-over-day trend.

## Drift classes it surfaces

1. **locked-without-frame** — committed contract shipping in code with NO Figma frame. Sharpest asymmetry → top priority.
2. **code-without-frame** — the full unanchored set (the 78). Burndown target.
3. **newly-unanchored (REGRESSION)** — an anchor went null OR a new ungoverned component appeared since yesterday. **Alarm — call out loudly.**
4. **newly-resolved (PROGRESS)** — graduated/anchored since yesterday. Celebrate + confirm.
5. **retroactive-anchored** — frame exists but marked "RETROACTIVE / requires design review" (code-side sees the registry marker; the Figma-description marker is caught in the weekly bridge pass).

## Daily run (scheduled ~04:45, before Samer's 5:30 start)

1. Run the engine. Parse JSON.
2. Compose a tight report (HTML per output-format if saved to artifacts; Slack mrkdwn for the DM):
   - headline: `anchored/total · unanchored N (Δ vs yesterday)`
   - **regressions first** (newly-unanchored) — if any, this is the lede.
   - progress (newly-resolved).
   - priority-1 list (locked-without-frame) + next-up top10.
3. **DM Samer** (Slack user `UANT64XRQ` per `feedback_n8n_slack_user_id` / CoS workspace) — daily, regardless. Verify any number against the engine JSON before sending (source-of-truth gate).
4. Append a one-line entry to `~/claude-os/daily-activity-log.md` with `[SCHEDULED]`.

## Weekly run (Mondays — adds the live-Figma reconcile + team digest)

5. If the Figma desktop bridge is connected (`figma_get_status` probe), run the live reconcile:
   - For each anchored component, confirm its `figmaNodeId` still resolves (`figma_search_components`); flag stale anchors.
   - Scan for Figma frames whose description contains "RETROACTIVE" → list as design-review debt.
   - If the bridge is NOT open, note "live-Figma reconcile skipped (bridge offline)" — do not fake it (verification gate).
6. Post a consolidated **weekly digest to #current-active-team-scrips (`C052WJ0NL1J`)**, @-mentioning Andrew + Tariq: current asymmetry, week's burndown (Δ), top priority-1 items, any stale anchors / retroactive debt. This is the team's shared truth.

## Burndown discipline

- The ranked `unanchored_list` IS the graduation queue. Order: locked → experimental → planned; cross-module before domain.
- Graduating a component is **interactive design work** → route through `design-to-dev-pipeline`
  (Claude Design → React/Storybook → Figma) + `signal-ds-graduation`. Never hand-build the frame.
- After a graduation lands, the next daily run shows it under `newly_resolved` and the count drops — that's the closed-loop confirmation.
- Track the burndown in the Jira epic (see activity log 2026-06-06 for the epic key).

## Guardrails

- **Numbers come from the engine JSON only** — never eyeball the registry (source-of-truth gate).
- **Don't auto-graduate / auto-edit Figma** — surface + route to the interactive pipeline.
- **Regression (newly-unanchored) is the signal that matters most** — it means the asymmetry is
  regrowing (someone shipped a component without graduating it). Lead the report with it.
