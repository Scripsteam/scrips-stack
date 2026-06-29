---
name: backend-performance-audit
description: Systematically audit a backend repository (or a set of backend repos) for performance issues and produce a prioritized, deduplicated findings inventory ready to feed a fix phase. Use this whenever the user wants to find, list, hunt, or inventory performance problems, bottlenecks, slow endpoints, N+1 queries, slow database access, scaling issues, or "what's making this slow" across one or more backend services — even if they don't say the word "audit." Also use when the user wants a triaged list of perf issues to fix later, a portfolio-level view across multiple backend repos, or a Claude Code-consumable brief of performance findings. Covers .NET/EF Core/ADO.NET/Dapper + SQL Server (first-class), Node/TypeScript, Python, Java, Go, and raw SQL.
---

# Backend Performance Audit

A grep-and-eyeball pass finds the obvious stuff and floods you with noise on the rest. The value of this skill is discipline: a fixed **taxonomy** of where backend latency actually comes from, a **detection method per category** that confirms before it reports, a **severity × confidence × hot-path** ranking so the list is actionable, and **deduplication** so forty instances of one anti-pattern become one batchable finding instead of forty line items. The deliverable is a ranked list you can hand straight to a fix phase.

## Core principles

- **Static analysis flags; it does not measure.** You are reading code, not profiling a running system. You can say "this is an N+1 that scales with row count," but you cannot say "this is *the* bottleneck." Never assert that a finding is the dominant cost without runtime evidence. Rank by likely impact and tell the user which top findings deserve confirmation against real telemetry (APM traces, SQL Server Query Store / `sys.dm_exec_query_stats`, slow-query logs) before any large rewrite.
- **Confirm before reporting.** A regex match is a *candidate*, not a finding. Read the surrounding code. A `.Result` in a one-shot startup task is not the same issue as a `.Result` in a request handler. Reading context is what keeps the false-positive rate low enough that the list stays trustworthy.
- **Group recurring patterns.** If the same root cause appears across many sites (e.g. controllers returning EF entities instead of projected DTOs), emit ONE finding with an instance count and representative locations — not one per site. The fix phase batches these.
- **Hot path dominates severity.** The same anti-pattern is Critical on a per-request handler and Low in a nightly migration script. Always estimate call frequency.
- **Don't break correctness chasing speed.** Especially in this codebase's domain (healthcare), flag any suggested change that could alter results, transaction semantics, or auditability as a risk rather than a clean win. `AsNoTracking` on a path that later writes, collapsing transactions, or changing read isolation are correctness changes, not free optimizations.
- **Never put secrets or patient/PII data in evidence snippets.** Redact connection strings, tokens, and any real identifiers (MRN, Emirates ID, names) when quoting code or query results.

## Workflow

Follow these steps in order. Steps 3–5 are the core loop; do them per category.

### 1. Scope and inventory

Determine what's in scope. If the user pointed at a single repo, that's the unit. If they said "all backend repos," establish the list — either repos already checked out under a parent directory, or an explicit list they provide. Do **not** clone or fetch repos on your own initiative; ask the user to make them available locally (or confirm a parent path) and operate on what's present.

For each repo, detect the stack so you load the right heuristics:

| Signal | Stack | Reference to load |
|---|---|---|
| `*.csproj`, `*.sln`, `Program.cs`, EF Core / Dapper packages | .NET | `references/dotnet.md` |
| `package.json` with express/nest/fastify/typeorm/prisma/sequelize | Node/TS | `references/node.md` |
| `*.sql`, stored procs, migrations, heavy raw SQL | SQL | `references/sql.md` |
| anything else, or to cover algorithmic/concurrency/caching regardless of stack | generic | `references/generic.md` |

A repo can match several (a .NET service with hand-written SQL → load `dotnet.md` **and** `sql.md`). Always also load `generic.md`. Read only the reference files you need.

