---
name: port-spec
description: Engineering-side port specification for redesigning a feature with a live implementation (Flutter / Razor / Vue → React). Runs a 5-parallel-subagent discovery (Figma A, Figma B, Backend, Confluence+brain, LIVE FE audit) and produces flow.md + state-machine.md + api-contract.md + gaps.md + a Stage 03 review packet. Shares Stage 01 sources with /synth — whichever runs first writes sources.md, the second reuses it. Use when porting a live feature to a new platform, NOT for greenfield (use /synth).
---

# /port-spec — Live System → Port Specification Skill

**Announce at start:** "Running port-spec on feature: `<feature-slug>`."

Engineering-side counterpart to `/synth`. Where synth produces a product BRD (personas, journeys, ACs), port-spec produces an **engineering port specification** — the artifact a developer needs to rebuild a feature on a new platform without inventing behavior.

---

## Why this skill exists

Most Scrips features have THREE truths and they disagree:

1. **Live FE** (Flutter `scrips_admin`, Razor `Scrips.SuperAdmin`, etc.) — knows what the BE actually accepts, what fields get stripped pre-POST, what validation runs client-side, what error states are recoverable.
2. **Backend code** — knows what gets persisted, what events fire, what auth (or lack thereof) protects each endpoint.
3. **Figma redesign** — knows what the next-gen UI should look like, often differs from live in step count / field names / multi-entity support.

If you write a port spec from Figma alone, you invent BE contracts. If you write it from BE alone, you miss the field-stripping and validation rules. If you write it from the live FE alone, you miss the redesign target. **You need all three.**

The organization-onboarding pilot (2026-04-24/25) proved this: Flutter audit revealed that legacy `POST /api/Organization` accepts ONE admin only — Figma's multi-admin Step 5 was net-new BE work, not a UI exercise. Without the Flutter pass, that gap is invisible until QA.

---

## When to use this skill

- Porting a feature from one frontend platform to another (Flutter → React, Razor → React, Vue → React, etc.)
- Building a "second client" against an already-live backend
- Reverse-engineering any feature where the design is a REDESIGN of an existing live system
- Before any Stage 04 ticket-writing for a feature that has prior live implementations

## When NOT to use this skill

- Greenfield features with no live implementation → use `/synth` instead
- Pure UI redesigns of an already-React feature → use `/design-sync`
- Backend-only changes → write a normal engineering note
- Internal tooling decisions where Retool / manual operation is appropriate (see Decision Gates step below — exit early if scope is internal-only at pre-revenue)

---

## Inputs

- **Feature slug** (e.g., `organization-onboarding`, `practitioner-association`)
- **Figma URL or selection** in active Figma document
- Optional: **Axure URL** or local export path
- Optional: pointer to live FE repo path (if not auto-discoverable from `~/scrips-repos/`)

---

## Outputs

```
docs/superpowers/sdlc/<feature-slug>/
├── 01-raw-sources/
│   ├── _manifest.md
│   ├── sources.md                    ← top-level index + N constraints
│   ├── figma-part-a.md               ← per-subagent
│   ├── figma-part-b.md               ← if >12 frames in scope
│   ├── backend.md                    ← controllers, endpoints, DB, events, auth gaps
│   ├── confluence-brain.md           ← BRDs + brain memos
│   └── flutter-reference.md          ← LIVE FE audit (or razor-/angular-/vue-reference.md)
└── 02-flow/
    ├── _manifest.md
    ├── flow.md                       ← click-by-click FE/BE per screen
    ├── state-machine.md              ← mermaid + invariants
    ├── api-contract.md               ← endpoints, DTOs, validation, file layout
    └── gaps.md                       ← gaps with owner + priority + sequencing
```

**Key differentiator vs synth:** synth produces a BRD (`02-brds/<feature>.md`). port-spec produces engineering specs (`02-flow/*.md`) — different audience, different artifact shape. The two skills can run on the same feature; sources are shared.

---

## Process

### Step 0 — Bootstrap

```
mkdir -p ~/claude-os/docs/superpowers/sdlc/<feature-slug>/{01-raw-sources,02-flow}
```

Write both `_manifest.md` files with `started: <ISO>`, `passed: false`.

### Step 0.5 — Reuse existing sources if present

