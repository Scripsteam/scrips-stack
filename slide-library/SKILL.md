---
name: slide-library
description: MANDATORY gate before building any new presentation slide, HTML visual, or embedded component. Read CATALOG.md, match investor questions to existing slides, cite what you checked. Build new ONLY if no match exists — then add it to the catalog immediately.
metadata:
  type: feedback
---

# slide-library — ENFORCED, not advisory

## THIS IS A MANDATORY GATE

**Before writing a single line of HTML for any slide or visual:**

1. Read `~/scrips-repos/scrips-slide-library/CATALOG.md`
2. For each slide needed: match the investor question OR narrative moment to an existing slug
3. If a match exists — use it. State the slug. Do not build a new one.
4. If no match — **you must explicitly state:**
   - Which slugs you checked (list them)
   - Why none of them fit (one sentence each)
   - THEN and only then build the new visual

**Failure mode to avoid:** Building a new flywheel, platform layer diagram, or structural-gap visual when `mevp-flywheel.html`, `mevp-platform.html`, or `mevp-8760.html` already exist and would serve the purpose.

---

## Where the catalog lives

```
~/scrips-repos/scrips-slide-library/CATALOG.md   ← agent-readable, full metadata
https://scrips-slide-library.vercel.app           ← visual browser with live previews
```

---

## How to use an existing slide (CDN)

```tsx
import ResetIframe from "@/components/ResetIframe";

<ResetIframe
  src="https://scrips-slide-library.vercel.app/shared/demo-rcm.html"
  title="Revenue Cycle Management"
/>
```

## How to use an existing slide (offline-safe local copy)

```bash
cp ~/scrips-repos/scrips-slide-library/public/shared/<slug>.html \
   ~/scrips-repos/<new-deck>/public/embeds/<slug>.html
```

---

## When building a new slide (after catalog check fails)

1. Build as a fully self-contained HTML file — zero external CDN links, all CSS/JS inline
2. Do NOT use Signal DS tokens or Scrips product styling in standalone embeds — they are self-contained artifacts with their own visual language (Signal DS is for Scrips product UI, not presentation embeds)
3. Save to `~/scrips-repos/scrips-slide-library/public/shared/<slug>.html`
4. Add the full CATALOG.md entry (all fields: slug, title, category, visual-type, narrative-act, description, when-to-use, investor-questions-answered)
5. Add to the `SLIDES` array in `public/index.html`
6. Commit and deploy:
   ```bash
   cd ~/scrips-repos/scrips-slide-library
   git add -A && git commit -m "Add <slug> — <description>"
   vercel --prod --yes
   ```

---

## Catalog quick-reference by investor question

| Investor asks… | Use slug |
|---|---|
| "Why is the system broken?" | `mevp-8760.html` |
| "Why cardiometabolic problem?" | `cardiometabolic-problem.html` |
| "What does Scrips actually do?" | `cardiometabolic-solution.html` |
| "Why a platform, not point solution?" | `mevp-market-pattern.html` |
| "What is the platform architecture?" | `mevp-platform.html` |
| "How does this compound / get defensible?" | `mevp-flywheel.html` |
| "How do you beat incumbents?" | `org-side-by-side.html` |
| "How does Scrips make money today?" | `demo-rcm.html` |
| "What does the patient layer look like?" | `demo-patient-care-workflow.html` |
| "Where does AI show up in the product?" | `vera-ir-chat.html` |
| "What's the AI architecture?" | `agentflow.html` or `wave3-architecture.html` |
| "What's the data moat?" | `wave3-knowledge-graph.html` |

---

## Enforcement summary

| Step | Required |
|---|---|
| Read CATALOG.md before any HTML | ✅ MANDATORY |
| Cite which slugs checked | ✅ MANDATORY |
| State why no existing slide fits | ✅ MANDATORY (only if building new) |
| Add new slide to catalog after building | ✅ MANDATORY |
| Deploy catalog update to Vercel | ✅ MANDATORY |

---

## Library stats (2026-05-22)

- 20 shared slides · 4 categories (demos, cardiometabolic, market/platform, architecture)
- 3 consuming decks: scrips-briefing · scrips-gt-briefing · scrips-mevp-briefing
- Source: `~/scrips-repos/scrips-slide-library/`
