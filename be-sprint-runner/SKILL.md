---
name: be-sprint-runner
description: Use to execute an autonomous Scrips backend (.NET) sprint. Reads stories from Jira, codes each story against the live BE codebase, runs unit + integration tests, runs security review, opens PR, notifies reviewers. Mirror of admin-sprint-runner for backend work. Use when the sprint contains .NET / Identity / API / FHIR / EF Core stories that scrips-react cannot deliver.
---

# Backend Sprint Runner

Autonomous execution of a Scrips backend (.NET) sprint. Zero human input during the sprint. Human review only at the PR gate.

**Announce at start:** "Running be-sprint-runner for Sprint [N], target repo: [Scrips.<service>]."

---

## Outcome Tracking (MANDATORY)

**At start — RECALL:** Before Step 1, invoke `agent-outcome-tracker` RECALL:
- Query `agent_traces` where `agent_skill = 'be-sprint-runner'`, last 10 rows
- Recall brain for `"backend sprint .NET identity coding"` + the target repo name
- Declare adjustments in one line before proceeding

**At end — CAPTURE:** After Step 5, invoke `agent-outcome-tracker` CAPTURE with:
- `task_type`: `sprint-execution`
- `agent_skill`: `be-sprint-runner`
- `jira_issue`: epic key
- `feature_slug`: sprint-[N]-be
- Score based on: stories completed / planned, retry count, security findings, build failures

**Per-story capture:** After each story completes, capture a row with:
- `task_type`: `jira-story-to-be-code`
- `jira_issue`: DEV-XXXX
- Score 5 if first-pass clean, 3 if rework needed, 1 if blocked

---

## Team + Review Gates

| Person | Role | Reviews |
|---|---|---|
| **Samer** | Founder — final approval | Sprint gate, security sign-off |
| **Andrew** | Backend (.NET) — primary BE reviewer | Code review on every BE PR |
| **Manish** | DevOps (Azure) | Required if sprint touches deployment, secrets, or infra |
| **Toufic** | Mirth / integration | Required if sprint touches HL7, FHIR adapter, Aidbox connect |

**Sprint PR reviewers:** Andrew (primary) + Samer (required). Add Manish/Toufic if sprint scope warrants.

---

## Sources of Truth (Priority Order)

When implementing any BE story, consult in this order:

1. **The live codebase** — `~/scrips-repos/Scrips.<service>/` is authoritative. Before writing new code, grep for existing patterns in the same controller / handler / repository.
2. **Stage 02 artifacts** if the story comes from the SDLC pipeline:
   - `~/claude-os/docs/superpowers/sdlc/<feature>/02-flow/api-contract.md` — endpoint specs (E1, E2, …)
   - `~/claude-os/docs/superpowers/sdlc/<feature>/02-flow/state-machine.md` — invariants
   - `~/claude-os/docs/superpowers/sdlc/<feature>/02-flow/gaps.md` — locked decisions
3. **Confluence BRDs** — search via Confluence MCP, space: SCRIPS DEVELOPMENT
4. **ISMS-005** — security/compliance floor for password, lockout, hashing, auth
5. **Jira story** — acceptance criteria, endpoint contracts, DB shape
6. **Brain** — `mcp__open-brain__search_brain` for prior decisions on the same module

**When sources conflict:** live code wins for what *is*. Stage 02 + ISMS-005 win for what *should be* (the gap). Document the gap as the work the story is doing.

---

## Repo Map

| Service | GitHub | Local path |
|---|---|---|
| Scrips.Identity | `Scripsteam/Scrips.Identity` | `~/scrips-repos/Scrips.Identity` |
| Scrips.Organization | `Scripsteam/Scrips.Organization` | `~/scrips-repos/Scrips.Organization` |
| Scrips.AppointmentScheduling | `Scripsteam/Scrips.AppointmentScheduling` | `~/scrips-repos/Scrips.AppointmentScheduling` |
| Scrips.PracticeManagement | `Scripsteam/Scrips.PracticeManagement` | `~/scrips-repos/Scrips.PracticeManagement` |
| Scrips.Notifications | `Scripsteam/Scrips.Notifications` | `~/scrips-repos/Scrips.Notifications` |
| Scrips.Common | `Scripsteam/Scrips.Common` | `~/scrips-repos/Scrips.Common` (event contracts only — touch carefully) |
| Scrips.OrganizationOnboarding | `Scripsteam/Scrips.OrganizationOnboarding` | `~/scrips-repos/Scrips.OrganizationOnboarding` |
| Scrips.Administration.Organization | `Scripsteam/Scrips.Administration.Organization` | `~/scrips-repos/Scrips.Administration.Organization` |

