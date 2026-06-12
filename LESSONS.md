# Scrips Engineering — Lessons (shared memory)

This is the team's accumulated hard-won knowledge — the "memory" a Scrips
engineer's Claude should have on day one, so it doesn't re-learn by breaking
things. Mined from real incidents, real PRs, and founder decisions. **Read this
at the start of substantive work; it's the difference between a grounded agent
and one that guesses.**

Each lesson: the rule, why, and how to apply. Sourced where a specific PR /
decision proves it. This file is **append-only and self-improving** — when a PR
or incident teaches something durable, capture it with `/lesson` (it appends here
and opens a PR). Don't let a lesson live only in someone's head.

---

## Repos, naming, currency

- **Local dir name ≠ GitHub repo name.** `~/scrips-repos/scrips-react` → remote
  `Scripsteam/dev-scrips-pm-react`. Run `git remote -v` before any `gh -R <name>`
  call. (Repos are named by *surface*, not environment — `dev-` in a repo name is
  legacy; new repos are `scrips-<surface>-<tech>`.)
- **`scrips-react` = Practice Management** web app; **`scrips-practitioner-react`
  = Practitioner** web app. The **.NET `Scrips.*` family** is the backend (not
  `scrips_msp1_pm`, which is the Flutter PM mobile app). The repo map in
  `CLAUDE.md` is authoritative.
