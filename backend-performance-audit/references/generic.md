# Generic performance heuristics (language-agnostic)

Always load this alongside the stack-specific reference. These categories recur in every backend regardless of language, and also cover Python, Java, Go, and anything the stack-specific files don't.

## ALGO — algorithmic complexity

- **Nested iteration with inner search** — a loop over collection A that, per element, scans collection B (`find`/`contains`/`indexOf`/inner loop) is O(n·m). Pre-build a hash map/set keyed on the join field and do O(1) lookups. This is the single most common avoidable CPU hot spot.
- **Repeated re-enumeration** — iterating the same lazy sequence (generator/iterator/`IEnumerable`/stream) multiple times re-runs it. Materialize once.
- **Quadratic string building** — concatenating strings in a loop reallocates each time. Use a builder/buffer/join.
- **Regex compiled per call** — hoist to a module/static constant. Watch for catastrophic backtracking (ReDoS) on user-controlled input — flag as perf + security.
- **Sorting/dedup in a loop** — re-sorting or re-deduping inside an iteration that could be done once outside it.

## CONCURRENCY

- **Serial independent work** — sequential `await`/blocking calls in a loop where iterations don't depend on each other can be parallelized (`Task.WhenAll` / `Promise.all` / goroutines / thread pool). Always note a concurrency cap so you don't swamp downstream resources or the DB pool.
- **Blocking on a hot path** — synchronous I/O, sleeps, or long CPU work on a request-serving thread/loop. Severity scales with how hot the path is.
- **Lock contention** — coarse locks held across slow work (I/O, external calls); a single global lock on a hot path. Flag held-lock-across-I/O as High.

## CACHE

- **Recomputation** — expensive pure functions called repeatedly with the same inputs → memoize.
- **Re-fetch of stable data** — reference/config/lookup data read from the store on every request → cache with a TTL. In multi-tenant systems the cache key MUST include the tenant/org id; a missing tenant key is a correctness bug, not just a perf miss — flag with risk.
- **Cache stampede** — many concurrent misses recomputing the same value; recommend single-flight / locked refresh for expensive entries.

## I/O & RESOURCES

- **Per-call client/connection creation** — HTTP clients, DB connections, SDK clients created per call instead of pooled/reused → resource exhaustion under load.
- **No timeouts** — external calls without a timeout block threads/connections indefinitely; perf + reliability flag.
- **Unbounded buffering** — reading an entire large file/response into memory instead of streaming.
- **Chatty external calls** — N sequential calls to a dependency that offers a batch endpoint.

## DATA ACCESS (generic)

- **N+1** — a query/RPC per item in a loop. Batch it.
- **Unbounded reads** — fetching without a limit from a growing dataset.
- **Over-fetch** — pulling more columns/fields/rows than the caller uses.
- **Work the store could do** — filtering/aggregating/sorting in app memory that the database/service could do server-side.

## HOTWORK & OBSERV

- **Inline heavy work** — report/PDF generation, bulk messaging, media processing, large exports done synchronously in a request handler → move to a background job/queue.
- **Logging/metrics in hot loops** — high-verbosity logging or serialization per iteration on a hot path.

## Python / Java / Go quick notes

- **Python**: ORM N+1 (Django `.select_related`/`.prefetch_related` missing; SQLAlchemy lazy loads); `requests.get` per call without a `Session`; sync work blocking an async (`asyncio`) handler; list-comp building huge lists where a generator suffices; pandas row-wise `.apply`/`iterrows` over vectorizable ops.
- **Java**: JPA/Hibernate N+1 (missing `JOIN FETCH`/`@EntityGraph`); `LAZY` access outside a session; `new RestTemplate`/`HttpClient` per call; synchronized methods on hot paths; autoboxing in tight loops; `String +` in loops (use `StringBuilder`).
- **Go**: queries in a `for` loop (batch with `IN` / `pgx.Batch`); missing `rows.Close()`/leaked connections; unbounded goroutine fan-out without a worker pool / `errgroup` limit; `defer` inside hot loops; building slices without capacity hints.

## Scanner stack key

`--stack generic` runs the language-agnostic patterns; `auto` always includes them.
