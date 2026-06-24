---
name: encounter-builder
description: The single autonomous "one fire" that builds the Scrips practitioner encounter end-to-end (pre-encounter → encounter → ordering → telemedicine) against the locked Encounter Contract. Reads the Contract as source of truth, drives the build wave-by-wave with sub-agents + verify loops, runs the layout-parity gate + an independent judge before every PR, opens DRAFT PRs for human merge, and pauses at each wave boundary for review. Full-stack (FE + the missing .NET endpoints). Use when picking up the practitioner-encounter build.
---

# Encounter Builder — the one fire

Autonomous, wave-gated build of the practitioner encounter. **One invocation drives the whole lifecycle**; it pauses for human review + merge at each wave boundary, then continues. Zero by-eye frame guessing — everything is grounded in and gated against the **Encounter Contract**.

**Announce at start:** "Running encounter-builder — Wave [N] against the Encounter Contract."

---

## 0. THE SOURCE OF TRUTH (read first, every run — non-negotiable)

Read the **Encounter Contract** before anything else:
`scrips-practitioner-react/docs/encounter-contract.md` (the working SoT; ratified as ADR-ENCOUNTER-001).

It is the **reconciliation authority** — when Jira, memory, a Figma file, or the Flutter code disagree with it, **the Contract wins**. Never re-derive the frame by eye from Flutter. Key things it locks (do not re-litigate):
- The encounter is **one declarative block host** (`EncounterShell`); phase/modality/patient-context/tier only change *which blocks are present and where*.
- Source-ownership (§1): Figma Encounter-2 owns layout; Flutter owns behavior (lifted, **never** copied structurally); **one content path** = a Template Studio FHIR Questionnaire → one `QuestionnaireRenderer`; DS Televisit owns telemedicine.
- **§6 (care-modeling) is RESOLVED:** care-modeling is the **superior orchestration layer that CALLS the building blocks by typed reference** — a `form` step calls a TS Questionnaire by canonical (→ HPI/ROS/PE). **Build ONE content path, not two.** The orchestration composition is Phase 0's module, not the encounter's content path.
- Telemedicine = **compose the DS Televisit family + WIRE the iframe transport** (not a free drop-in).
- The wearable-vitals-over-video strip is **parked** (ADR-FHIR-003) — never build it.

If the Contract file is absent in the repo, STOP and report — do not proceed from memory.

---

## 1. Outcome tracking (MANDATORY)
- **Start — RECALL** `agent-outcome-tracker`: query `agent_traces` where `agent_skill='encounter-builder'` (last 10) + brain recall `"encounter builder wave practitioner react"`; declare adjustments in one line.
- **Per wave — CAPTURE:** `task_type: encounter-wave`, `feature_slug: encounter-wave-[N]`, score 5 first-pass-clean / 3 rework / 1 blocked.

---

## 2. Boundaries (hold these absolutely)
- **DRAFT PRs only. NEVER merge, deploy, self-approve, or touch infra** (az/kubectl/terraform/secret/delete). Humans merge protected paths (ADR-008).
- **Wave-gated:** at each wave boundary → open the DRAFT PR(s), run the judge, then **PushNotify Samer + PAUSE.** Resume the next wave only on his go.
- **Clinical sign-off** is Samer/clinical-advisor's — gate any wave that touches clinical thresholds; never invent a cut-point.
- **Full-stack scope:** you own the missing .NET endpoints (be-sprint-runner pattern) but **coordinate backend merges with Andrew.**
- **Team comms → `#current-active-team-scrips`** (@mention), never DM.
- **Never** build a second content path (§6), the parked wearable strip (§8), or rebuild the Televisit video UI.

---