(Full inventory in `~/scrips-repos/`. Other services exist; add to this table if the sprint targets them.)

**NEVER commit to:** `main`, `develop`, or any release branch directly. Always work on the sprint branch.

**Cross-service changes:** if a single story requires edits in 2+ services, open one PR per service (linked in description). Do not co-mingle service changes in a single PR — review burden + revert blast radius.

---

## Sprint Execution Process

### Step 1: Setup

```
1. Fetch Jira stories: label = be-sprint-[N] OR explicit list provided in invocation
2. Identify target service(s) from story descriptions / acceptance criteria
3. For EACH target service, create a git worktree:
   ~/scrips-repos/Scrips.<service>-sprint-[N]
   Branch: feature/be-sprint-[N]-<service>
4. Read referenced Stage 02 artifacts (api-contract.md, gaps.md) for every story that links them
5. Create TodoWrite with all stories grouped by target service
```

### Step 2: Per Story Execution

For each story, in this order: **security-debt P0 stories FIRST** (G10-style backdoor removals, anonymous endpoints), then features, then cleanups.

```
1. Transition Jira story → "In Progress"
2. Read story description + ACs + linked Stage 02 references in full
3. Grep the live codebase for the target file/endpoint/handler — UNDERSTAND existing patterns before writing
4. If story is non-trivial (>50 LOC change OR touches >2 files):
   Invoke: writing-plans → save to docs/superpowers/plans/[story-key]-be-plan.md
5. Invoke: subagent-driven-development to execute plan
   - Each subtask: TDD-style (write or extend xUnit/NUnit test first if test infra exists)
   - Implement
   - Self-review against ACs
   - Commit. Format: "[DEV-XXXX] brief description"
6. Run local build + test:
   - `dotnet build` — must succeed, zero new warnings
   - `dotnet test` — must succeed, zero failing tests
   - For tests touching Identity/auth: `dotnet test --filter Category!=Integration` if integration tests need a DB; otherwise full
7. Invoke: review (staff engineer review)
8. Invoke: scrips-security-audit (BE security pass — OWASP, STRIDE, NABIDH, ISMS-005 if applicable)
9. Resolve all review + security findings; re-test
10. **Step 6.5 — Jira transition path:** Project workflow may not have direct "In Progress → Done". Verified 2026-04-26: PROD project workflow path is `In Progress → Code Review → Done`. Use `getTransitionsForJiraIssue` first to discover actual transitions; do NOT hardcode IDs. Walk the workflow gracefully.
11. **Step 6.6 — WIP-PR fallback (when stuck):** If after 3 attempts a build/test still fails OR you've used >50% of available execution budget:
    - Commit WIP (`git add -A && git commit -m "[WIP — see PR body] DEV-XXXX"`)
    - Push branch + open DRAFT PR with title prefix `[WIP]` and body listing failing tests + reason for stopping
    - Transition Jira to Code Review with comment about blocking issues
    - Report back with draft PR URL — NEVER lose work to a turn cutoff
12. All issues resolved → Transition Jira story along the workflow's actual transition path
```

### Step 2.5: Pre-worktree default-branch verification (mandatory)

Before creating any worktree:
```
gh repo view Scripsteam/Scrips.<service> --json defaultBranchRef
```
Use the returned default branch (`master` for `Scrips.Identity` as of 2026-04-26 — NOT `main`). Create worktree explicitly based on `origin/<defaultBranch>`:
```
git worktree add ~/scrips-repos/Scrips.<service>-sprint-[N] -b feature/be-sprint-[N]-<service> origin/<defaultBranch>
```
Without `origin/<defaultBranch>`, the worktree may inherit the parent's checked-out branch — usually wrong.

### Step 3: Sprint security + compliance pass

After all stories complete:

```
1. Full test suite per touched service: `dotnet test` — must be 100% green
2. Invoke: scrips-security-audit at sprint scope (looks across stories for cumulative effect — e.g., did we introduce a new auth surface?)
3. Fix any P0/P1 findings; re-test
4. Verify ISMS-005 invariants if sprint touched auth/identity:
   - Password policy: RequiredLength≥12, complexity, lockout=10
   - JWT claims: ns=1 preserved on user creation
   - No new [AllowAnonymous] without justification + rate limit
5. If sprint introduced new EF Core migrations:
   - Andrew gate: explicit approval before opening PR
   - Migration script reviewed for downgrade-safety
```

