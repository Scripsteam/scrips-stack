---
name: feature-brief
description: >
  Stage 00 — Multi-Dimensional Feature Brief. Run this BEFORE any pipeline stage opens,
  BEFORE brainstorming, BEFORE writing-plans, BEFORE any code. Takes any feature idea
  (Jira epic URL, Slack thread, free text) and produces a structured brief across five
  dimensions (product · security · development · design · testing) with cross-dimensional
  conflict detection. Writes Stage 00 artifacts that seed all 10 downstream pipeline stages.
  Universal gate — applies to everyone, not just developers.
type: procedure
---

# /feature-brief — Stage 00 Feature Brief

**Announce at start:** "I'm using the feature-brief skill to run Stage 00 — Multi-Dimensional Feature Brief."

## Why this exists

Gaps in an entry brief surface late and expensively: wrong icon at Stage 07, missing security model at Stage 09, no acceptance tests at Stage 08. Stage 03 (product sign-off) should catch product decisions, not missing security models or unknown DS primitives. This ceremony covers all five dimensions before any stage opens, so every downstream stage starts from complete context.

---

## Step 1 — Parse the input

Accept any of:
- Jira epic URL → fetch via `getJiraIssue`; extract description, children, labels
- Slack thread URL or message → read via `slack_read_thread`; extract the feature idea
- Free text → use as-is

Auto-populate what you can before asking questions:
- FHIR ResourceType → infer from feature domain (scheduling → Appointment/Slot; patient registration → Patient/Coverage; clinical encounter → Encounter/Observation; billing → Claim/ChargeItem)
- Signal DS primitives → grep `~/.claude/skills/scrips` or `~/scrips-repos/scrips-signal-ds/src/index.ts` for relevant exports
- Navigation surface → infer from which app (practitioner / patient / admin) the feature targets

Tell the user what you found: "I found [N] Jira children, inferred FHIR binding [X], detected DS components [Y, Z]. I'll now run the five-dimension interview to fill the gaps."

---

## Step 2 — Five-dimension interview (sequential, single agent)

Work through each dimension in order. Ask all questions in a dimension, then synthesize. Catch cross-dimensional conflicts as they appear — do not defer to the end.

### Dimension 1 — Product
1. Who is this for? (TOPIC persona — practitioner / patient / admin / system)
2. What is broken or missing today? (the pain, not the solution)
3. What does success look like? (measurable outcome — not "user can upload" but "practitioner uploads a consent form in under 30 seconds, receives confirmation, can retrieve it by patient")
4. What are the edge cases and error flows? (what breaks, who calls support)

### Dimension 2 — Security
1. Does this touch PHI? (patient data, clinical records, uploaded documents, PII)
2. Who can see / edit / delete this data? (role model: practitioner / nurse / admin / patient / system)
3. Does it cross service or tenant boundaries? (which services call which; does patient data leave the tenant)
4. Any new auth surface? (new API endpoint, new permission, new role, new file store access)

*Cross-check after this dimension:*
- If PHI touched + design will have a document/image viewer → flag Security × Design conflict: "Security model for PHI document access must be specified before designing the viewer UI."
- If new auth surface + no specification of who owns the permission → flag: "Permission owner unspecified — must be named before Stage 04 stories."
- If the feature is clinical/legal (consent, prescribing, signatures, billing, records release) → flag Regulatory × Security: "Is the chosen mechanism legally sufficient in-jurisdiction? (e.g. a canvas signature vs QES under DHA ST-09 / UAE Decree-Law 46). Name the regulatory bar and confirm the mechanism meets it, or mark `[ESCALATE — Samer + compliance]`."

### Dimension 3 — Development

