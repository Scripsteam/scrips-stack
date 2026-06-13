# scrips-stack — Claude Code Instructions (team grounding kernel)

This file is the shared grounding kernel for every Scrips engineer's Claude. Its
job is to keep the agent **accurate** about what the repos are, where things
live, and how we ship — so it never has to guess (guessing is how onboarding
docs end up with invented repos, wrong hosting, and rejected colors).

> **Anti-drift principle (read first).** Do NOT state a repo's purpose, a token
> value, a deploy target, or a file path from memory or inference. Verify against
> the source of truth below, or inspect the repo (`ls`, `Read`, `git remote -v`).
> If you cannot verify a fact, say so — never fabricate a plausible answer.
> Counts ("2,500 units", "21 modules"), file paths, and directory names must be
> produced by actually reading the tree, not imagined.

> **Shared memory — read `LESSONS.md`.** The team's accumulated hard-won
> knowledge (auth quirks, the CORS-per-service pattern, DS token rules, the deploy
> path, "green tests can certify a dead core") lives in `LESSONS.md`. Read it
> before substantive work — it's grounding you'd otherwise relearn by breaking
> something. When you learn something durable, capture it with **`/lesson`** so it
> compounds instead of living in one person's head.

---

## Canonical source map — consult the authority, don't grep-and-guess

The most common agent error is a confident wrong answer to "where does X live / what's
the reference / does Z exist", produced by searching one convenient place and stopping.
For these questions, go to the NAMED authority below. State your search SCOPE; never
conclude "doesn't exist" from a narrow search.

