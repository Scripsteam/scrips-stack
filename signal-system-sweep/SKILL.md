---
name: signal-system-sweep
description: Auto-fires on any work touching the four Scrips operating systems — SIGNAL (Design), TOPIC (Product), KERNEL (Engineering), TEMPO (Operations) — plus Storybook, design tokens, ADRs (DS-NNN / BRD-NNN / ADR-NNN), or any constitutional doc per META-SPEC. Runs a system-wide consistency sweep — pulls latest across scrips-signal-ds, signal-portal, scrips-react, the vault (Obsidian), and ~/.claude config; detects drift between locked decisions, tokens, agent contracts, and consumer code; updates the canonical changelog; surfaces stale references for Samer / Andrew / Tariq / Mark Watson / future-agent. Use when the user mentions: signal-ds, signal portal, signal-portal, TOPIC, KERNEL, TEMPO, Storybook, design system, DS-NNN / BRD-NNN / ADR-NNN decision, token update, brand sweep, version-control sweep, meta-spec, sister-OS, "make sure everything is in sync".
---

# signal-system-sweep

You are about to make a change that touches one of the four Scrips operating systems — **SIGNAL** (Design) · **TOPIC** (Product) · **KERNEL** (Engineering) · **TEMPO** (Operations) — or any of their downstream artefacts (Storybook, tokens, ADRs, constitutional docs per META-SPEC). Run this skill **before and after** the change so the system stays unified across all consumers (Samer, Andrew, Tariq, Mark Watson advisor review, Claude Code, Claude Design, Claude in Chrome, future agents).

## The four operating systems

| OS | Domain | Canonical location |
|---|---|---|
| **SIGNAL** | Design | `~/scrips-repos/scrips-signal-ds/` (DESIGN-STATE.md + tokens + components) + `@scripsteam/scrips-signal-ds` package + signal-ds.vercel.app |
| **TOPIC** | Product | `~/claude-os/docs/topic-v2/src/Topic.jsx` (canonical) + topic.html (rendered v1) + vault `TOPIC.md` pointer |
| **KERNEL** | Engineering | Vault `KERNEL.md` (currently scaffold; questionnaire-driven draft in progress 2026-05-17) — see `00-inbox/2026-05-17-kernel-questionnaire-prefilled-draft.md` |
| **TEMPO** | Operations | Vault `TEMPO.md` (per sister-OS — operations/cadence/capacity) |
| **META-SPEC** | The contract every constitutional doc above follows | Vault `META-SPEC.md` — six-slot frontmatter contract |

## When to fire

Auto-fire when the conversation touches any of:

- Signal design system: tokens, decisions, contracts, llms.txt, DESIGN-STATE.md, design-tokens.ts, design-map.json
- TOPIC (the editorial source-of-truth document)
- Storybook: stories, Chromatic, signal-ds.vercel.app/storybook
- Kernel: CLAUDE.md, SKILL files, env/context, agent instructions
- Any DS-NNN decision (lock, amendment, rollback, supersede)
- Brand assets: logo, wordmark, Orb, fonts
- Color or palette changes (any hex value in the canonical set or REJECTED list)
- W3C tokens.json, figma-variables.json, ai-tools-brief.html

Don't fire for: pure code changes inside `src/scheduling/`, `src/billing/`, `src/patients/` that only consume tokens (those go through `flutter-to-react` or the standard port path).

## What it does — pre-change

1. **Pull latest from all related repos** (parallel where possible):
   - `Scripsteam/scrips-signal-ds` (main)
   - `samertad/signal-portal` (main)
   - `Scripsteam/dev-scrips-pm-react` (main)
   - `~/.claude/` (read-only, but show recent commits in ~/.claude/skills/ + ~/.claude/context/)
