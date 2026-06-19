---
name: scrips-verify
description: >
  Unified pre-handback verification for Scrips features. Runs a diff-aware multi-dimensional
  check before any merge/PR is created. Always-on: integration + security. Conditional:
  frontend (if UI files changed), backend (if .NET files changed), devops (if env/config
  changed). Outputs PASS / FAIL / ESCALATE per section. Called by finishing-a-development-branch
  Step 1.5 and by the ship skill before creating a PR.
type: procedure
---

# /scrips-verify — Unified Pre-Handback Verification

**Announce at start:** "I'm running scrips-verify — unified pre-handback check."

## Why this skill exists

Separate verification skills (frontend-verify, backend-verify) create integration seams. An orchestrator routing "this is frontend-only" misses cross-surface implications (e.g., a React component that invokes a new .NET endpoint that has no auth gate). One unified skill with always-on cross-cutting checks is safer.

---

## Step 1 — Diff analysis

```bash
git diff origin/main...HEAD --name-only
```

Classify each changed file into sections:
- **Frontend**: `*.tsx`, `*.ts`, `*.css`, anything under `src/`, `components/`, `pages/`
- **Backend**: `*.cs`, `*.csproj`, migrations, `appsettings*.json`
- **DevOps**: `*.yaml`/`*.yml` in `.github/`, `k8s/`, `helm/`, `Dockerfile`, env vars
- **DS**: `scrips-signal-ds/` files, `design-tokens.ts`, `contracts/`

---

## Step 2 — Always-on checks

### Integration (always run)
- [ ] Every new API call from FE has a corresponding .NET endpoint in the diff (no orphaned calls)
- [ ] Every new .NET endpoint called from FE has an auth gate (`[Authorize]`, role check, or `permissiongrp` validation)
- [ ] FHIR ResourceType used in the feature matches the Stage 00 brief binding (no drift from brief)
- [ ] No new cross-service calls without a corresponding service registration or `HttpClient` injection

### Security (always run)
- [ ] No hardcoded secrets, tokens, or connection strings
- [ ] PHI access paths have explicit authorization (no `[AllowAnonymous]` on PHI endpoints)
- [ ] Tenant isolation maintained: every data query includes `OrgId` filter where applicable
- [ ] File upload paths (if any): MIME type validation + size limit present
- [ ] New roles/permissions match the `permissiongrp` pattern — no `if (user.Role == "Nurse")` string literals

---

## Step 3 — Conditional checks

### Frontend (run if frontend files changed)
- [ ] Signal DS tokens used — no hardcoded hex colors (grep for `#[0-9A-Fa-f]{3,6}` in changed `.tsx`/`.ts`)
- [ ] No `console.log` left in production paths
- [ ] Design-parity-judge gate: call `design-parity-judge` skill if a new screen or component is in the diff
- [ ] All interactive elements have accessible labels (no bare icon buttons without `aria-label`)
- [ ] TypeScript strict mode — no `any` introduced in changed files (grep for `: any` in diff)

### Backend (run if .NET files changed)
- [ ] `dotnet build` passes (or flag as UNVERIFIED if .NET runtime unavailable)
- [ ] Migrations are additive — no destructive column drops or type changes on live tables
- [ ] New endpoints follow existing auth patterns (Bearer + `[Authorize(Policy=...)]`)
- [ ] No `catch (Exception)` without logging

### DevOps (run if config/env/k8s files changed)
- [ ] No secrets in YAML — all sensitive values use `$(VARIABLE)` or k8s Secret references
- [ ] New env vars documented in `.env.example`
- [ ] k8s resource limits set on any new Deployment

---

## Step 4 — Output

For each section, report:

```
scrips-verify result — <feature> / <branch>

Integration:  PASS | FAIL (N issues) | N/A
Security:     PASS | FAIL (N issues) | ESCALATE
Frontend:     PASS | FAIL (N issues) | N/A (no UI changes)
Backend:      PASS | FAIL (N issues) | UNVERIFIED (no runtime) | N/A
DevOps:       PASS | FAIL (N issues) | N/A

Overall: PASS | FAIL | ESCALATE

Issues:
  [FAIL]    integration: <file:line> — <finding>
  [FAIL]    security: <file:line> — <finding>
  [ESCALATE] security: PHI endpoint lacks explicit authorization — Samer sign-off required
```

**PASS**: All applicable sections pass. Proceed to Codex review (finishing-a-development-branch Step 2.5).

**FAIL**: List all findings with `file:line`. Do NOT create the PR until fixed.

**ESCALATE**: A security or integration finding requires Samer's explicit sign-off before proceeding. Surface the finding with: failure type, file:line, attack vector, recommended fix, confidence level.

---

## Rules

- **ESCALATE beats FAIL**: If any section ESCALATEs, the overall result is ESCALATE regardless of other sections.
- **UNVERIFIED is not a pass**: If backend checks can't run (no .NET runtime), mark the backend section UNVERIFIED and note it in the PR description. Do not claim a clean result.
- **Design-parity-judge is mandatory** when a new screen/component is in the diff. It is not optional even if scrips-verify passes.
- **Security section cannot be waived** — there is no `--skip-security` flag.

## Integration

**Called by:**
- `finishing-a-development-branch` Step 1.5 (between test verification and Codex review)
- `ship` skill before PR creation

**Calls:**
- `design-parity-judge` (if frontend files changed)
- `dotnet build` (if backend files changed)

**Origin:** 2026-06-12 — Replaces the pattern of separate surface-specific verification scripts that created integration seams. Unified skill with always-on integration + security + conditional surface sections.