If `01-raw-sources/sources.md` already exists from a prior `/synth` or `/port-spec` run on the same feature, READ it instead of re-discovering. Check:

- Does every source row in `sources.md` have content or an explicit `[SOURCE UNAVAILABLE]` marker?
- Does it include a `flutter-reference.md` (or razor-/vue-reference.md) row? port-spec requires the live FE audit.

If yes → skip to Step 3. If the live-FE row is missing → run ONLY Subagent E (live FE audit) and append to `sources.md`. If the file is stale (>14d) or partial → re-run Step 1 in full.

### Step 1 — Discover sources (Stage 01) — DISPATCH 5 PARALLEL SUBAGENTS

In a single message with 5 parallel `Agent` calls:

**Subagent A — Figma part 1**
- Tools: `mcp__claude_ai_Figma__get_metadata`, `get_design_context`, `get_screenshot` (or `figma-console` equivalents)
- Task: First half of frames in scope. Per frame: nodeId, frame name, components, transitions, screenshot path.
- Save screenshots to `01-raw-sources/figma-screenshots/`

**Subagent B — Figma part 2**
- Same tools as A
- Task: Second half of frames. Split when scope >12 frames.

**Subagent C — Backend audit**
- Tools: Glob, Grep, Read on `~/scrips-repos/Scrips.*` repos
- Task: For each surface in the Figma scope, locate the controllers + endpoints. Return:
  - Controller path + line numbers
  - Request body shape, response shape
  - DB tables touched, schema details
  - Events published (Dapr / RabbitMQ / signalR)
  - Auth attributes (`[Authorize]`, `[AllowAnonymous]`, claim policies)
  - Known gaps (anonymous endpoints, missing policies, swallowed exceptions)

**Subagent D — Confluence + brain**
- Tools: `searchConfluenceUsingCql`, `getConfluencePage`, `mcp__open-brain__search_brain`, `recall_related`
- Task: Search SCRIPS DEVELOPMENT space + brain for BRDs, prior decisions, persona references, compliance constraints. Return titles + relevant excerpts.

**Subagent E — Live FE audit (THE NEW STEP vs synth)**
- Tools: Glob, Grep, Read on `~/scrips-repos/scrips_admin/` (Flutter), `~/scrips-repos/Scrips.SuperAdmin/` (Razor), `~/scrips-repos/scrips-react/` (existing React features), or whatever live implementation exists
- Task: Find the equivalent screen/route in the live repo. Extract:
  - **Screen/widget paths** with line numbers
  - **State management** (BLoC/Cubit/Provider/Redux/etc.) with state class + events/emissions
  - **API client paths** mapping each call to its endpoint
  - **Validation rules** lifted VERBATIM from the state-handler code (e.g. `CreateButtonEnableEvent` handler)
  - **Field-stripping patterns** before POST (very common, easy to miss)
  - **Error handling** including partial-failure recovery paths
  - **Route/navigator setup** (push/pop, named routes, PageController, etc.)
  - **What the live FE does NOT have** that Figma adds — this becomes net-new scope

If no live FE exists, write `[NO LIVE FE — net-new feature; consider running /synth instead]` and continue with 4 sources.

### Step 2 — Stitch sources.md (Stage 01)

Index of sources + N top-line constraints surfaced across them. Sample constraints to look for:
- Multiple parallel BE paths for the same conceptual operation
- Auth gaps (anonymous endpoints, missing policies)
- DB schema typos / legacy columns
- Two-phase save patterns
- Events with empty no-op handlers
- Live-vs-redesign delta (e.g. "Figma adds N admins; legacy supports 1")

Mark Stage 01 manifest `passed: true` only when every source is non-empty or has explicit `[SOURCE UNAVAILABLE — <reason>]`.

### Step 3 — Stage 02 deliverables (SERIAL, in this order)

#### 3a. flow.md — click-by-click per screen

Format per screen:

```markdown
## Screen N — <name> (Figma nodeId `<id>` | Live FE `<file:line>`)

### FE
- Route: `<path>`
- Components: <list>
- Validation: <rules — lift verbatim from live FE state-handler if present>
- State transitions: <on-change behavior>

### BE
- Endpoint(s): `<METHOD> <path>` → `<controller>:<line>`
- Request body: <shape>
- Side effects: <DB writes, events, downstream calls>
- Failure modes: <error responses + how live FE handles them>
```

