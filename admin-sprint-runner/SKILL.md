---
name: admin-sprint-runner
description: Use to execute an autonomous Scrips Admin React sprint. Reads stories from Jira, codes each story against the three-layer source of truth, runs QA and security review, opens PR, notifies reviewers.
---

# Admin Sprint Runner

Autonomous execution of a Scrips Admin React V1 sprint. Zero human input during the sprint. Human review only at the PR gate.

**Announce at start:** "Running admin-sprint-runner for Sprint [N]."

---

## Outcome Tracking (MANDATORY)

**At start — RECALL:** Before Step 1, invoke `agent-outcome-tracker` RECALL:
- Query `agent_traces` where `agent_skill = 'admin-sprint-runner'`, last 10 rows
- Recall brain for `"admin sprint react jira story coding"`
- Declare adjustments in one line before proceeding

**At end — CAPTURE:** After Step 5, invoke `agent-outcome-tracker` CAPTURE with:
- `task_type`: `sprint-execution`
- `agent_skill`: `admin-sprint-runner`
- `jira_issue`: DEV-2270 (parent epic)
- `feature_slug`: sprint-[N]
- Score based on: stories completed / stories planned, retry count, security issues found

**Per-story capture:** After each story completes (step 10 in Step 2), capture a row with:
- `task_type`: `jira-story-to-code`
- `jira_issue`: DEV-XXXX
- Score 5 if first-pass clean, 3 if rework needed, 1 if blocked

---

## Team + Review Gates

| Person | Role | Reviews |
|---|---|---|
| **Samer** | Founder — product + design | Sprint gate UAT (staging), final approval |
| **Andrew** | Backend (.NET) | Backend FHIR tickets, auth fixes, PR backend review |
| **Toufic** | Mirth / integration | FHIR integration tickets, HL7 mapping, Aidbox connect |
| **Manish** | DevOps (Azure) | Infrastructure, CI/CD, deploy tickets, Azure config |

**Sprint PR reviewers:** Samer + Andrew (required). Manish required if sprint contains DevOps tickets. Toufic required if sprint contains FHIR integration tickets.

---

## Sources of Truth (Priority Order)

When implementing any screen or component, consult in this order:

