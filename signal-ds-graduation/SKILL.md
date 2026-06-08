---
name: signal-ds-graduation
description: Use when graduating a new Signal DS primitive from in-development to LOCKED, when introducing a vocabulary or hierarchy change (DS-NNN ADRs), when auditing cross-surface drift, or when Andrew's cloud agents escalate because Figma / Storybook / Signal contracts disagree. Enforces the tri-surface contract — Figma, Storybook, Signal DS must carry the same architecture and the same spec or the system stops compounding. Use proactively any time a Signal contract changes, a Storybook story is added, or a Figma component is published.
type: procedure
---

# Signal DS — Tri-Surface Graduation Contract

## The principle

Signal DS only compounds when **Figma, Storybook, and Signal DS carry the same architecture and the same spec.** If any of the three drifts, Andrew's cloud agents (and any future LLM consumer) read one source of truth, build to it, and the system fragments. Founder rule, locked 2026-05-12.

A graduation is **never** a single-surface action. Even a vocabulary rename in `llms.txt` propagates to Storybook story title paths and Figma library labels. Even a new variant on Figma propagates to a contract JSON and a Storybook story arg. Treat the three surfaces as one logical commit; the only thing that varies is the tooling.

## When this skill fires

1. **New primitive graduation** — a primitive moves from `EXPERIMENTAL` / `PLANNED` / `ASPIRATIONAL` → `LOCKED`. Triggers: a contract JSON's `status` flips to `LOCKED`, OR a designer publishes a Figma variant to the Library, OR an engineer opens a PR with a new `.stories.tsx`.
2. **Vocabulary or hierarchy change** — a DS-NNN ADR alters level names, retires a level, adds a new level, or shifts the scope axis.
3. **Naming change** — a primitive is renamed (e.g. `IndicatorTag` folds into `Badge` as a variant). Touches all three surfaces.
4. **State machine change** — a state is added/removed/relabeled (e.g. Orb gaining a 5th state). Touches all three.
5. **FHIR mapping change** — a contract's `fhir.primary` changes (or is added for the first time on a clinical primitive). Touches Signal contract + Figma description + Storybook story metadata.
6. **Surface eligibility change** — a primitive gains or loses a surface (Practice / Practitioner / Patient). Today's example: Orb moving from Practitioner-only to cross-surface (2026-05-12).
7. **Audit request** — Samer or Andrew asks "are we aligned?" or surfaces a contradiction between two surfaces.

**Do NOT fire** for: token tweaks that don't touch primitives (e.g. shifting a single hex by 1 unit), bugfixes in component implementation that don't change the spec, comment-only PRs.

## The three surfaces — what each MUST carry

Every Signal primitive (Component / Card / Block / Template / Frame) must be discoverable on all three surfaces, with these fields aligned:

| Field | Figma (Library file `IzvV9OCSeIQ3yKS3aNpYOJzL`) | Storybook (`dev-scrips-pm-react/src/**/*.stories.tsx` → Chromatic) | Signal DS (`scrips-signal-ds/contracts/<Name>.json`) |
|---|---|---|---|
| **Name** | Component name (PascalCase) | Story title path leaf (e.g. `Components/Badge`) | `"name"` field |
| **Hierarchy level** | Component description prefix (`[Component]`, `[Card]`, `[Block]`...) | Story title path matches level (`Components/Badge`, `Cards/CardData`, `Blocks/HPI`) | `"hierarchy"` field — one of `component`/`card`/`block`/`template`/`frame` |
| **Scope** | Library group / page (`Cross-Module` / `Domain · Scheduling` / `Frame · Practitioner`) | Story title path prefix indicates (`Shared/`, `Scheduling/`, `Frame/`) | `"scope"` field — one of `cross-module`/`domain`/`frame` |
| **Variants** | Figma variants (named: `tone`, `size`, `state`, etc.) | Storybook args + ArgTypes with closed-enum controls | `"props"` array with typed variants + figmaSurface annotations |
| **States** | Figma states / interactive variants | Storybook stories for each state (Default / Hover / Focus / Pressed / Disabled minimum) | `"states"` array — at minimum `default`, plus interactive states |
| **FHIR ResourceType** (clinical primitives only) | Description field `"FHIR: <ResourceType>"` | Story description: `## FHIR: <ResourceType>` | `"fhir.primary"` field (ResourceType R4) + `"fhir.secondary"` array |
| **Surfaces eligible** | Surface tag in description (`Surfaces: Practice / Practitioner / Patient`) | Story tag `surfaces:[...]` (a Storybook custom param) | `"surfaces"` array |
| **Cross-surface anchors** | Library node ID (auto) | Storybook ID (e.g. `components-badge--default`) | `"figma.nodeId"` + `"react.storybookId"` + `"react.storybookUrl"` (alias) |
| **Status** | Published vs Draft on Library | Tag: `experimental` or absent for LOCKED | `"status"` field — `LOCKED` / `EXPERIMENTAL` / `DRIFT` / `PLANNED` / `ASPIRATIONAL` |

