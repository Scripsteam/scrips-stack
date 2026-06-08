---
name: source-of-truth-discipline
description: Mandatory protocol for handling any quantitative or factual claim. Tag every number's provenance tier, match source scope to question scope, reconcile against primary before presenting, and close analytical deliverables with a Sources & confidence block. Use whenever producing analysis that quotes numbers, metrics, costs, dates, counts, or status assertions — especially before they land in chat, an artifact, Slack, or an invoice/finance answer.
---

# Source-of-Truth Discipline

**Origin:** 2026-05-26 FinOps session. Quoted a *forecast* tile ($255/mo) as a current actual, *inferred* RI purchase dates from invoice billing-period dates, and *assumed* a CLI field name ("Premium Series Compute") meant a SQL tier mismatch. Each was caught by Samer, not by me. Root cause: **stating a number whose provenance I had not classified, at a scope that didn't match the question.** This skill makes provenance classification mechanical instead of optional.

The principle is the same one already in the Signal DS authority rule and the code-currency rule: **the generating source wins; downstream copies drift; forecasts and inferences are not actuals.** This skill generalises it to every number.

---

## The 5 provenance tiers

Every number gets exactly one tier, tagged at the moment you write it.

| Tier | Definition | How you may present it |
|---|---|---|
| **PRIMARY** | The system that *generates* the data, queried live | Quote freely. Cite the command/screen. |
| **DERIVED** | Arithmetic on primary (sum, delta, projection-from-actuals) | Show the inputs inline: `$2,766 = Prod $2,690 + IHL $47 + $29`. |
| **FORECAST** | A projection / model output, not yet realized | Must say "forecast/projection" + method. **NEVER** present as a current actual. |
| **CACHE / MIRROR** | A downstream copy that drifts | Reconcile to PRIMARY before quoting. State it's a cache if unreconciled. |
| **ASSUMED / INFERRED** | Your own reasoning, no external source | Label `[ASSUMED]`. Lowest trust. Flag for verification. |

Inline tag format when it matters: `$1,967 [ACTUAL · az cost query]` · `$255 [FORECAST · portal tile]` · `~23mo [ASSUMED]`.

---

## The 6 mechanics (in order)

1. **Scope-match first.** Does the *unit* of your source match the *unit* of the question? The 2026-05-26 core miss was answering a billing-profile question with subscription-scope data. Cost lives at billing-profile scope (= the invoice); code lives at `origin/main` not local; design lives at upstream tokens not downstream docs.
2. **Classify before quoting.** Every number gets a tier the moment it's written. If you can't name the tier, you can't use the number yet.
3. **Trace to PRIMARY before presenting.** A cache → reconcile to primary. A forecast/derived → label it as such.
4. **Reconcile check.** A derived or cache number and its primary must agree within rounding. Mismatch = STOP and investigate. (The $4,761 derived ≈ $4,760 invoice match is what *proved* the Profile 1 = Prod+IHL mapping — reconciliation is evidence, not a formality.)
5. **The pull-it-up test.** Would this number survive Samer opening the source himself? If he'd see something different, you have failed — fix it before sending.
6. **Sources & confidence block** closes every analytical deliverable (see below).

---

## Source register — PRIMARY per domain (the "lists")

| Domain | PRIMARY (ground truth) | Cache/trap — never quote as fact |
|---|---|---|
| **Azure cost** | Cost Management *actual* at **billing-profile scope** + the invoice PDF | forecast tiles; subscription-scope when the question is invoice-scope |
| **Azure reservations** | Reservations → **Utilization tab** + the reservation's own metadata (purchase date, SKU) | invoice line-item dates; SKU-name guesses ("Premium" is a compute series, not a SQL tier) |
| **Code `file:line`** | `git fetch origin` → `origin/<default-branch>` | the local checkout (stale cache — see github.md code-currency rule) |
| **Design tokens / DS facts** | `scrips-signal-ds/tokens/design-tokens.ts` + `DESIGN-STATE.md` | llms.txt, portal HTML, vault ADRs (all caches) |
| **Counterparty / financial $** | bank statements + executed instruments | QuickBooks balances, internal workbooks |
| **Vendor pricing** | the actual contract/invoice in the inbox | memory, round-number guesses |
| **Jira / PR status** | live `gh` / Jira JQL query | memory, assumption from last session |
| **Person classification** | the HR/contract file + Samer's confirmation | Attio title, temporal proximity |
| **Product facts** | brain + canonical docs *that surface their own original source* | a brain citation with no upstream source |

When a new domain appears, add a row rather than freelancing. Most rows already exist as standalone memories; this register consolidates them.

---

## Sources & confidence block (mandatory on analytical deliverables)

Every report/brief/artifact/Slack answer that quotes load-bearing numbers ends with:

```
## Sources & confidence
| Claim | Value | Tier | Source (command / screen) | Re-verify by |
|-------|-------|------|---------------------------|--------------|
| April Profile 1 bill | $4,760 | PRIMARY | invoice G156842392 | open the PDF |
| May Profile 1 proj | $2,904 | DERIVED | Prod $2,690 + IHL $47 + $29 | re-run profile cost query |
| IHL May cost | $47 | FORECAST→ACTUAL(MTD) | Cost Mgmt, billing-profile scope, May MTD | portal Cost analysis |
```

Filling the table IS the audit. A row reading "claim: current cost / tier: forecast" is a caught bug — before anyone else sees it.

---

## Hard rules

- **G1** No FORECAST or DERIVED figure presented as a current ACTUAL. Ever.
- **G2** No number quoted in a deliverable without a citable source command/screen, or an explicit `[UNVERIFIED]` / `[ASSUMED]` label.
- **G3** Scope of source must match scope of question. State the scope explicitly when ambiguous (subscription vs billing-profile vs resource-group).
- **G4** Derived/cache vs primary must reconcile within rounding before presenting; surface the mismatch if not.
- **G5** Don't echo a user's factual assertion as confirmed when you hold contradicting evidence — check your own prior tool output first (the 2026-05-26 "switch to Scrips directory" echo failure).

## Violation = stop and fix in the same pass

If you catch yourself about to state a number you haven't tiered, stop. Classify it. If it's forecast/derived/assumed, either pull the primary or label it. Don't ship an untiered number.