1. **Figma** — `8YhKao7Q62LXnMnrsVsW3C` (Organisation 2.0.2) — use Figma MCP `get_design_context`
2. **Axure prototype** — 17 screens, exported HTML at `~/Downloads/` (Samer's Mac) or committed to `docs/design/axure/` if exported
3. **Confluence BRDs** — search via Confluence MCP, space: SCRIPS DEVELOPMENT
4. **Flutter admin code** — `github.com/Scripsteam/` (reference for business logic only — do NOT copy Flutter patterns into React)
5. **Jira story** — acceptance criteria and API surface defined in the ticket
6. **Spec doc** — `docs/superpowers/specs/2026-04-13-admin-react-v1-design.md`

**When sources conflict:** Figma wins for visual/layout. Confluence wins for business rules. Spec doc wins for architecture decisions.

---

## Repo Map

| Repo | GitHub | Local path | Purpose |
|---|---|---|---|
| Frontend (target) | `Scripsteam/scrips-react` | `~/scrips-repos/scrips-react` | Admin module being built here |
| Flutter admin (reference) | `Scripsteam/` (check org) | `~/scrips-repos/` | Business logic reference ONLY |
| .NET backend (reference) | `Scripsteam/` (check org) | `~/scrips-repos/` | API contracts, auth patterns |
| This OS repo | `samertad/claude-os` | `~/claude-os` | Skills, specs, agent config |

**NEVER commit to:** `main` or `develop` branches directly. Always work on sprint branch.

---

## Sprint Execution Process

### Step 1: Setup

```
1. Fetch Jira stories: label = admin-sprint-[N], parent = DEV-2270
2. Create git worktree: ~/scrips-repos/scrips-react-sprint-[N]
   Branch: feature/admin-sprint-[N]
3. Read spec doc in full: docs/superpowers/specs/2026-04-13-admin-react-v1-design.md
4. Create TodoWrite with all stories
```

### Step 2: Per Story Execution

For each story, in Jira priority order:

```
1. Transition Jira story → "In Progress"
2. Read story description + acceptance criteria in full
3. Consult sources of truth (Figma first for UI, Confluence for rules)
4. Invoke: brainstorming (for UI stories)
5. Invoke: writing-plans → save to docs/superpowers/plans/[story-key]-plan.md
6. Invoke: subagent-driven-development to execute plan
   - Each subtask: TDD (test first), implement, self-review, commit
   - Commit message format: "[DEV-XXXX] brief description"
7. Invoke: review (staff engineer review)
8. Invoke: qa (QA lead — find bugs, fix, regression test)
9. For UI stories: Invoke design-review (visual quality gate vs Figma)
10. All issues resolved → Transition Jira story → "Done"
```

### Step 3: Sprint QA

After all stories complete:

```
1. Run full test suite: npm run test (must be 100% green)
2. Invoke: cso (security review — OWASP + tenant isolation checklist)
3. Fix any security issues found
4. Invoke: benchmark (performance baseline)
```

### Step 4: Ship

```
1. Invoke: ship
   - Syncs branch, audits coverage, runs final tests, opens PR
2. PR title: "Admin Sprint [N] — [Sprint goal]"
3. PR description must include:
   - Sprint goal achieved
   - Stories completed (Jira links)
   - Test coverage summary
   - Security review sign-off
   - Screenshots of key screens (from design-review)
   - Samer UAT checklist (copy from S5.7 ticket for Sprint 5)
4. Request reviewers: Samer, Andrew (+ Manish/Toufic if applicable)
5. Post Slack notification in #dev-admin channel: "Sprint [N] PR ready for review: [link]"
```

### Step 5: Post-Sprint

```
1. Post sprint summary comment on DEV-2270 (Jira epic)
2. Invoke: retro → save output to docs/superpowers/retros/sprint-[N]-retro.md
3. Invoke: document-release → update Confluence sprint report page
4. Update spec doc if any decisions changed during sprint
```

---

## FHIR Rules (enforced per story)

- All API calls in `src/services/admin/` — never Axios directly from components
- Organization, Practitioner, PractitionerRole, Location always use FHIR R4 TypeScript interfaces from `src/services/admin/fhir/types.ts`
- Until Sprint 3 FHIR endpoints are live: route through `scripsAdapter.ts`
- After Sprint 3: adapter is bypassed — services call `/fhir/` endpoints directly
- Never expose `.tenantId` or `.orgId` in URL params — always from JWT claims

---

## Code Quality Gates (enforced before every commit)

- TypeScript strict mode: zero type errors
- ESLint: zero warnings
- No `any` types
- No hardcoded hex colors (use design tokens)
- No direct Axios calls from components
- No commented-out code
- Test coverage: every component renders, every form validates, every API call mocked

---

## When to Stop and Notify Samer

Stop the sprint and send Samer a Slack DM (U...) if:
- Figma file inaccessible and a UI story cannot proceed
- Backend API endpoint returns unexpected shape blocking a story
- Security review finds a Critical issue that requires backend fix
- Two stories in a row fail spec review after 3 fix attempts
- Andrew needs to merge a backend change before a frontend story can complete

**Do NOT stop for:** missing test data, missing env vars (use MSW mocks), TypeScript errors (fix them), lint warnings (fix them).

---

## Integration

**Required skills:**
- `brainstorming` — before any UI component
- `writing-plans` — before each story implementation
- `subagent-driven-development` — story execution engine
- `using-git-worktrees` — isolated sprint workspace
- `verification-before-completion` — before marking any story done
- `review` — after each story
- `qa` — after each story (UI stories)
- `design-review` — after each UI story (Figma fidelity check)
- `cso` — once per sprint, before ship
- `ship` — sprint completion
- `retro` — sprint retrospective
