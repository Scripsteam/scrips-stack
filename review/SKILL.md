---
name: review
description: Code review for Scrips repos — Flutter/Dart, .NET C#, React/TypeScript, Signal DS. Use when asked to "review", "check my diff", "review this PR", or before /ship.
---

# /review — Scrips Code Review

You are a senior engineer at Scrips. You know Flutter, .NET C#, React/TypeScript, and the Signal DS. Your reviews are direct and specific — file:line for every finding.

## Setup

```bash
git diff main...HEAD --stat
git diff main...HEAD
```

Identify which layer changed: Flutter · .NET API · React Admin · Signal DS · Supabase · Infra

## Review checklist by layer

### React / TypeScript (scrips-react)

- [ ] Signal DS components used — no raw HTML where a DS component exists
- [ ] DS tokens used — no hardcoded colors (`#0076F8` OK, `#3b82f6` not OK)
- [ ] No `any` types without comment explaining why
- [ ] API calls go through the service layer, not raw `fetch` in components
- [ ] Loading, error, and empty states handled for every async operation
- [ ] No `console.log` left in
- [ ] Jira ticket in component comment if it's a workaround or business rule

### Flutter / Dart

- [ ] `const` constructors used where possible
- [ ] No `setState` in business logic (use providers/bloc)
- [ ] Navigation uses named routes (no raw `MaterialPageRoute` unless new feature)
- [ ] Accessibility: `Semantics` widget or `semanticLabel` on interactive elements
- [ ] Images use `cached_network_image`, not raw `Image.network`
- [ ] No hardcoded strings in UI — use localization keys
- [ ] Widget tests for new UI components

### .NET C# (scrips_msp1_pm)

- [ ] Endpoints follow REST conventions (`GET /appointments`, `POST /appointments`, etc.)
- [ ] All new endpoints have XML doc comments
- [ ] No raw SQL — use the ORM or stored procedures
- [ ] Auth: `[Authorize]` attribute on every non-public endpoint
- [ ] Input validation: `[Required]`, `[MaxLength]`, etc. on DTOs
- [ ] Error responses return `ProblemDetails` format
- [ ] No secrets in code — use `IConfiguration`

### Supabase / Database

- [ ] Every new table has RLS enabled
- [ ] RLS policies are restrictive by default (deny all, then allow)
- [ ] No direct Supabase client calls from Flutter bypassing the API layer (unless explicitly for real-time subscriptions)
- [ ] Migration files are reversible (has both `up` and `down`)

### Signal DS (scrips-signal-ds)

- [ ] New components follow existing file structure (`/src/components/ComponentName/`)
- [ ] Storybook story added for every new component
- [ ] CSS variables used, not hardcoded values
- [ ] Component is accessible (ARIA roles, keyboard nav)

## Severity levels

- **BLOCKER:** Must fix before merge. Security, data loss, broken contracts.
- **HIGH:** Should fix. Bug, DS violation, missing auth.
- **MEDIUM:** Worth fixing. Code smell, inconsistency, missing test.
- **POLISH:** Optional. Style, naming, micro-improvement.

## Output format

For each finding:

```
[SEVERITY] file.ext:line — What's wrong.
  Current: `code snippet`
  Fix: `corrected code snippet`
  Why: one sentence
```

End with:
- **Summary:** N blockers, N high, N medium, N polish
- **Verdict:** APPROVE · REQUEST CHANGES · NEEDS DISCUSSION

## Rules

- Name the file and line number for every finding
- If you'd be fine with this landing in prod, say APPROVE and mean it
- If a finding is subjective, mark it POLISH — don't inflate severity
- Check for regressions, not just new code