End with summary tables: endpoints, events, DB writes ordered by happy-path.

#### 3b. state-machine.md — mermaid + invariants

At minimum:
- **Wizard/step machine** (or feature-equivalent navigation graph)
- **Per-entity lifecycle** (one per major entity touched — Organization, Admin, Invitation, etc.)
- **Composite happy-path sequence diagram** (actor → frontend → BE → DB → event → consumer)
- **Invariants table** — hard rules that must hold across all states, with column for "Enforced by" (DB constraint / FE-only / not enforced — the last is a gap)

State machines often surface gaps the per-screen flow.md missed (e.g. ambiguous step semantics, dangling states without inbound/outbound transitions).

#### 3c. api-contract.md — engineering port contract

- **Endpoint inventory table** — columns: endpoint, method, service, auth, used by live FE? (Y/N), action for port (use / skip / extend)
- **Per-endpoint OpenAPI-style spec** — request body shape (verbatim from live FE), response shape, side effects, error modes, port file anchor
- **TypeScript DTOs** lifted from live source (model files in Flutter / DTO classes in .NET)
- **Validation rules** — quote the state-handler verbatim, file:line cited
- **Partial-failure matrix** — scenario × current BE behavior × port-side mitigation
- **Proposed file layout** for the port (folder tree)

#### 3d. gaps.md — consolidated gaps with owner + priority

Per-gap fields:
- ID (G1, G2, ...)
- Type: BE / FE / PRD / INF
- Where: file:line or system reference
- Impact: 1-2 sentences
- Resolution: option A vs B if applicable, with rationale
- Decision-required flag for human gates

End with:
- **By-owner summary table** — BE / FE / PRD / INF, prioritized
- **Recommended sequencing** — week-by-week or phase-by-phase
- **Decision gates** flagged separately for human review

### Step 3e — Stage 03 review packet

After `gaps.md` is written, emit `03-review/stage-03-packet.md` in the SDLC folder. This is what Samer reviews at PIPELINE.md Stage 03 — a single document that aggregates everything humans need to decide before Stage 04 ticket-writing.

```bash
mkdir -p ~/claude-os/docs/superpowers/sdlc/<feature-slug>/03-review
```

Sections (in this order):

1. **Pipeline run summary** — slug, mode (redesign-port / greenfield), sub-skills run, started/completed timestamps.
2. **Decision gates requiring Samer review** — every gap with `decision-required: true` from `gaps.md`. Per gate: options A/B/C, recommended option, blast-radius commentary, what blocks if unresolved.
3. **Open gaps by owner** — BE / FE / PRD / INF, prioritized.
4. **DS coverage summary** — only if `02-design/ds-audit.md` exists from a parallel `/design-sync` run. % DS components, new patterns flagged, token drift.
5. **BRD spot-check** — only if `02-brds/<feature-slug>.md` exists from a parallel `/synth` run. List of `[GAP]` and `[DRAFT]` markers needing source resolution.
6. **Recommended next steps** — usually one of:
   - "Resolve N decision gates with Samer; then run `/sprint plan`."
   - "BE hardening sprint first (G1, G2, …); React sprint depends on BE."
   - "Defer entirely — internal-only scope at pre-revenue. Manual provisioning suffices."
7. **What was NOT decided** — explicit list of items left open by design.

Write `03-review/_manifest.md` with `passed: true` once the packet is written.

### Step 4 — Decision gates (BEFORE Stage 04 ticket-writing)

For any gap of type PRD or "platform decision," explicitly flag:
- Decision required
- Options A / B / C with rationale
- Recommended option with reasoning
- BLOCK ticket-writing until human resolves

**Common decision gates seen in practice:**
- BE endpoint extension: option A (extend existing) vs option B (new endpoint) vs option C (client-side compose)
- Platform choice: React vs Retool vs defer-entirely (especially for SSA/internal tools at pre-revenue stage)
- Multi-entity semantics (e.g. "is this list one-thing-many-fields or many-things")

**At pre-revenue stage with SSA/admin scope, default to "defer entirely + manual provisioning" until the journey stabilizes** — see organization-onboarding pilot for reasoning.

### Step 5 — Quality gates