### Step 4: Ship

```
1. Per service worktree:
   a. Sync branch with origin/main; resolve conflicts deliberately
   b. Run final `dotnet build && dotnet test`
   c. Open PR via gh CLI:
      gh pr create \
        --title "BE Sprint [N] / Scrips.<service> — [scope]" \
        --reviewer Scripsteam/Andrew,Scripsteam/Samer \
        --body "$(...)"
   d. PR description must include:
      - Sprint goal achieved (per service slice)
      - Stories completed (Jira links)
      - Files changed summary
      - Test pass count
      - Security review sign-off (scrips-security-audit output summary)
      - Migration impact if any
      - Rollback plan if any [Authorize] / endpoint-shape changes
2. Add Manish to reviewers if sprint scope includes deployment/infra/secrets
3. Add Toufic to reviewers if sprint scope includes HL7/FHIR adapter changes
4. Post Slack notification in #dev-backend (or #dev-admin if no BE channel exists): "BE Sprint [N] PR(s) ready: [links]"
```

### Step 5: Post-Sprint

```
1. Post sprint summary comment on parent Jira epic
2. Invoke: retro → save output to docs/superpowers/retros/be-sprint-[N]-retro.md
3. If sprint closed any items in `~/claude-os/docs/superpowers/sdlc/<feature>/02-flow/gaps.md`:
   - Update gap status to status-shipped + link the merged PR
4. Update Stage 02 artifacts if implementation revealed contract drift from api-contract.md
```

---

## .NET / Identity Rules (enforced per story)

- **Auth defaults:** every new endpoint is `[Authorize]` unless story explicitly justifies `[AllowAnonymous]` + adds rate-limit + adds an audit log entry
- **No string concatenation in SQL.** Use EF Core parameterized queries or Dapper with parameters
- **JWT claims:** if user creation is touched, verify `TenantId="100"` is set so `ns=1` claim fires (per `ScripsProfileService.cs`); otherwise React port rejects the user
- **Identity options:** if story touches `AddIdentity()` config, lockout=10, RequiredLength=12 are the floors per ISMS-005 §6.2
- **Event publishing:** every `IIntegrationEvent` published must have a documented consumer (verified in `Scrips.<consumer>/Startup.cs` Subscribe call). No fire-and-forget.
- **Tenant isolation:** every repository query must filter by `TenantId` from the JWT, never from a request body / URL param
- **No PII in logs.** Email, phone, name → masked. Password / token / SSN → never logged at any level.
- **DI registration:** new services registered in `Startup.cs` `ConfigureServices` AND verified resolvable via integration test that boots the host

---

## Code Quality Gates (enforced before every commit)

- `dotnet build`: zero errors, zero new warnings (existing warnings tolerated; do not silence)
- `dotnet test`: 100% pass on touched test projects; coverage threshold per existing config
- No new `using static` of broad namespaces
- No `Result.Result` / `.Wait()` synchronous-over-async (use `await`)
- No commented-out code
- No `TODO` without an attached Jira ticket reference

---

## When to Stop and Notify Samer

Stop the sprint and send Samer a Slack DM if:
- Story requires a DB migration whose downgrade path isn't safe (data-destructive)
- ISMS-005 violation found in a story not scoped to fix it (out-of-scope security debt)
- A required dependency service (e.g., Notifications, Common) needs a coordinated change Andrew has not approved
- Two stories in a row fail security review after 3 fix attempts
- Cross-service event contract change (touches `Scrips.Common`) without prior Andrew approval

**Do NOT stop for:** missing test data (use in-memory or test container), failing build (fix it), failing test (fix it), warnings (fix them), missing config (use appsettings.Development.json defaults).

---

## Integration

**Required skills:**
- `writing-plans` — before each non-trivial story implementation
- `subagent-driven-development` — story execution engine
- `using-git-worktrees` — isolated sprint workspace per service
- `verification-before-completion` — before marking any story done
- `review` — after each story
- `scrips-security-audit` — after each story AND once per sprint (cumulative pass)
- `ship` — sprint completion (one invocation per service worktree)
- `retro` — sprint retrospective

**NOT required (these are FE-only):**
- `design-review` — no UI surfaces in BE
- `qa` (preview-server-based) — replaced by `dotnet test` + integration tests + (where appropriate) Postman/curl smoke
- `brainstorming` — most BE stories have specs; brainstorm only when implementation approach is genuinely ambiguous