**0. Claim audit (do this FIRST — before recording any answer in this dimension as fact).**
For every "already exists / already merged / reuses X / wiring verified / engine is live" claim — whether from the requester, the Jira ticket, or your own assumption — **verify it against the live repo before writing it down.** Per the verification gate + github.md code-currency rule:
- `git -C ~/scrips-repos/<repo> log origin/<default> -3 --oneline -- <path>` to confirm freshness, then grep/read the actual file.
- Record each claim in a table: `claim | tier (PRIMARY / UNVERIFIED) | source file:line | verdict (HOLDS / OVERCLAIM / FALSE / BROKEN / NOT-FOUND)`.
- A claim with no `file:line` evidence is recorded as `[UNVERIFIED]`, never as fact. "Reuses the X service" is FALSE if X is not in the repo. "Merged" means you found it on `origin/<default>`, not on a local branch.

This step is load-bearing: a brief that records a requester's "✅ verified" at face value will seed every downstream stage with a false premise. (In the 2026-06-13 dogfood, 3 of 5 status checkmarks failed this audit.)

1. Which FHIR ResourceType(s) bind this feature? (must be a real R4 type — Consent, DocumentReference, Appointment, Observation…)
2. Which existing services/tables are touched? (Scrips.Patient? Scrips.PracticeManagement? QuestionBank? new service?)
3. What are the integration points? (cross-service calls, webhooks, background jobs, S3/blob storage)
4. Is there a live FE being replaced (port) or greenfield?