If any cell is empty for a LOCKED primitive, **the primitive is not LOCKED yet** — it's in drift. File a graduation PR to align.

## Graduation procedure — new primitive

When promoting a primitive from EXPERIMENTAL → LOCKED, run these in parallel where possible:

### Designer (Figma)
1. Author the component in the DS Library file with required variants
2. Set description: `Hierarchy: <Component|Card|Block|Template|Frame>. Scope: <cross-module|domain|frame>. FHIR: <ResourceType or "none">. Surfaces: <Practice/Practitioner/Patient>.`
3. Publish to Library (Library files only, not project files — downstream consumers depend on this)
4. Note the Figma node ID for the engineer

### Engineer (Storybook + React)
1. Author `<Component>.tsx` in the right folder (`src/shared/ui/components/` for cross-module, `src/<domain>/components/` for domain, `src/<domain>/frames/` for frame chrome)
2. Author `<Component>.stories.tsx` with title path that matches the hierarchy level. Examples:
   - `Components/Badge` (not `Shared/Atoms/Badge` — Atom is retired per DS-002)
   - `Cards/CardData` (cross-module card)
   - `Blocks/HPI` (cross-module block)
   - `Scheduling/CalendarToolbar` (domain block)
   - `Frame/Encounter` (frame chrome)
3. Cover at minimum: Default + Hover (if interactive) + Focus (if interactive) + Pressed (if interactive) + Disabled
4. Use FormProvider + QueryClientProvider decorators when needed (see `create-patient-view.stories.tsx` pattern)
5. Open PR. Chromatic publishes the build automatically.

### Founder / Claude (Signal DS contract)
1. Write `contracts/<Component>.json` per the schema in `scrips-signal-ds/contracts/README.md`. Required fields:
   - `name`, `version`, `status: LOCKED`, `lastUpdated`, `lockedDate`
   - `hierarchy` (one of `component`/`card`/`block`/`template`/`frame`)
   - `hierarchyLevel` (one of `L1`..`L5` mapped: Component=L1, Card=L2, Block=L3, Template=L4, Frame=L5)
   - `scope` (one of `cross-module`/`domain`/`frame`)
   - `fhir.primary` (FHIR R4 ResourceType, or `null` for non-clinical)
   - `topic.domain`, `topic.stakeholder`, `topic.wedgeAlignment`
   - `surfaces` array
   - `figma.fileKey` (always `IzvV9OCSeIQ3yKS3aNpYOJzL`), `figma.nodeId` (from designer), `figma.nodeName`
   - `react.import`, `react.exportName`, `react.storybookId`, `react.storybookUrl` (use the alias `https://signal-ds.vercel.app/storybook?path=/story/<storybookId>`)
   - `props`, `states`, `tokens`, `a11y`, `doDont`, `decisionRefs`, `_provenance`
2. Register the primitive in `tokens/design-map.json` under the appropriate category (`components` / `cards` / `blocks` / `templates` / `frames`)
3. Add a row to `coverage-matrix.md` (status / level / scope / FHIR / Figma synced / Storybook synced)
4. Cross-link in `llms.txt` §14 COMPONENT INVENTORY if it's a notable primitive
5. Open PR. After merge, the contract is the single source of truth for the primitive.

### The graduation tag
The PR that lands the primitive on all three surfaces gets a `graduation:<Component>` label. Three PRs (Figma is a publish event, not a PR) but they go in **one logical commit** — i.e., the Storybook PR and the Signal-contract PR reference each other and land within a short window.

