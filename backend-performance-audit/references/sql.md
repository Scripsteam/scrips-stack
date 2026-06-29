# SQL performance heuristics (SQL Server-flavored)

For repos with hand-written SQL — inline queries, `.sql` files, stored procedures, migrations. Pair with `dotnet.md` or `node.md` when the SQL is embedded in app code. These patterns are about the SQL text itself.

## Unbounded / over-fetch

- `SELECT *` — names every column including large/unused ones; breaks covering indexes; brittle. Flag DB-overfetch.
- No `TOP`/`OFFSET ... FETCH` on queries feeding a UI list or API → DB-unbounded.
- `SELECT` into application memory of a whole growing table (claims, appointments, audit) → Critical if hot.

## Index-defeating predicates (confidently flaggable without schema)

- Leading-wildcard `LIKE '%term'` — cannot use a normal index; full scan.
- Function on a filtered column: `WHERE YEAR(CreatedDate) = 2025`, `WHERE LOWER(Email) = ...`, `WHERE CONVERT(...) = ...` — makes the predicate non-SARGable; the index on that column won't be used. Suggest rewriting as a range (`CreatedDate >= '2025-01-01' AND < '2026-01-01'`) or a computed/persisted column.
- Implicit type conversion (e.g. `nvarchar` column compared to an `int` parameter, or vice versa) — silent scans; flag if column/param types are visible.
- `OR` across different columns often defeats index usage — note as Needs-review.

## Plan / structural smells

- `WHERE col IN (SELECT ...)` correlated subqueries executed per row; prefer a join. DB-N+1-like at the SQL level.
- `DISTINCT` or `GROUP BY` used to paper over a join that fans out rows — fix the join, don't dedupe after.
- `CURSOR` / `WHILE` loops in stored procs doing row-by-row work that a set-based statement would do once → High.
- Scalar UDFs in `SELECT`/`WHERE` — historically force row-by-row execution; flag in hot queries.
- Missing `WHERE` on `UPDATE`/`DELETE` — correctness landmine, but also a full-table lock; flag as risk + perf.
- Wrapping a whole batch in one transaction that includes slow or external steps → lock duration.

## N+1 at the data-access layer

- The same parameterized query string executed in a loop (look for query text built/issued inside `foreach`/`for`). Replace with a single set-based query using a table-valued parameter or `WHERE Id IN (...)`.

## Confirmation criteria

For anything index-related you can't confirm from text alone (is there an index? what does the plan do?), record **Needs-review** and set `confirm_with` to point at SQL Server Query Store, `SET STATISTICS IO/TIME ON`, or the actual execution plan. Leading-wildcard `LIKE`, function-on-column, and row-by-row cursors are safe to record as Confirmed/Likely because they're properties of the SQL text itself.

## Multi-tenant note

In a multi-tenant schema, every query should be scoped by the tenant/org id. A query missing the tenant predicate is both a **security/correctness** bug and a performance one (scanning all tenants' rows). Flag missing tenant scoping as a risk-tagged finding.

## Scanner stack key

Pass `--stack sql`, or rely on `auto` (keys off `.sql` files / SQL keywords in source).
