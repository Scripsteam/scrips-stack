# .NET backend performance heuristics

For ASP.NET Core services using EF Core, Dapper, or raw ADO.NET. Each category lists candidate patterns (what the scanner greps for) and **confirmation criteria** — what to verify by reading before you record a finding. Read SQL Server-specific query concerns in `sql.md` as well when the repo issues hand-written SQL.

## DB-N+1 (highest yield — check first)

Candidate patterns:
- `foreach`/`for`/`.Select(`/`.Where(` body containing `_context.`, `db.`, `repository.`, `.Find(`, `.First`, `.Single`, `.Any(`, `.Count(`, `await ... Async(` — i.e. a query executed once per iteration.
- Lazy-loading: navigation property access (`order.Customer.Name`, `appt.Patient.Mrn`) inside a loop where the navigation was not `Include`d. If `UseLazyLoadingProxies` is configured, every such access is a round-trip.
- A method that returns a list of DTOs and, per element, calls another service method that itself queries.

Confirm by checking: is the loop body issuing a DB call (directly or via a navigation under lazy loading)? Is the loop over data that scales (rows, list length)? If yes → DB-N+1. Severity Critical if on a request path.

Fix direction: project with a single query and `.Include`/explicit join, or batch the lookups (`WHERE Id IN (...)`) and join in memory once. Note: multiple collection `.Include`s in one query cause a **cartesian explosion** — prefer `AsSplitQuery()` (record as DB-conn/DB-overfetch if you spot several collection includes together).

## DB-unbounded

Candidate patterns: `.ToList()` / `.ToArray()` / `.ToListAsync()` directly on a `DbSet` or a query with no `.Where`, `.Take`, `.Skip`. Raw `SELECT` without `TOP`/`OFFSET FETCH`. List endpoints with no page-size parameter.

Confirm: does the query bound its result set? Could the table grow unboundedly (appointments, audit logs, claims)? Unbounded materialization of a growing table on a request path → Critical.

## DB-overfetch

Candidate patterns: `return ... DbSet` / returning entities from controllers; `.Include` chains feeding an endpoint; `SELECT *`; no `.Select(x => new Dto{...})` projection.

Confirm: is the full entity (or graph) serialized to the client when only a subset is used? Group across endpoints — this is almost always a recurring pattern, so emit one grouped finding.

## DB-clienteval

Candidate patterns: `.ToList()` / `.AsEnumerable()` followed by `.Where`/`.Sum`/`.OrderBy`/`.GroupBy`; `.Where(... someCSharpMethod(x) ...)` that EF can't translate; string ops in predicates.

Confirm: is filtering/aggregation happening in memory after pulling rows the DB could have filtered? In EF Core 3+, untranslatable predicates throw, but `.AsEnumerable()`/`.ToList()` mid-query silently moves work client-side. High severity when it pulls many rows to return few.

## DB-conn

Candidate patterns: `new DbContext`/`new SqlConnection` inside a loop or per call outside DI; `new SqlConnection(` not in a `using`; `BeginTransaction` with `await` external calls (HTTP, file) inside the transaction scope; several collection `.Include`s in one query.

Confirm: connections/contexts should come from DI and be scoped per request, not per row. Transactions should not span network calls. Flag long-lived transactions as High (lock contention).

## DB-index — Needs-review by default

Candidate patterns: `.Where(x => x.SomeColumn == ...)`, `WHERE col =`, `JOIN ... ON`, `ORDER BY`, `LIKE '%...'` (leading wildcard), functions on filtered columns (`WHERE YEAR(date) =`, `WHERE LOWER(name) =`).

You cannot see indexes from app code. Record as Needs-review with `confirm_with: "check index on <table>.<column> / execution plan in SQL Server"`. Leading-wildcard `LIKE` and functions-on-columns are confidently flaggable as index-defeating regardless of schema.

## CONCURRENCY-block (deadlock + thread-pool starvation risk)

Candidate patterns: `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`, `Task.Run(...).Result`, `Thread.Sleep(` on a request path, sync I/O (`File.ReadAllText`, `WebClient`, `stream.Read`) in an async method.

Confirm: is this on a request-handling path or a frequently-called service method? Sync-over-async there risks thread-pool starvation and, with a sync context, deadlock under load → Critical. The same in a CLI/startup task → Low.

## CONCURRENCY-serial

Candidate patterns: `await` inside a `foreach`/`for` where each iteration is independent (no data dependency between iterations).

Confirm: are the awaited operations independent? If yes, they can be `await Task.WhenAll(items.Select(async i => ...))`. Watch the caveat: a single `DbContext` is **not** thread-safe — do not parallelize DB calls that share one context. Note that caveat in the finding.

## IO-client (socket exhaustion)

Candidate patterns: `new HttpClient(` (especially inside methods/loops rather than via `IHttpClientFactory`); `new SmtpClient`, SDK clients constructed per call; no `Timeout` set on outbound clients.

Confirm: `HttpClient` instantiated per call exhausts sockets (TIME_WAIT) under load → High/Critical. Should be `IHttpClientFactory` or a singleton. No timeout on an external call is a separate reliability flag.

## CACHE-missing

Candidate patterns: repeated reads of config/reference tables (lookup lists, code tables, tenant settings) per request with no `IMemoryCache`/`IDistributedCache`; expensive pure computation recomputed each call.

Confirm: is the data stable within a request/short window and read on a hot path? Multi-tenant note: cache keys must include the tenant/org id — a missing tenant key is a correctness bug, flag it as risk.

## ALGO

Candidate patterns: nested `foreach` over collections with an inner `.First`/`.Any`/`.Where` (O(n²) — replace inner scan with a `Dictionary`/`HashSet` lookup); `new Regex(` inside a method (compile once as a static/`[GeneratedRegex]`); `+=` string concat in loops (use `StringBuilder`); multiple enumeration of the same `IEnumerable` (materialize once).

## PAYLOAD / HOTWORK / OBSERV

- PAYLOAD: list endpoints returning unpaged collections or full entity graphs (overlaps DB-overfetch/unbounded but reported at the API boundary).
- HOTWORK: report generation, bulk notification/WhatsApp sends, PDF rendering, file processing done inline in a request handler instead of enqueued to a background worker/queue → High.
- OBSERV: `_logger.LogInformation`/`LogDebug` with string interpolation inside hot loops; serializing large objects to logs per call.

## Scanner stack key

When invoking `scripts/scan.py`, pass `--stack dotnet` (or rely on `auto`, which keys off `*.csproj`/`*.sln`).