## 3. Preflight (each run)
1. Read the Contract (§0). Read the wave tracker `claude-os/state/encounter-build.md` (create it on first run from the §11 wave plan); determine the current wave + its status.
2. **Verify current `main`** of `scrips-practitioner-react` (don't trust a stale local checkout): `git fetch origin && git show origin/main:src/encounter/encounter-shell-view.tsx` — confirm the §9 current-state table still holds; if `main` moved, reconcile the wave's starting point before building.
3. Spin an **isolated worktree** per the worktree rules (`bash ~/claude-os/scripts/cos-worktree.sh encounter-wave-[N]`) — never branch-switch a shared clone.

---

## 4. The wave loop (run the current wave to a gated DRAFT PR, then pause)

For the current wave, run this loop. Decompose the wave into its child stories (from the Jira epic tree the Contract §11 names) and run each story through:

1. **Discovery (Contract-first dispatch):** hand each sub-agent the relevant **Contract excerpt** + the canonical **Figma frame** (pull live via the cloud Figma MCP — `get_design_context`/`get_screenshot` on the frame the Contract §2 names for this screen; latest-dated-per-route) + the **Flutter behavior** (lifted, file:line from §5 — context rules, ordering, transport). Nothing gets built that isn't in the Contract.
2. **Build (compose the chassis — do not reinvent):**
   - FE stories → the `admin-sprint-runner` per-story loop (brainstorm → writing-plans → subagent-driven-development → review), composing Signal DS organisms (`QuestionnaireRenderer`, `AssessmentPlanCanvas`, `InternationalPatientSummary`, `EncounterStep*`, `VitalsRow`, `Televisit*`). Apply `flutter-style-port` for token mapping. Pin the latest signal-ds.
   - BE stories (missing endpoints) → the `be-sprint-runner` loop, worktree-per-service, TDD, additive migrations.
3. **Verify (no claim without primary evidence — verification gate):**
   - `tsc` 0 + `npm run build` (FE); `dotnet build`/`dotnet test` (BE) — real output.
   - **Storybook screenshots across the Contract's personas** (pediatric / female-of-age / male / virtual) — proves context-awareness actually fires, taken this run (not a sub-agent's word).
   - `scrips-verify` PASS (integration + security always-on; FE/BE conditional).
   - **The §10 layout-parity gate** (Contract §10 + §13b) — measurable thresholds, semantic selectors, in-person vs virtual branches, +/- context personas. Run it on the real render, not just Storybook.
   - `design-parity-judge` vs the Contract block model.
4. **Independent judge:** a separate agent reads the code + screenshots and returns PASS/FAIL **before** the PR goes to Samer (judge-before-merge). Relay its verdict as an input to check, never as your own verification.
5. **Open the DRAFT PR** (`ship` skill conventions: branch, Jira link, changelog, reviewers). Then `ci-watch-and-fix` for mechanical CI failures (never auto-patch logic).
6. **Wave-gate:** update the tracker (PR#, evidence), post a one-line status to `#current-active-team-scrips`, then **PushNotify Samer with the wave's evidence and PAUSE.** Do not start the next wave until he says go.

---

## 5. Wave plan (from Contract §11)
- **Wave 0 — `EncounterShell` block host + zone engine + context-resolver** (PROD-1273). The keystone. Collapse today's 4 columns → 3 (vertical step-nav → horizontal status tabs), add the 4-tab right drawer, make it the declarative block engine. *Build first — everything slots in.*
- **Wave 1 — steps as blocks:** Risk/ROS/PE/Docs/Wrap-up (PROD-1234) + A/P page-wiring (PROD-1144); add the `pe` step key. HPI/ROS/PE content = the TS Questionnaire resolved from the active CarePlan's current `form` step (§6), one renderer.
- **Wave 2 — vitals + context-awareness:** top vitals canvas (PROD-1274) + pediatric HC + LMP + gender-filtered ROS/PE (PROD-1236/1237) + 36-record history.
- **Wave 3 — ordering depth:** ICD/SNOMED search, medication dosage (PROD-1167), order FHIR writes. **BE:** the missing search + order-write endpoints.
- **Wave 4 — telemedicine:** virtual mode composes the Televisit family **+ wires the iframe transport** (PROD-1276). **BE:** video-URL endpoint.
- **Wave 5 — pre-encounter parity + drawer:** chief-complaint persist, reschedule, sign&locked, previous notes; the in-encounter 4-tab drawer (PROD-1260).

Default sequential; Waves 2/3/4 may run as parallel sub-streams within one gate once Wave 0 lands, if Samer approves the parallelism.

---

## 6. Stop conditions / escalate (PushNotify Samer)
- Any wave-gate (always).
- A clinical-threshold decision, an ADR contradiction, infra/spend, or a Contract gap the build exposes (file it back into the Contract + flag).
- A judge FAIL you can't resolve in 2 iterations.
- Never silently defer — log it to `claude-os/state/open-loops.md` with an owner.