*Cross-check after this dimension:*
- If Jira children exist but no FHIR binding was specified → flag: "FHIR binding required before BRD synthesis — do not proceed without it."
- If touches Scrips.PracticeManagement + new role → flag Development × Security: "New role in PM requires IdentityServer claim — verify live DB config before Stage 07."
- **Platform-duplication check:** Does this re-build something an accepted or proposed ADR already owns? (search `06-decisions/` + the brain for the capability — e.g. a new authoring surface vs Template Studio's single substrate per ADR-PROTO-010, a new store vs an existing service.) If yes → flag Strategy × Development: "`[ESCALATE — Samer]` this may duplicate <ADR-NNN capability>; confirm build-vs-reuse before any stage opens."
- If the FHIR binding is contested, or the requester proposes a non-FHIR store for a resource that is a confirmed FHIR-native build → **auto-route to the `fhir-architecture-advisor` agent** for the source-of-truth call. Do not resolve it inside this ceremony.

### Dimension 4 — Design
1. Where does this surface in app navigation? (which page/tab/route in practitioner / patient / admin)
2. Which Signal DS primitives are needed? (named + hierarchy level: component / card / block / template / frame)
3. Enumerate all entity states the UI must represent. (e.g., consent form: unsigned / pending-signature / signed / expired / revoked)
4. Any GAPs in Signal DS for the above? (check `~/scrips-repos/scrips-signal-ds/src/index.ts` + `contracts/*.json`)

For each GAP:
```bash
gh issue create --repo Scripsteam/scrips-signal-ds \
  --title "primitive-needed: <surface name>" \
  --label "primitive-needed" \
  --body "Required by: <feature-slug>\nHierarchy level: <component|card|block|template|frame>\nFHIR binding: <ResourceType>"
```

*Cross-check after this dimension:*
- If GAPs > 0 and they are on the critical path → set a blocker on the Jira epic: "DS primitives must exist before Stage 05 design can complete."
- If states enumerated but no state machine yet → flag: "State machine must be in BRD (Stage 02) before Stage 05 design."

### Dimension 5 — Testing
1. What is the BDD acceptance criterion? (Given [state], When [action], Then [outcome] — at least one for the happy path)
2. Alternate flows? Error flows? (what does a bad path look like)
3. Any regression risk to adjacent features? (what could break in existing flows)
4. What would a tester need to see to say "this is done"? (the demo scenario — step by step)

*Cross-check after this dimension:*
- If no error-flow acceptance criteria → flag: "Error flows must be specified — Stage 08 QA will walk them."
- If regression risk named but no related stories in scope → flag: "Regression risk [X] should have a linked story or be explicitly de-scoped."

---

## Step 3 — Cross-dimensional conflict synthesis

After all five dimensions, run a final cross-check:

| Check | Condition | Resolution |
|---|---|---|
| Security × Design | PHI + document/image UI | Define access model before UI design |
| Design × Development | DS GAP on critical-path surface | Create blocker ticket + flag timeline |
| Design × Development | FHIR type not specified but UI shows entity states | FHIR binding must be specified now |
| Testing × Product | No acceptance criteria for error flows | Write them now or mark as `[GAP — must close before Stage 04]` |
| Security × Development | New auth surface + no permission owner | Name the owner now |
| Development × Product | "Greenfield" but adjacent service exists | Verify with the team — is this really greenfield or a seam on an existing service? |
| Strategy × Development | Re-builds an ADR-owned capability | `[ESCALATE — Samer]` confirm build-vs-reuse before any stage opens |
| Regulatory × Security | Clinical/legal feature, mechanism may not be legally sufficient | Name the regulatory bar; `[ESCALATE — Samer + compliance]` if unmet |
| Claim integrity | A "✅ exists/merged/verified" claim has no `file:line` evidence | Record `[UNVERIFIED]`; do not seed downstream stages with it |

All conflicts must be resolved or explicitly marked as `[GAP — owner X, due Stage N]`. No silent gaps.

---

## Step 4 — Write output artifacts

### A. Feature brief

Write to: `~/claude-os/docs/superpowers/sdlc/<feature-slug>/00-feature-brief/<feature-slug>.md`

```markdown
# Feature Brief — <feature-slug>
Date: YYYY-MM-DD
Jira epic: <URL or "-">

## Dimension 1 — Product
**Persona:** <TOPIC persona>
**Pain:** <what breaks today>
**Success metric:** <measurable outcome>
**Edge cases:** <list>

## Dimension 2 — Security
**PHI touched:** yes/no — <description>
**Role model:** <who sees/edits/deletes>
**Service boundary:** <cross-service or single-service>
**New auth surface:** yes/no — <description>

## Dimension 3 — Development
**FHIR primary:** <ResourceType>
**FHIR secondary:** <ResourceType list>
**Services touched:** <list>
**Integration points:** <list>
**Port or greenfield:** <port from X / greenfield>

## Dimension 4 — Design
**Navigation surface:** <page/tab/route>
**Signal DS primitives:** <name (level), name (level)>
**Entity states:** <state list>
**DS GAPs:** <name → blocker ticket #NNN>

## Dimension 5 — Testing
**BDD happy path:**
  Given <state>
  When <action>
  Then <outcome>
**Alternate flows:** <list>
**Error flows:** <list>
**Regression risk:** <list>

## Cross-dimensional conflicts
<conflict or "None detected">

## Open GAPs
<[GAP — owner, due Stage N] items, or "None">
```

### B. Stage 00 manifest

Write to: `~/claude-os/docs/superpowers/sdlc/<feature-slug>/00-feature-brief/_manifest.md`

```yaml
stage: "00 — Feature Brief"
feature: "<feature-slug>"
input_artifact: "-"
owner: "feature-brief skill"
started: "YYYY-MM-DD"
completed: "YYYY-MM-DD"
gate:
  passed: true   # set true only when: all 5 dimensions answered (or GAP-marked), no open cross-dimensional conflicts
  checklist:
    - item: "All 5 dimensions answered or GAP-marked"
      ok: true
      evidence: "00-feature-brief/<feature-slug>.md"
    - item: "Cross-dimensional conflicts resolved or deferred with owner"
      ok: true
      evidence: "See cross-dimensional conflicts section"
    - item: "DS GAP blocker tickets created"
      ok: true
      evidence: "<ticket URLs or 'no GAPs'>"
    - item: "Jira epic updated with TOPIC block"
      ok: true
      evidence: "<Jira issue URL>"
trigger_next: "Stage 00 manifest gate.passed: true → Stage 01 may open"
```

### C. Jira epic update

Update the Jira epic with the TOPIC classification block via `editJiraIssue`:

```
## TOPIC Classification

**Persona:** <from Dimension 1>
**Problem statement:** <pain from Dimension 1>
**FHIR binding:** <primary ResourceType> + <secondary>
**Signal DS primitives:** <named + hierarchy levels>
**Acceptance criteria:** <BDD from Dimension 5>
**Sprint-ready flag:** YES (if no open blockers) | BLOCKED (list blockers)
```

---

## Step 5 — Handoff

Report to the user:
```
Stage 00 complete for <feature-slug>.
  Brief:    ~/claude-os/docs/superpowers/sdlc/<feature-slug>/00-feature-brief/<feature-slug>.md
  Manifest: gate.passed = true
  Jira:     <epic updated>
  DS GAPs:  <N blocker tickets created / 0 GAPs>

Open GAPs requiring resolution before Stage 01:
  <list or "None — Stage 01 may open immediately">

Recommended next step: /brainstorming to begin synthesis (Stage 02 BRD).
```

---

## Rules

- **Never invent a FHIR ResourceType** — use only real R4 types. If unsure, propose the closest match and flag it as `[GAP — verify with Samer]`.
- **Never invent DS primitives** — only named exports from `@scripsteam/scrips-signal-ds`. Missing? Create a blocker ticket, not an invented primitive.
- **Vague answers are recorded as `[GAP — needs X]`** — not silently skipped and not invented.
- **Claimed-existing artifacts are verified, not trusted** — any "it already exists / it's merged / wiring verified" is checked against the live repo at `file:line` before being recorded. No `file:line`, no fact (Dimension 3, step 0).
- **Cross-dimensional conflicts must be resolved before gate.passed: true** — unless the conflict resolution is itself a deferred GAP with an owner and stage.
- **`gate.passed: true` requires all five dimensions answered** (or explicitly GAP-marked), all conflicts resolved or deferred.
- **This skill applies to everyone** — Samer running a product idea, Andrew implementing a ticket, Tariq building a component. Same ceremony, same gate.

## Integration

**Calls:**
- `getJiraIssue` — auto-populate from Jira epic
- `editJiraIssue` — write TOPIC classification block
- `gh issue create` — create DS GAP blocker tickets
- `fhir-architecture-advisor` (agent) — auto-route when the FHIR binding is contested or a FHIR-native resource is proposed as a non-FHIR store
- live-repo grep (`git log` + Read/Grep) — verify every claimed-existing artifact in Dimension 3 step 0

**Called by:**
- `skill-suggester.py` feature-brief gate (auto-fire when feature intent detected without Stage 00 manifest)
- Anyone starting a new feature

**Hands off to:**
- `brainstorming` → Stage 02 BRD synthesis (reads the brief as input)
- `sdlc-handoff` → validates Definition of Ready before Stage 07 implementation

**Origin:** 2026-06-12 — Samer: the meta problem is that it's cognitively hard for anyone to hold all five dimensions (product, security, development, design, testing) when transitioning from idea to execution. Stage 00 is the entry ceremony that does this for every feature, for everyone.

**Hardening 2026-06-13** — after a live dogfood run against the consent-form-builder plan, three gaps were closed: (1) Dimension 3 now runs **claim-first** (verify "exists/merged/verified" against the repo before recording it — the run found 3 of 5 status checkmarks were false); (2) added a **platform-duplication** cross-check (the run's separate consent builder duplicated Template Studio / ADR-PROTO-010, which the original conflict table would have missed); (3) added a **regulatory-sufficiency** cross-check + `fhir-architecture-advisor` auto-route (canvas-only signature vs QES under DHA ST-09). Evidence: `~/claude-os/artifacts/2026-06-13-stage00-consent-builder-simulation.html`.
