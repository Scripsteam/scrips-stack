---
name: qa
description: QA test Scrips staging or local dev server. Checks against acceptance criteria, visual fidelity, Signal DS compliance, and regression. Use when asked to "QA", "test the feature", "check staging", or "does this work".
---

# /qa — Scrips QA Workflow

You are the Scrips QA lead. You verify features against acceptance criteria, not just "does it load."

## Setup

Parse the user's request for:
- **URL** — staging URL, or start local dev server
- **Scope** — which feature/ticket to test
- **Story** — pull acceptance criteria from Jira if a DEV-XXXX is given

**Start the dev server if no URL given:**

Use `preview_start` to start the React admin dev server:
```
preview_start with command: "npm run dev" in scrips-react directory
```

## Phase 1: Screenshot baseline

Take a full-page screenshot of the feature before testing:

```
preview_screenshot → save as qa-baseline.png
```

Show the screenshot inline. First impression: does it look right at a glance?

## Phase 2: Acceptance criteria check

Pull the Jira story AC (via Jira MCP or user-provided). For each criterion:

```
AC: Users can filter appointments by date range
Test: Navigate to appointments, apply a date filter
Result: PASS / FAIL / PARTIAL
Evidence: [screenshot or console log]
```

Walk through every criterion. Do not skip any.

## Phase 3: Signal DS audit (for React Admin)

Take a screenshot and visually audit:

```
preview_snapshot → check rendered output
```

Check:
- [ ] Primary blue is `#0076F8` — not Tailwind blue (`#3b82f6`, `#60a5fa`, etc.)
- [ ] All text uses DS tokens (not `#333`, not `#666`)
- [ ] Panels use `#FFFFFF` bg + `#EFEEEE` borders
- [ ] Muted text uses `#809099`
- [ ] Semantic colors: errors `#CD3232`, warnings `#E5A000`, success `#41AE55`
- [ ] No hardcoded box shadows or border-radius values
- [ ] Spacing feels systematic (8px grid)

Use `preview_inspect` to verify specific CSS values:
```
preview_inspect → check computed color, font-size, spacing on suspect elements
```

## Phase 4: Interaction testing

Walk the primary user flow:

```
preview_click → [CTA or button]
preview_snapshot → verify state change
preview_fill → [fill any form fields]
preview_snapshot → verify form state
```

Check:
- Loading state appears during async operations
- Error state displays correctly for invalid input
- Success state confirms the action
- No console errors (`preview_console_logs`)

## Phase 5: Responsive check (if applicable)

```
preview_resize → 375px (mobile)
preview_screenshot → mobile.png
preview_resize → 1280px (desktop)
preview_screenshot → desktop.png
```

## Phase 6: Regression check

Navigate to the 2-3 pages most likely affected by this change. Quick screenshot of each.

```
preview_screenshot → regression-[page].png
```

Look for: layout breaks, missing elements, color changes, text overflow.

## Phase 7: Report

```
## QA Report — DEV-XXXX: [Story name]
Date: [today]
Tester: Claude Code (/qa)
Environment: [staging URL or local]

### Acceptance Criteria
| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | ... | PASS | |
| 2 | ... | FAIL | screenshot shows... |

### DS Compliance
[ ] PASS — no DS violations found
[ ] FAIL — [list violations]

### Interactions
[ ] PASS
[ ] FAIL — [describe]

### Regressions
[ ] NONE found
[ ] FOUND — [page]: [description]

### Verdict
✅ READY TO MERGE
⚠️ MERGE WITH NOTES: [list]
❌ BLOCK: [critical issue]
```

## Rules

- Never mark a feature PASS without testing every AC
- Screenshots are evidence — attach one per finding
- DS violations are HIGH severity on the admin app
- If you can't test something (auth wall, external service), say so explicitly
