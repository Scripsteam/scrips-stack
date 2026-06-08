---
name: sdlc-handoff
description: >
  Product→engineering handoff contract + Software Factory gate enforcement. Load this
  whenever a coding agent or engineer is about to PICK UP product work and implement it —
  starting a sprint-runner, "implement this story/feature", executing an SDLC stage, or
  building anything that a product spec hands off. Enforces the product/engineering boundary,
  the Definition-of-Ready handoff packet, the per-stage manifest gate, and the agent
  must/never rules. Owns the GENERAL handoff/definition-of-ready/gate discipline across the
  whole SDLC; defers the design slice to design-to-dev-pipeline and the pipeline structure to
  docs/superpowers/sdlc/PIPELINE.md.
type: procedure
---

# sdlc-handoff

Canonical: vault `06-decisions/product/2026-06-05-sdlc-software-factory-handoff.md`.
Readable: `~/claude-os/artifacts/2026-06-05-product-engineering-handoff-canonical-rules.html`.

## The boundary (non-negotiable)

- **Product** owns *what/why*: capability, packaging (tier + `feature.*` flag), clinical truth
  (Studio PlanDefinition/Measure), Signal DS + FHIR contracts, acceptance criteria.
- **Engineering** (you, coding agent / human) owns *how*: code, schema, services, tests,
  deploy, **server-side** entitlement gating.
- Tier/flags/clinical-truth/DS+FHIR contracts travel WITH the work. **Never invent them** —
  read the carried packet, or stop and ask.

## Before you start — verify the Definition of Ready packet

Do not begin implementation until the handoff packet carries ALL of:

1. Capability + why (the user/clinical question).
2. Tier + `feature.*` flag — gate it **server-side** from entitlement, not UI-hide.
3. Signal DS components — named/levelled (component|card|block|template|frame); clinical =
   FHIR-resource-named; states enumerated; net-new UI designed in Claude Design first
   (→ `design-to-dev-pipeline`).
4. FHIR + clinical contract — resource binding, value-sets, gate conditions — from Studio,
   not invented in code.
5. BDD acceptance criteria.
6. Backend mapping + data path.
7. Provenance — numbers tagged; synthetic vs live flagged.
8. Human gates — any action (orders/dispatch) is human-confirmed, never auto-executed.

Missing any → not ready. Send it back to product; do not fill the gap with invention.

## The factory gate

Read the prior stage's `_manifest.md` (`docs/superpowers/sdlc/PIPELINE.md`). Do not start your
stage unless its gate reads `passed: true`. When you finish, write your own `_manifest.md`
with the gate checklist + evidence. Template: `docs/superpowers/sdlc/_manifest-template.md`.
Check with `docs/superpowers/sdlc/check-gate.sh <prior-stage-folder>`.

## Must

- Build on EXISTING Signal DS + the carried contracts; read the real `.d.ts` / FHIR / nav
  source before coding — never guess an API or a nav/icon set.
- Gate the flag server-side; respect base/enterprise tier.
- Verify vs the acceptance criteria (CI green: lint · typecheck · vitest · axe · e2e).
- **Functional gate:** prove it WORKS in the running app, not just renders.
- **Independently test interactivity — never trust a self-verifier's pass.** (A coding agent
  reported "tab routing checks out" while the tabs did not switch; an interactive Present-mode
  test caught it, 2026-06-05.) See `feedback_self_grading_goodhart_broken`,
  `feedback_smoke_test_before_done`, `feedback_blast_radius_before_done_claim`.
- **Right-size the model.** Opus 4.8 for architecture/security/whole-repo reasoning; Sonnet 4.6
  for bulk implementation/review/orchestration; Haiku 4.5 for mechanical (format/lint/tests/
  log-parse). Set per-agent model overrides on cheap workers; never lock the whole run to Opus.
  Full table + token rules: the canonical doc §5 (commands/modes + model orchestration).

## Never

- Invent a tier, flag, clinical threshold, chart type, brand value, or **nav/icon set** — read
  the real source (see `feedback_no_fiction_ports`).
- Hardcode a clinical measure/pathway — it comes from Studio definitions.
- Auto-execute a clinical action without a human confirm
  (`feedback_agent_authored_auth_needs_human_review`).
- Hand-build net-new UI as a substitute for Claude Design → DS.
- Ship auth/security on a green build alone — adversarial refuter panel + human owner first.

## Hands off to

- Design SDLC (Stage 05) → `scrips-design-sdlc` owns the design process + gates (Phase-0 verify-canonical, 14-pt Validate); `design-to-dev-pipeline` owns execution (Claude Design → React → Storybook → wire → graduate). Graduation gated by `signal-ds-judge` + `signal-ds-graduation` + `figma-doc-sync` + `signal-system-sweep`. Net-new UI designed in Claude Design, never hand-built.
- Pipeline structure / stage list → `docs/superpowers/sdlc/PIPELINE.md`.
- Review/security gates → `/review`, `security-review`, `signal-ds-judge`.
- Retro (stage 10) → `/retro` MUST emit a feedback memo + skill/CLAUDE update so the factory compounds.

**Origin:** 2026-06-05 — Samer directed canonical product→engineering handoff rules after
repeated agent invention (tiers, nav icons) and a false self-verifier pass. Locked + graduated
from the canonical-rules artifact.