- **The local checkout is a cache, not the source of truth.** Before citing
  `file:line` as current or flagging a "missing guard" as future work,
  `git fetch` + `git log origin/<default>` the file, and `gh pr list --search`
  the symbol/ticket — the gap may already be fixed in a merged PR. (Origin:
  recommended a DoS cap that Andrew had already shipped in `Scrips.Patient` #874.)
- **Quantitative claims expire.** A `[VERIFIED]` number in a doc was true when
  written. Re-verify any metric/count older than ~30 days before repeating it.

## Deploy & infrastructure

- **Product apps deploy GitHub Actions → ACR (`scripsdevacr`) → AKS
  (`ScripsDevAKS`, ns `dev`) → ingress `dev-*.scrips.com`. NOT Vercel.** Vercel is
  external portals only. The image is built in CI (or `az acr build` when local
  Docker is down); the container serves the built `dist/` via nginx on port 8002.
- **A new web origin needs CORS added to every backend it calls — per service.**
  Each `Scrips.<Service>` carries its own `AllowedOrigins` in
  `appsettings.{env}.json`, baked into the image at build → a CORS change is a
  PR + rebuild/redeploy *per service*. Template: Andrew's `feat(cors): allow
  https://dev-practice-v2.scrips.com origin` — `Scrips.Patient` #875,
  `Scrips.Identity` #492, `Scrips.RuleEngine` #46, `Scrips.QuestionBank` #94. Plus
  the Identity SSO client must allow the origin/redirect for login.
- **The shared dev ingress (`ingress-resource-dev`) serves ~20 hosts.** Editing it
  is high-blast-radius — back it up first, patch additively (JSON `add`, never
  replace the rules/tls arrays), and verify all existing hosts survive.
- **`RuleEngine.API` has no browser ingress** — it binds cluster-internal
  (`IPAddress.Any:6014`), reachable pod-to-pod but not from the browser. The React
  rail can't call it directly; route through `Scrips.Patient` `RunClinicalEdits`
  on `dev-api`, mirroring the Flutter path.

## Backend (.NET) — auth, shared libs, security

- **Auth tokens are audience-less (Skoruba/IS4).** `ValidateAudience` MUST be
  false (else `IDX10208`; no KeyVault secret fixes it). Tenancy rides `orgId`.
  Inherit Bearer from `Scrips.Common.Core` (never double-register); forward the
  caller's bearer on cross-service calls.
- **Shared logic lives in `Scrips.Common.Core` — bump the version, don't fork it.**
  Org-scoping uses the shared `OrganizationIdValidationMiddleware` (QuestionBank
  #90). KV/loader and SignalR-detection fixes ship as Common.Core version bumps
  applied across services (#91–#93, #871). Single-source correctness-critical
  logic; duplicating it is how behaviour drifts.
- **Security/auth code never ships on an agent's green build.** It passes an
  adversarial review + a human owner before merge. Real examples of the bar:
  server-side `password == confirmPassword` (Identity #489), reset-token TTL
  24h→1h (#491), upload size-cap + magic-byte sniff (Patient #874). Green tests ≠
  secure.
- **Green tests can certify a dead core.** A passing suite proves nothing if the
  tests were scoped so the engine never has to run. Verify the evaluator/engine
  *fires* end-to-end, not just that surfaces pass. (Origin: RulesEngine evaluated
  zero rules — silent "all clear" P0 — while 81 tests passed.)

## Frontend (React) & Signal DS

- **Never hardcode a hex value — reference the token.** Canonical primary blue is
  `#005FD4` (`--color-brand-primary`, DS-015). `#0076F8` is **REJECTED** (the
  pre-DS-015 blue). A PreToolUse hook (`ds-color-gate.py`) blocks rejected hex in
  code, reading the live denylist from `scrips-signal-ds/tokens/design-tokens.ts`.
  If you hit it, swap the literal for the token and retry — no investigation.
- **Signal DS is a package, not a folder.** `@scripsteam/scrips-signal-ds`
  (GitHub Packages, Scripsteam-private). Compose its exports; read
  `node_modules/@scripsteam/scrips-signal-ds/dist/index.d.ts` for props before
  building a screen. **Source of truth = the `scrips-signal-ds` repo** (source +
  `contracts/*.json` + `coverage-matrix.md`) + **local Storybook** (`npm run
  storybook` in that repo); `signal-ds.vercel.app/storybook` is an investor-demo
  deploy that can lag — never the dev source. Missing a component → PR it into
  `Scripsteam/scrips-signal-ds`, never author it in a consumer app's domain folder.
- **Local install needs GitHub Packages auth.** `.npmrc` points `@scripsteam` at
  GitHub Packages; set `NODE_AUTH_TOKEN=$(gh auth token)` (token needs
  `read:packages` on Scripsteam) before `npm install`. A `401 Unauthorized` on
  `@scripsteam/scrips-signal-ds` = missing package-read access (an org grant).
- **`index.css` `@theme` generates the `*-status-*` Tailwind utilities** (used by
  ~147 files); the package `tokens.css` `:root` does not. Don't delete the
  `@theme` block to "dedupe" — edit values in place.
- **The Flutter `.dart` is the spec for the port.** Read the real source for
  behaviour, field order, validation strings, event sequencing. The *visual*
  structure comes from Signal Storybook, not Flutter. Don't invent it.

## Process & agent discipline

- **Verify before "done" — primary evidence, this session.** A screenshot for
  "the UI renders", real test output for "tests pass", a grep for "the route
  mounts it". A passing logic test is not proof of a rendered UI. Never relay a
  subagent's self-graded verdict as verification. If you can't verify, say
  "UNVERIFIED" and why.
- **Every PR links a `PROD-XXXX` ticket.** Branch `feat/PROD-XXXX-desc`; commit
  `[PROD-XXXX] …`. One ticket per session; `/clear` between unrelated tasks.
- **Worktree isolation ≠ separation for same-repo agents.** Two parallel agents
  writing the same repo in one worktree will tangle; split commits by file path
  and verify with `git diff`.
- **A subagent's `file:line` facts are branch-scoped** — they reflect the
  checked-out branch, which may be stale vs `origin/main`. Confirm freshness
  before citing as current drift.
- **Small, scoped PRs are the unit of work.** The healthy pattern (Andrew's
  stream): `fix(scheduling): gate Order Requests tab on role`, `style(patients):
  align edit-shell to billing underline-tab design`, a single CORS add, one
  Common.Core bump. Each is one reviewable concern. That's also the shape of a
  good first PR.
- **A setup/install step that reports success without verifying its write is a
  silent failure waiting to happen.** `team-setup.sh` step 5 (the
  `settings.local.json` deny-rule merge) passed an MSYS path (`/c/Users/…`) into
  native Windows Python → `FileNotFoundError`, but with no `set -e` and no
  post-write check it still printed "merged ✓". Net: the security deny-guardrails
  (MCP denies + `az`/`kubectl`/`terraform`) were never applied on any Windows
  engineer's machine while setup reported READY. Two rules: **never pass an MSYS
  path to native Windows Python** (do it in `jq`, or `python3 -c … < "$f" >
  "$f.tmp"` so the shell owns the path); and **every mutating step must re-read
  and assert its result, failing loud** — same family as "green tests can certify
  a dead core." (Source: Andrew, 2026-06-10.)
- **Team-infra that "installs on every machine" has prerequisites beyond copying
  files — its definition-of-done is a *second* engineer's data/effect actually
  landing, not that files copied.** The telemetry instruments
  (`agent-track`/`task-gate`/`push.sh`) installed cleanly yet delivered nothing
  for teammates, for two unhandled reasons: (1) **git-identity** — they read
  `git config --global user.email`, which returns the *personal* email for anyone
  whose scrips identity is set per-repo via `includeIf` (`--global` deliberately
  bypasses `includeIf`) → events mis-attributed. Fix: read the *effective*
  `git config user.email` (no `--global`). (2) **private-repo access** — `push.sh`
  pushes to the private `scrips-telemetry` sink, but teammates had no access (one
  also lacked org write to open the fix PR) → `push.sh` exits "sink repo missing."
  Net: only the author's machine emitted while the rollout looked done. So a
  team-infra skill must, up front: resolve identity the way the team actually
  configures git (effective, not `--global`), and include the access grants /
  clone step in the rollout — then verify a real teammate completes the loop
  end-to-end. Same family as "a setup step that reports success without verifying
  its write." (Source: Tariq + Andrew, 2026-06-12.)

---

*Sources: the team's incident memory + merged PRs (`Scrips.Patient`,
`Scrips.Identity`, `Scrips.RuleEngine`, `Scrips.QuestionBank`,
`dev-scrips-pm-react`, `scrips-signal-ds`) as of 2026-06-09. Keep it current with
`/lesson`.*