| Question | Authority (consult this, not a sibling repo's filesystem) |
|---|---|
| Product UI design / components for ANY surface (practice, **practitioner**, patient) | **The `scrips-signal-ds` repo is the source of truth**: component source in `src/{atoms,molecules,organisms,templates}`, `contracts/*.json`, `coverage-matrix.md`, `design-tokens.ts`, `DESIGN-STATE.md` — plus the installed `@scripsteam/scrips-signal-ds` package and **local Storybook** (`npm run storybook` in the repo). Figma = "Scrips Design System". A sibling React app is NOT the design reference. **`signal-ds.vercel.app/storybook` is an investor-demo deploy — it can lag the repo; never cite it as the dev source.** |
| What's already built vs a genuine gap | `scrips-signal-ds/coverage-matrix.md` |
| DS tokens / locked decisions | `scrips-signal-ds/tokens/design-tokens.ts` + `DESIGN-STATE.md` |
| Repo map / what each repo is | this file |
| Team engineering lessons | `LESSONS.md` |

**Porting rule:** the practitioner clinical/encounter surface is ALREADY graduated into
Signal DS (`EncounterStep`, `VitalCard`, `PatientSummaryPanel`, 18 chart-tab organisms…,
all exported from `@scripsteam/scrips-signal-ds`). **Compose these — do not hand-port them
from Flutter.** Hand-port only what `coverage-matrix.md` shows as not yet built. Check
Signal DS FIRST.

---

## Repo map (source of truth — local dir ≠ GitHub repo name)

All repos live at `~/scrips-repos/`. **The local folder name often differs from
the GitHub repo name — run `git remote -v` before any `gh -R` call.**

### Product surfaces (what we build)
| Local dir | GitHub repo | What it is | Stack |
|---|---|---|---|
| `scrips-react` | `Scripsteam/dev-scrips-pm-react` | **Practice Management** web app (clinic/operational). Ground-up React rewrite, Flutter as spec. | React 19 · TS · Vite · Tailwind 4 · Signal DS |
| `scrips-practitioner-react` | `Scripsteam/scrips-practitioner-react` | **Practitioner** web app (doctor/clinical). Active Flutter→React port. | React 19 · TS · Vite · Tailwind 4 · Signal DS |
| `scrips-signal-ds` | `Scripsteam/scrips-signal-ds` | **Signal Design System** — published as `@scripsteam/scrips-signal-ds`. | React · tokens · Storybook |

### Port sources (Flutter — the spec for the React rewrite)
| Local dir | What it is |
|---|---|
| `scrips_msp1_pm` | Flutter **Practice Management** mobile app |
| `scrips_msp1_pa` | Flutter **Practitioner** app — the PA-React port source |
| `scrips_msp1_flutter_shared` | Shared Flutter code — source of truth for shared widgets/logic |

### Backend (.NET C# microservices — the `Scrips.*` family)
The API is **not** a single repo. It is a family of .NET microservices, each its
own `Scrips.<Service>` repo, deployed to AKS. Key ones: `Scrips.Patient`,
`Scrips.PracticeManagement`, `Scrips.Identity`, `Scrips.AppointmentScheduling`,
`Scrips.Billing`, `Scrips.Master`, `Scrips.Persons`, `Scrips.Provider`,
`Scrips.Organization`, `Scrips.Notifications`, `Scrips.RuleEngine`. They surface
behind one gateway host, `dev-api.scrips.com`, routed per-path by the dev ingress.

> Common mislabels to avoid: `scrips-react` is **PM, not "admin"**.
> `scrips_msp1_pm` is the **Flutter mobile app, not the backend**. The backend is
> the `Scrips.*` services.

---

## Hosting & deploy (NOT Vercel for product apps)

Product apps (the React web apps + the .NET services) deploy via **GitHub Actions
→ Azure Container Registry (`scripsdevacr`) → AKS (`ScripsDevAKS`, namespace
`dev`)**, served behind the shared nginx ingress at `dev-*.scrips.com`. Vercel is
for **external portals only** (e.g. signal-ds.vercel.app, marketing/portal
surfaces) — never the product apps.

- PM web app → `https://dev-practice-v2.scrips.com`
- Practitioner web app → `https://dev-practitioner-v2.scrips.com`
- API gateway → `https://dev-api.scrips.com`

Database: SQL Server. Auth: IdentityServer (Skoruba/IS4) JWTs — tokens are
**audience-less**, tenancy rides `orgId`; never assume an `aud` claim.

---

## Signal DS — read the live source, never hardcode hex

Signal DS ships as the versioned package **`@scripsteam/scrips-signal-ds`** (GitHub
Packages, Scripsteam-private). Consume it; don't reinvent UI.

```tsx
import { Button, StatusChip } from '@scripsteam/scrips-signal-ds';
import '@scripsteam/scrips-signal-ds/tokens.css';   // CSS variables — USE THESE
import '@scripsteam/scrips-signal-ds/fonts.css';
```

**Never hardcode a hex value — reference the token.** Raw hex literals are exactly
what drifts when a token moves. The canonical primary blue is **`#005FD4`**
(`--color-brand-primary` / `--color-interactive-default`, DS-015). The older
`#0076F8` is **REJECTED** — if you see it, it's stale.

Canonical references, in order (the **repo is the source of truth**):
1. **`Scripsteam/scrips-signal-ds` repo** — component source in `src/`, `contracts/*.json` (per-component), `DESIGN-STATE.md` (locked DS-NNN decisions), `tokens/design-tokens.ts` (hex), `coverage-matrix.md`.
2. **Installed exports** — `node_modules/@scripsteam/scrips-signal-ds/dist/index.d.ts` (read props before composing).
3. **Local Storybook** — `npm run storybook` *in the scrips-signal-ds repo* — the live visual contract, always in sync with your checkout.
4. **`signal-ds.vercel.app/storybook` — investor-demo deploy only.** It can lag the repo; do NOT use it as the dev source of truth.

If a component is missing, open a PR against `Scripsteam/scrips-signal-ds` — do not
author it inside a consumer app's domain folders.

## Figma

Canonical design file is the **"Scrips Design System"** space (30 pages, 268
components). **Refer to it by name, never paste the file key.** Open via Figma
Desktop or the figma MCP; do not cite a raw key in any message or doc.

---

## Estimation — calibrate against measured reality (non-negotiable)

Agents over-estimate (week-scale guesses for hour-scale work). Before giving ANY
task or sprint estimate:
1. **Read the measured baseline** — `Scripsteam/scrips-telemetry/baseline.json`
   (per-category PR delivery-lead medians + per-ticket history; PRIMARY/measured).
2. **Apply reference-class forecasting** — find the matching category, state the
   measured median/p75, and correct your raw estimate toward it. Show both:
   "raw estimate X; reference class (category, n=…) median Y → corrected Z."
3. **Record the estimate on the Jira ticket** (`estimatedMin` + category +
   one-line rationale) so the loop closes — the reconciler later pairs it with the
   measured actual (PR open→merge). An estimate not recorded on the ticket is a
   lost calibration pair.

Lead time = delivery (PR open→merge), not pure effort — estimate *delivery*, the
thing sprint planning actually needs.

## Git & Jira conventions

- **Jira project key: `PROD`.** Tickets are `PROD-XXXX`. (Not `DEV-`.)
- Branch: `feat/PROD-XXXX-short-description` (or `fix/`, `chore/`)
- Commit: `[PROD-XXXX] Imperative description`
- PR: title `[PROD-XXXX] …`, body links the Jira ticket. Every PR links a ticket — no exceptions.
- DS-first: always Signal DS components; never invent UI; never hardcode colors.
- No `console.log` in commits. One ticket per session; `/clear` between unrelated tasks.

---

## Skill routing

When the user's request matches a scrips-stack skill, invoke it with the Skill
tool as your FIRST action — don't answer directly or use other tools first.

- Ship / deploy / create PR / push branch → **ship**
- Code review / check my diff / review this PR → **review**
- Bug / error / crash / 500 / "why is this broken" → **investigate**
- Sprint planning / demo / Jira ceremony → **sprint**
- Figma to code / Signal DS / component → **design-sync**
- QA / test the feature / acceptance criteria / staging → **qa**
- Morning brief / standup / "plan today" → **brief**
- Retro / "what did we ship" → **retro**
- Security audit / OWASP / DB access control → **cso**
- Save progress / checkpoint / resume later → **checkpoint**
- Onboard a new engineer / "onboard me" → **onboard**
- PR merged / bug root-caused / "we shouldn't relearn this" / "capture this" → **lesson** (append to `LESSONS.md`, PR it)

Methodology (auto-invoke without being asked):
- New feature/component/behavior described → **feature-brief** FIRST (Stage 00 — a 5-dimension brief + gate before any stage opens), then **brainstorming**
- Requirements clear, about to code → **writing-plans**
- Implementing from a plan → **test-driven-development** (per unit)
- Plan has independent parallel tasks → **subagent-driven-development**
- User says "done"/"it works" → **verification-before-completion** FIRST
- Bug / test failure → **systematic-debugging** FIRST
- About to open a PR → **requesting-code-review**; feedback arrives → **receiving-code-review**

---

## Available skills

Installed flat at `~/.claude/skills/<name>/` by `./setup` (the umbrella link
`~/.claude/skills/scrips/` also resolves for reference).

Scrips: `/feature-brief` (Stage 00 — start every feature here) · `/ship` · `/review` · `/investigate` · `/sprint` · `/design-sync` · `/qa` · `/brief` · `/retro` · `/cso` · `/checkpoint` · `/onboard` · `/synth` · `/admin-sprint-runner` · `/decompose-strategy` · `/lesson`

**Harness (the gates the team runs):** `harness/install-harness.sh` (run by `./setup`) installs the DS-color gate (blocks rejected hex like `#0076F8` in code), the destructive-bash gate, and the FHIR architecture advisor into `~/.claude/`. Same guardrails on every dev's machine.

Methodology (`~/.claude/skills/scrips/methodology/`): `/brainstorming` · `/writing-plans` · `/test-driven-development` · `/systematic-debugging` · `/verification-before-completion` · `/using-git-worktrees` · `/subagent-driven-development` · `/executing-plans` · `/dispatching-parallel-agents` · `/requesting-code-review` · `/receiving-code-review` · `/finishing-a-development-branch`

---

## Verify-before-done (team rule)

No claim of "done / working / passing / rendered" without primary evidence
produced this session — a screenshot for UI, real test output for tests, a grep
for "the route mounts it". A passing logic test is not proof a UI renders. When
you can't verify, say "UNVERIFIED" and why. (This is what `/verification-before-completion` enforces.)