2. **Read DESIGN-STATE.md** — confirm current LOCKED list (DS-001..DS-NNN). Surface any PROPOSED / EXPERIMENTAL entries.
3. **Run token validator** (`node tokens/build-tokens.mjs` in scrips-signal-ds) — fails loud on DS-015 (blue/500=#005FD4) or REJECTED-list violations.
4. **Run drift detectors** (greps):
   - `#0076F8` outside `_rejected` / commentary lists → DS-015 violation
   - `#1A8F7A` or `#C25B12` outside REJECTED → DS-012 violation
   - `bg-X-100 text-X-700` hand-bound pills outside `signal-ds/atoms/StatusChip/` → DS-016 / PR #176 violation
   - Storybook titles not under `Signal DS/<Surface>/...` for files in `src/components/signal-ds/`
5. **Cross-doc consistency** — compare token values across:
   - `scrips-signal-ds/tokens/design-tokens.ts`
   - `scrips-signal-ds/tokens/tokens.w3c.json`
   - `scrips-signal-ds/tokens/figma-variables.json`
   - `scrips-signal-ds/DESIGN-STATE.md` (LOCKED section)
   - `signal-portal/tokens.json` (mirror)
   - `signal-portal/ai-tools-brief.html` (inline values)
   - Drift → flag before proceeding.

## What it does — post-change

After the user-driven change lands, run:

1. **Update `Scripsteam/scrips-signal-ds/CHANGELOG.md`** — single line per change with date, DS-NNN reference, one-sentence summary, commit SHA. Format: `2026-MM-DD · DS-NNN · <summary> · <repo>@<sha>`.
2. **Sync mirrored consumers** (run, don't ask):
   - Copy updated `tokens.w3c.json` → `signal-portal/tokens.json`
   - Copy updated `figma-variables.json` → `signal-portal/figma-variables.json`
   - Copy updated `design-map.json` → `signal-portal/design-map.json`
   - If `ai-tools-brief.html` references inline values that changed, regenerate.
3. **Commit + push both repos** (signal-ds first, then portal). Vercel auto-deploys portal.
4. **Verify endpoints live** (`curl -sIo /dev/null -w '%{http_code}'`):
   - signal-ds.vercel.app/tokens.json
   - signal-ds.vercel.app/figma-variables.json
   - signal-ds.vercel.app/ai-tools-brief.html
   - signal-ds.vercel.app/fonts/scrips-fonts.css
5. **Update Andrew / Tariq / agent CLAUDE.md** if the change shifts a token or vocabulary they reference:
   - `dev-scrips-pm-react/CLAUDE.md` — Andrew's agent
   - Future: `dev-scrips-pm-react/.claude/skills/flutter-to-react/SKILL.md`
   - `~/.claude/skills/html-artifact.md` — artifact authoring
   - `~/.claude/context/signal-ds-authority.md` — agent hierarchy contract
6. **Re-brief Claude Design** if a canonical token / font / decision changed. DM via the design chat with the locked text inline (per `feedback_synthesize_for_external_ai_tools`).
7. **Trigger Storybook publish** (when SIGNAL_PORTAL_DEPLOY_PAT secret is set in scrips-signal-ds):
   - `gh workflow run storybook-publish.yml --repo Scripsteam/scrips-signal-ds --ref main`
   - Wait for completion; verify `signal-ds.vercel.app/storybook` is fresh.
8. **Refresh the vault `SIGNAL.md` pointer block** (added 2026-06-07 — the May→June drift proved "per-event" doesn't fire itself): if the sweep touched package version, DS-lock range, canonical Figma file, or enforcement tooling, update the corresponding line in vault `SIGNAL.md` (frontmatter `slot-6` + the POINTER-CANONICAL block) with a dated provenance note. Verify against PRIMARY (`package.json`, `DESIGN-STATE.md`) before writing — never copy from another mirror.
9. **Post a one-line summary** to the daily-activity-log with `[HUMAN]` or `[SKILL]` attribution per `feedback_attribution_tagging`.

## Single-source / no-dual-maintenance rule (software factory) — 2026-06-05

Every canonical DS fact has **one source of truth**; all other appearances are **generated
mirrors**, never hand-edited copies. A hand-maintained second copy is a drift bug — *blacklisted*.
Full registry: `Scripsteam/scrips-signal-ds/docs/single-source-registry.md`.

| Fact | SINGLE SOURCE | Mirrors regenerate from it |
|---|---|---|
| All tokens / primary `#005FD4` | `tokens/design-tokens.ts` | tokens.css, figma-variables.json, w3c.json, portal tokens.json, scrips-react index.css (via `build-tokens.mjs`) |
| Rejected denylist (15-hex) | `tokens/design-tokens.ts` `REJECTED_COLORS` | `build-tokens.mjs` now **derives** it; eslint denylist is the one allowed manual mirror (target: import from package) |
| Canonical Figma key `qrKkhV…` | `tokens/design-map.json` `figma.designSystemFileKey` | DESIGN-STATE.md, llms.txt, design-system-rules.md |
| Fonts (Inter / JetBrains) | `design-tokens.ts` typography | component stacks, portal font CSS |

**When you touch any of these:** edit the SOURCE only, run the generator (it aborts on drift),
let mirrors follow. Never add a second hand-copy. If a sweep finds a dual-maintained value,
replace the copy with a derived reference in the same pass.

## Drift report format

When pre-change or post-change drift is detected, surface it in this format:

```
DRIFT REPORT — <YYYY-MM-DD>

Locked decisions touched:
- DS-NNN — <one line>

Drift found:
1. <file>:<line> — <what's wrong> — <what it should be>
2. ...

Proposed fixes:
- <file> — <surgical change>
- ...
```

User confirms → execute the fixes in the same compound-fix cycle (per `feedback_compound_fix_never_defer`).

## Consumers this skill keeps in sync

| Consumer | What it reads | How sweep keeps it current |
|---|---|---|
| Samer | DESIGN-STATE.md, CHANGELOG.md, ~/claude-os/daily-activity-log.md | Updated in same pass + activity log entry |
| Andrew | `Scripsteam/dev-scrips-pm-react/CLAUDE.md` + `.claude/skills/flutter-to-react/SKILL.md` | Patched when token/vocabulary shifts (PR-driven) |
| Tariq | Future: `Scripsteam/dev-scrips-pm-react/CLAUDE.md` (same as Andrew) | Same as Andrew |
| Claude Design | tokens.json fetched at session start + ai-tools-brief.html + canonical-CSS URL | Auto-current (it fetches signal-ds.vercel.app/*); also re-DM'd when major locks ship |
| Claude Code (this agent) | ~/.claude/skills/, ~/.claude/context/, MEMORY.md | Patched directly + memory updated if cross-cutting |
| Claude in Chrome | Public endpoints only (signal-ds.vercel.app) | Auto-current via portal redeploy |
| GitHub Actions (storybook-publish) | scrips-signal-ds tokens + storybook | Auto-runs on push to main when PAT is configured |
| Future agents | All of the above via the skill registry | Reads this skill description on session start |

## Files this skill writes to

- `Scripsteam/scrips-signal-ds/CHANGELOG.md` — append a line per change
- `Scripsteam/scrips-signal-ds/DESIGN-STATE.md` — append a new DS-NNN if locking
- `Scripsteam/scrips-signal-ds/tokens/*.json` — regenerate from design-tokens.ts on token changes
- `samertad/signal-portal/{tokens,figma-variables,design-map}.json` — copy from signal-ds
- `samertad/signal-portal/ai-tools-brief.html` — regenerate when inline values change
- `~/claude-os/daily-activity-log.md` — append [HUMAN]/[SKILL] tagged summary

## Files this skill never writes to without explicit Samer approval

- `Scripsteam/scrips-signal-ds/DESIGN-STATE.md` LOCKED section — locks require explicit Samer pick per `feedback_drafts_not_decisions`. Auto-mode classifier will block.
- Any `*.tsx` / `*.ts` source files outside the design-system repo (those go through Andrew or Tariq's normal PR flow).
- `~/.claude/CLAUDE.md` or `~/.claude/context/*` — these change Samer's global agent instructions; ask first.

## Failure modes + recovery

| Symptom | Cause | Recovery |
|---|---|---|
| `node tokens/build-tokens.mjs` exits non-zero | A REJECTED hex appears in design-tokens.ts, or DS-015 violated (blue/500 ≠ #005FD4) | Identify the offending hex, swap to the canonical value, re-run validator |
| Vercel deploy 404s on signal-ds.vercel.app/* after push | `vercel --prod` not run (auto-deploy isn't wired for signal-portal) | `cd ~/scrips-repos/signal-portal && vercel --prod` |
| Storybook URL 401s | Chromatic auth gate (pre-DS-018 / pre-GH-Actions) | If PAT is set: `gh workflow run storybook-publish.yml --repo Scripsteam/scrips-signal-ds`. If not set: manual `npm run build-storybook` + copy to signal-portal/storybook/. |
| Claude Design banner "Missing brand fonts" after DS-017 | UI-managed font cache separate from CSS | Samer must upload woff2 via Claude Design "Upload fonts" button; can't be automated |
| Andrew's `CLAUDE.md` still references old hex / vocabulary after a lock | Andrew's repo wasn't included in the sweep | Open a PR against `Scripsteam/dev-scrips-pm-react` patching `CLAUDE.md`; reference the new DS-NNN |

## Post-change handshake (Claude Design ↔ Signal DS)

After a push to `Scripsteam/scrips-signal-ds:main` that touches
`DESIGN-STATE.md`, `CHANGELOG.md`, `tokens/`, `src/`, or `package.json`,
the `sync-claude-design.yml` GH Action fires automatically. Verify it ran:

```bash
gh run list --repo Scripsteam/scrips-signal-ds --workflow sync-claude-design.yml --limit 1
```

The workflow is tolerant of missing `SCRIPS_SLACK_BOT_TOKEN`. Inbound
Claude Design proposals arrive as GitHub issues labelled `ds-proposal`
and are validated by `validate-ds-proposal.yml`. Full protocol:
`~/scrips-repos/scrips-signal-ds/docs/claude-design-handshake.md`.

## Relationship to other skills

- **`html-artifact`** — when generating artifacts about Signal DS work, this skill ensures the artifact references the current locked values (via signal-ds.vercel.app/fonts/scrips-fonts.css + #005FD4).
- **`figma-design-sweep`** — when sweeping Figma frames, this skill ensures Figma variables and tokens.w3c.json stay in sync.
- **`flutter-to-react`** (in dev-scrips-pm-react) — when Andrew/Tariq port a component, the SKILL.md it loads should always reflect the latest locked decisions. This skill keeps that file current.
- **`session-capture`** — at EOD, if signal-system-sweep ran during the session, the wrap should include the CHANGELOG.md entries + activity log.

## Anti-pattern: don't fire this for

- A port task that consumes existing tokens (use `flutter-to-react`)
- A pure code fix in a domain folder (`src/scheduling/`, `src/billing/`, etc.)
- A Storybook story update for an unchanged component
- Documentation edits to `~/claude-os/` outside `daily-activity-log.md`

If unsure, default to running it — false positives are cheap; missed drift compounds.