## Vocabulary-change procedure — DS-NNN ADRs

When a DS-NNN ADR alters level names, retires a level, or shifts the scope axis (example: DS-008 retiring `atom`/`primitive` from contract enum), all three surfaces migrate in lockstep:

### Signal DS
1. Open `decisions/DS-<NNN>-<slug>.md` MADR-style: status=accepted, deciders=[Samer], context, decision, consequences
2. Migrate `contracts/*.json` to the new vocabulary (mass `hierarchy` rewrite if applicable)
3. Update `contracts/README.md` schema enum
4. Amend `llms.txt` §5 / §6 / §7 / §14 wherever the old vocabulary appears
5. Cross-reference in `coverage-matrix.md`

### Storybook (`dev-scrips-pm-react`)
1. Rename folders that mirrored the retired level (e.g. `src/shared/ui/atoms/` → `src/shared/ui/components/`)
2. Update story title paths to match the new hierarchy (`Shared/Atoms/Badge` → `Components/Badge`)
3. Grep-replace any imports that reference the old folder
4. Verify Chromatic build after merge — story navigation should reflect the new vocabulary

### Figma
1. Audit the Library file: do component descriptions carry the right hierarchy label? Are pages / groups labeled with the canonical level names?
2. Update component metadata where it drifts. (Figma node IDs don't change on rename — the anchor in `contracts/<X>.json` stays valid.)
3. Note the Figma side of the migration in the DS-NNN ADR's consequences list

### Cross-reference
Every DS-NNN that touches vocabulary must end with a paragraph: "Migration spans Figma (Library description audit), Storybook (story title path + folder rename), Signal DS (contract enum + llms.txt + coverage-matrix)." If a future reader can't tell from the ADR which surfaces moved, the ADR is incomplete.

## Cross-surface anchors — how the three stay tied

Two fields in `contracts/<X>.json` are the **machine-readable anchors** that keep the surfaces in sync:

```json
{
  "figma": {
    "fileKey": "IzvV9OCSeIQ3yKS3aNpYOJzL",
    "nodeId": "<from designer>",
    "nodeName": "<must match `name`>"
  },
  "react": {
    "storybookId": "<kebab-case lowercase path>",
    "storybookUrl": "https://signal-ds.vercel.app/storybook?path=/story/<storybookId>"
  }
}
```

When an agent looks up a Signal primitive, it should be able to navigate to its Figma source AND its Storybook canonical from these fields alone, no intermediaries. If `figma.nodeId` is `null`, the primitive is React-first and the Figma graduation is pending — flag in PR.

## Audit procedure

Run an audit when:
- Founder asks "are we aligned?"
- A new contract is added (audit the existing ones for drift surfaced by the new one)
- A vocabulary change lands (post-migration sanity check)
- Quarterly, regardless

Audit steps:
1. List all `LOCKED` contracts in `scrips-signal-ds/contracts/*.json`. For each:
   - `figma.nodeId` is non-null and resolves in the Library? Yes / no
   - `react.storybookId` resolves on Chromatic? Yes / no
   - Story title path matches `hierarchy` level? Yes / no
   - Variants in Figma match variants in Storybook match `props` in the contract? Yes / no
2. Build an audit table. Anything `no` → file a `chore/audit-fix-<Name>` PR.

Andrew's `flutter-to-react` skill cross-references this skill in its pre-flight so the agent runs an implicit audit before declaring a primitive shipped.

## Escalation — when drift is detected

When Andrew's cloud agent (or any Claude session) finds drift between Figma, Storybook, and Signal:

1. **Do not silently auto-resolve** — drift is information; resolving it without surfacing means future agents will re-encounter the same drift.
2. Report drift in the PR description with the specific contradiction:
   - "Figma description says `FHIR: Observation`; contract JSON says `fhir.primary: null`. Which is canonical?"
   - "Storybook story title `Shared/Atoms/Badge` doesn't match contract `hierarchy: component`."
3. Tag the founder for a single-sentence resolution. After resolution, file a `chore/align-<Name>` PR that fixes the drift on whichever surfaces were stale.
4. Update this skill if a new drift pattern recurs — add the pattern to the audit procedure.

## Worked example — DS-008 (2026-05-12)

DS-008 retired `atom` and `primitive` from the contract `hierarchy` enum, locked the 6-level canon (Tokens · Components · Cards · Blocks · Templates · Frames), added a `scope` field, and locked the Card-vs-Block + Template-vs-Frame boundary rules.

Tri-surface execution (the first worked example of this skill):

| Surface | Action | PR / Action |
|---|---|---|
| Signal DS | DS-008 ADR + 7 contract `hierarchy` migrations + `scope` field on 9 contracts + `llms.txt` amendments + `coverage-matrix.md` cross-reference | One PR on `scrips-signal-ds` |
| Storybook + React | `src/shared/ui/atoms/` → `src/shared/ui/components/` folder rename + import migrations + story title path renames (`Shared/Atoms/*` → `Components/*`) | One PR on `dev-scrips-pm-react` |
| Figma | Audit Library file for hierarchy/scope labels + description updates on 8 locked components | Checklist for Samer / designer; no Claude action (figma-console MCP edits project files, not the published Library file) |

Both PRs reference each other in their bodies. The Figma audit checklist lands as a comment on the Signal-side PR so the founder ratifies in the same review pass.

This skill itself was authored 2026-05-12 as part of the DS-008 graduation. If future graduations expose missing axes, amend this skill alongside the new DS-NNN ADR.

## Skill cross-references

- `~/.claude/skills/flutter-to-react/SKILL.md` (Andrew's port skill) — should reference this skill in its pre-flight checklist so subagents check tri-surface alignment before declaring port-work shipped. PR [#37](https://github.com/Scripsteam/dev-scrips-pm-react/pull/37) added the Signal-source anchor; a follow-up PR can deepen the cross-reference once this skill is consumed in anger.
- `anthropic-skills:scrips-engineering` — for code-side concerns
- `anthropic-skills:scrips-product` — for cross-module sequencing concerns

## When NOT to use this skill

- Token shifts that don't touch a primitive's spec (e.g. tweaking a hex by 1)
- Bug fixes in component implementation that don't change props/states/FHIR/surfaces
- Comment-only PRs
- Documentation rewording that doesn't change content
- One-off prototypes in `experimental/` that aren't graduating

If unsure: fire the skill. The cost of running it on a non-graduation is a 30-second review; the cost of skipping it on a real graduation is months of compounding drift.

## Audience filter — surface what's actionable, not what's interesting

**When informing an engineer of audit findings or graduation status, filter by their active scope.** Drift that doesn't touch their work is noise — it creates cognitive load without actionable upside, and accumulates "blocker fatigue" where the engineer learns to skim the updates.

Concretely:
- **Andrew → Practice Management port** (Scheduling · Patients · Billing · RCM · Org). Surface anything that touches `shared/ui/components/` shadcn primitives, the PM domain components, or rules that apply across all surfaces (tinted-pill contrast, DS-008 vocabulary, surface taxonomy). **Do NOT surface** Patient consumer / longevity / Stage Frame / OrganAge family drift — that's a separate stream (Samer-led).
- **Patient-surface engineer / designer → Stream 2**. Surface OrganAge family, Stage Frame, Reveal mode, longevity primitives. Do NOT surface PM-only churn (RCM dashboards, scheduling toolbars).
- **Cross-cutting** (founder, design-system owner, anyone touching all surfaces) → full picture is appropriate.

The rule: **what does THIS person need to carry their next move?** If the answer is "nothing — this is FYI", consider whether it belongs in the audit trail artifact (which they can read if curious) rather than the Slack DM (which interrupts).

Default Slack update template per scope:
- **PR merged that affects their work** → ✓ surface
- **PR merged that doesn't affect their work** → omit (or one-line index reference)
- **Drift discovered that blocks them** → surface immediately
- **Drift discovered in adjacent surface** → activity log + artifact, NOT Slack
- **Open blockers they could close** → surface with explicit ask
- **Open blockers only the founder can close** → omit (it's not actionable for them)

Set 2026-05-12 after Samer caught Claude noising up an Andrew DM with OrganAgeCard publish blocker + Drift B graduation queue — none of which touched Andrew's PM port scope.
