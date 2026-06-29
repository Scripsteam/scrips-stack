# Node / TypeScript backend performance heuristics

For Express/Nest/Fastify services using Prisma, TypeORM, Sequelize, Knex, or a raw driver. Pair with `sql.md` for hand-written SQL and always with `generic.md`.

## DB-N+1

Candidate patterns:
- `await` to the ORM/driver (`prisma.`, `repository.`, `.findOne`, `.findByPk`, `.query(`) inside a `for`/`for...of`/`.map(async ...)`/`.forEach(async ...)`.
- `Promise.all(items.map(i => prisma.x.findUnique(...)))` — parallel, but still N queries; for lookups prefer a single `findMany({ where: { id: { in: ids } } })`.
- Sequelize/TypeORM lazy relations accessed per row without eager `include`/`relations`.

Confirm: query-per-row over scaling data → Critical on a request path. Fix: batch with an `IN` query (`findMany`/`whereIn`) and join in memory, or eager-load the relation in one query.

## DB-unbounded / overfetch

- `findMany()` / `.findAll()` / `SELECT *` with no `take`/`limit`/`where` → DB-unbounded.
- Returning full ORM models (with all relations) from handlers instead of a `select`/projection → DB-overfetch. Group across routes.
- List routes with no pagination params → PAYLOAD + DB-unbounded.

## CONCURRENCY-serial (very common in Node)

- `await` inside `for...of`/`for` where iterations are independent → should be `Promise.all`. High value, easy fix.
- Caveat: don't unbound the concurrency — `Promise.all` over thousands of items can overwhelm the DB/connection pool. Recommend a concurrency cap (`p-limit`, batching). Note this in the finding.

## CONCURRENCY-block

- Sync I/O on the event loop: `fs.readFileSync`, `fs.writeFileSync`, `execSync`, synchronous crypto (`crypto.pbkdf2Sync`, large `bcrypt` sync), `JSON.parse` of very large payloads on the request path → blocks the single event-loop thread → Critical on a hot path.
- Long synchronous CPU loops on the request path (should move to a worker thread / queue).

## IO-client

- `new http.Agent` defaults / no keep-alive; creating a new client (axios instance, DB pool) per call rather than reusing a module-level singleton; no request timeout set.

## ALGO

- `array.find`/`array.includes`/`array.indexOf` inside a loop over another array → O(n²); build a `Map`/`Set`.
- Spreading/recreating large arrays/objects in loops; `array.push` patterns that re-allocate; building strings with `+=` in tight loops.
- `new RegExp(` recompiled per call; regexes with catastrophic backtracking on user input (ReDoS) — flag as perf + reliability.
- Repeated re-computation that could be memoized.

## CACHE-missing / HOTWORK / OBSERV

- Reference data fetched from DB on every request without an in-memory/Redis cache (key by tenant).
- Heavy work inline in a handler (PDF/report generation, bulk sends, image processing) that belongs on a queue (BullMQ, etc.) → HOTWORK.
- `console.log`/logger calls with serialization inside hot loops → OBSERV.

## Confirmation criteria

Read the route/handler to confirm hot-path status. For ORM lazy-loading, confirm relations aren't eager-loaded upstream. For event-loop blocking, confirm it's reachable from a request handler (not a startup/CLI script).

## Scanner stack key

Pass `--stack node`, or rely on `auto` (keys off `package.json`).