### 2. Load detection heuristics

Read the relevant reference file(s). Each one carries the category-specific patterns, the ripgrep candidate queries, and the confirmation criteria for that stack. Don't proceed on memory — the patterns are tuned and the false-positive notes matter.

### 3. Find candidates

Run the scanner to get a fast, deterministic first pass:

```bash
python3 scripts/scan.py --repo <repo-path> --stack auto --out <repo>/candidates.jsonl
```

It emits one JSON object per candidate (`file`, `line`, `category`, `pattern`, `match`, `note`). It is deliberately high-recall and noisy — its job is to point you at code to read, not to decide. Supplement it with targeted reads wherever a category needs semantic understanding the scanner can't reach (e.g. "is this `await` inside a loop that could be `Task.WhenAll`?").

### 4. Confirm and classify

For each candidate, open the file and read enough context to decide. Discard false positives silently. For real issues, assign:

- **Category** — from the taxonomy below.
- **Severity** — Critical / High / Medium / Low (rubric below).
- **Confidence** — Confirmed (read it, it's real) / Likely (pattern strongly implies, context not fully verifiable) / Needs-review (heuristic, needs human judgment).
- **Hot path** — yes / no / unknown. Is this on a request path, a frequently-called service method, a per-row loop in a batch over large data? Trace callers when it's cheap to do so.
- **Estimated impact** — qualitative and honest: "scales linearly with appointments per clinic," "fixed ~50ms per call," "only on cold start."

### 5. Deduplicate and group

Before writing anything: collapse. Same root cause, many sites → one grouped finding with `instances: N` and 2–3 representative `file:line` locations. Distinct root causes stay separate even if they share a category. This is what makes the list fixable instead of overwhelming.

### 6. Prioritize

Rank findings by **severity**, breaking ties with **hot-path** then **confidence**. Confirmed Critical on a hot path is the top of the list; Needs-review Low micro-optimizations are the bottom. This ranked list is the primary output — it's the "list of issues to fix" the user asked for.

### 7. Emit the inventory

Produce both:
1. A human-readable report (markdown) — see structure below.
2. A machine-readable `findings.jsonl` (one record per finding) for Claude Code fix-phase handoff.

### 8. Multi-repo aggregation (only when scope is more than one repo)

Run steps 1–7 per repo, then merge: concatenate the `findings.jsonl` files, re-rank globally, and write a portfolio report that leads with a cross-repo summary table (repo × count by severity) and a single global Top-N ranked list, then per-repo sections. Note any anti-pattern that recurs across repos — those are candidates for a shared library fix or a lint rule rather than N separate patches.

## Performance issue taxonomy

The categories the audit must cover. Stack-specific detection lives in the reference files; this is the shared vocabulary.

1. **DB-N+1** — a query per item in a loop / ORM lazy-loading per row. The classic, and usually the highest-impact finding in a CRUD backend.
2. **DB-unbounded** — queries with no pagination or row cap; materializing whole tables (`SELECT *` → list, `.ToList()` on an unfiltered set).
3. **DB-overfetch** — `SELECT *` / returning full entities when a few columns or a projected DTO would do.
4. **DB-clienteval** — filtering, aggregating, sorting, or joining in application memory after pulling more rows than needed (EF Core client-side evaluation; LINQ-to-Objects over a `.ToList()`).
5. **DB-index** — `WHERE`/`JOIN`/`ORDER BY` on columns unlikely to be indexed; leading-wildcard `LIKE`; functions on filtered columns defeating an index. Flag as Needs-review — index existence isn't visible in app code; recommend checking the schema / execution plan.
6. **DB-conn** — connection or `DbContext` per call inside loops, missing pooling, transactions held across slow work or external calls.
7. **CONCURRENCY-block** — sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`), `Thread.Sleep` on a request path, blocking I/O on an async path.
8. **CONCURRENCY-serial** — sequential `await`s in a loop that are independent and could run via `Task.WhenAll` / `Promise.all`.
9. **IO-client** — `HttpClient` / SDK client instantiated per call (socket exhaustion), no connection reuse, no timeout set.
10. **CACHE-missing** — recomputing or re-fetching stable reference data on every call; no memoization of expensive pure work; cache stampede risk.
11. **ALGO** — O(n²) nested scans where a dict/set lookup applies; repeated re-enumeration of `IEnumerable`/iterators; string concat in loops; regex compiled per call; large allocations in hot paths.
12. **PAYLOAD** — large API responses, no pagination on list endpoints, returning entity graphs, chatty endpoints forcing many round-trips.
13. **HOTWORK** — expensive work inline on the request path that belongs in a background job/queue (report generation, bulk notification sends, heavy file processing).
14. **OBSERV** — high-verbosity logging or serialization inside hot loops; per-call expensive diagnostics.

## Severity rubric

- **Critical** — on a hot path AND cost grows with data or traffic (N+1, unbounded query, sync-over-async deadlock risk under load, per-request client instantiation). These cause timeouts and outages as the system scales.
- **High** — significant fixed cost on a hot path, or unbounded cost off the main path; clear win, contained blast radius.
- **Medium** — moderate cost, or a real issue on an infrequent path; worth fixing, not urgent.
- **Low** — micro-optimization, cold-start-only, or cosmetic. List it, don't lead with it.

When confidence is Needs-review, cap the *reported urgency* one notch and say what would confirm it.

## Report structure

ALWAYS use this template for the human-readable report:

```markdown
# Backend Performance Audit — <repo or "Portfolio">
_Generated <date> · static analysis · <N> findings_

> Static review flags likely issues; it does not measure runtime cost. Confirm the
> top findings against profiling/telemetry before large rewrites.

## Top findings (ranked)
| # | Severity | Conf. | Category | Repo | Location | Issue | Est. impact |
|---|----------|-------|----------|------|----------|-------|-------------|
| 1 | Critical | Confirmed | DB-N+1 | ... | file:line | one line | scales with ... |

## Summary
- Counts by severity, and by category. For multi-repo: a repo × severity table.
- Cross-cutting patterns worth a shared fix or lint rule.

## Findings (detail)
For each finding:
### [ID] Title  ·  Severity · Confidence · Category
- **Location(s):** file:line (+ "and N more" with 2–3 representatives if grouped)
- **What & why:** what's slow and the mechanism by which it's slow
- **Evidence:** minimal redacted snippet or the matched pattern
- **Hot path:** yes/no/unknown — call-frequency reasoning
- **Suggested fix:** concrete, with the correctness/risk caveat if any
- **Confirm with:** (only if Needs-review) what telemetry/check would settle it

## Validate before fixing
Short list: the 2–4 findings whose assumed impact most deserves a profiling/Query-Store check first.
```

## Findings record schema (`findings.jsonl`)

One JSON object per line:

```json
{"id":"REPO-DBN1-001","repo":"scrips-pm-api","category":"DB-N+1","title":"Per-appointment patient lookup in list endpoint","severity":"Critical","confidence":"Confirmed","hot_path":"yes","locations":["src/Appointments/AppointmentService.cs:142"],"instances":1,"what":"...","why":"...","evidence":"foreach(var a in appts) { db.Patients.Find(a.PatientId); }","suggested_fix":"...","risk":"none","confirm_with":null}
```

Keep `evidence` short and redacted. `instances` > 1 means a grouped finding; list representative `locations`.

## What this skill does not do

- It does not run or profile the application, and does not read APM/Query-Store data unless the user supplies it. Treat any such data the user gives as ground truth that overrides static guesses.
- It does not fix anything — it produces the inventory. Fixing is a separate phase (the findings.jsonl is the handoff).
- It does not assert root-cause certainty. When in doubt, lower confidence rather than overclaim.