- [ ] Every claim in flow.md traces to a source file
- [ ] Live FE file paths cited per screen (when live FE exists)
- [ ] Validation rules lifted VERBATIM, not paraphrased
- [ ] Field-stripping patterns documented if live FE strips
- [ ] Every endpoint in flow.md appears in api-contract.md
- [ ] Every gap in flow.md/state-machine.md appears in gaps.md
- [ ] Decision gates explicitly flagged with recommended options
- [ ] Both _manifest.md files marked `passed: true` only when all checks above pass

If any check fails, fix or mark `[GAP — <reason>]`. Never mark passed silently.

---

## Hard rules (non-negotiable)

1. **Live FE first.** When a live implementation exists, it is the AUTHORITATIVE source for BE contract behavior. Figma alone lies about field shapes, error states, and edge cases.
2. **Validation rules are quoted, not paraphrased.** Lift from BLoC / Redux / Cubit / state-handler code verbatim with file:line citations. Paraphrasing introduces drift.
3. **Field-stripping patterns are part of the contract.** When the live client strips fields before POSTing (Flutter scrips_admin does this on tab 0 + tab 1), document the EXACT strip list. The BE may not enforce these rules itself but the contract requires them.
4. **Two-phase saves are intentional unless proven otherwise.** Don't simplify them in the port without verifying the BE accepts a single-phase variant.
5. **Decision gates before ticket-writing.** Platform choice (Retool / React / defer), endpoint extension (A/B), product semantics — all flagged before splitting into Sprint tickets. Rationale must be in `gaps.md`.
6. **No fiction.** Every claim has a source or an explicit `[GAP]` / `[DRAFT]` marker. Same rule as `/synth`.
7. **Pre-revenue scale changes the calculus.** Internal tooling at 0 customers should default to manual / Retool, not React. Re-evaluate at customer-count threshold (~15+) or journey-stability threshold (3+ months unchanged).

---

## Skill dependencies

- Figma Console MCP (`figma-console` namespace) or Figma MCP (`Figma` namespace) — frame reads + screenshots
- Atlassian MCP — Jira + Confluence
- open-brain MCP — prior decisions + memos
- Local filesystem read for live FE audit (Glob, Grep, Read on `~/scrips-repos/`)
- Agent tool — 5 parallel subagents in Stage 01

## Outcome tracking (mandatory)

- **Start (RECALL):** Query brain for `<feature-slug> port-spec OR engineering-spec`. Note prior failures.
- **End (CAPTURE):** Score 5 if all 5 source subagents returned content + decision gates resolved; 3 if any source unavailable; 1 if any quality gate failed. Tag `[SKILL: port-spec]` in commit + activity log.

## Attribution tag

`[SKILL: port-spec]` — required in commits, activity log entries, and frontmatter `attribution:` of every file produced.

---

## Lessons learned (from organization-onboarding pilot 2026-04-24/25)

1. **Flutter audit was the highest-leverage source.** Without it, multi-admin would have been assumed BE-supported; field-stripping pattern would have been missed; country-immutability wouldn't have been flagged. Always do live-FE audit when one exists.

2. **Platform decision belongs at Stage 03, not as a tail-end gap.** When the question is "Retool vs React vs nothing," surface it BEFORE writing Sprint tickets — better yet, before writing the API contract — because it changes file layout and effort estimate.

3. **Pre-revenue scale changes the platform calculus.** SSA-style internal tooling at 0 customers should default to manual provisioning + maybe Retool, not React. The org-onboarding pilot ran through three platform decisions (React → React+Retool hybrid → defer entirely) before landing on the right answer.

4. **The live FE may BE the redesign target.** Sometimes Figma is a redesign of an existing live system; sometimes it's fresh. Detect which case you're in EARLY — it changes the synthesis approach. If redesign, the live FE is the BE contract anchor and Figma is the UI target. If fresh, no live-FE-audit subagent needed.

5. **State machines find gaps that flow.md alone misses.** Drawing the wizard machine surfaced the "Step 4 = contact address vs clinic locations" ambiguity (G11 in org-onboarding) that the per-screen flow doc had buried.

6. **Customer-facing surfaces stay in React; internal-facing surfaces don't.** Even when deferring the SSA wizard, the set-password landing page (the FIRST screen a new admin sees of the brand) belongs in React + Signal DS. The boundary is "does the customer see it."
