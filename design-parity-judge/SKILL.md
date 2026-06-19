---
name: design-parity-judge
description: "MEASURED visual-craft + parity gate for any rendered Scrips UI before claiming it looks good / is at parity / done. A render passing is NOT a design passing — this judge MEASURES the live DOM (getComputedStyle / getBoundingClientRect) against hard gates AND a Signal-DS-calibrated craft checklist, scores it, and flags AI-slop. Grounded in the Signal DS (tokens / DESIGN-STATE / contracts) + the prototype/handoff as parity source — never a generic DESIGN.md. Run after any Storybook/preview/browser render and BEFORE saying done/works/parity. Pairs with design-judge (anti-fiction/operational), signal-ds-judge (DS-canon), graduate-and-retire (root-cause to the DS source). Use on: 'validate the design', 'is this at parity', 'does it match the prototype', 'visual QA', 'design polish', or any time you are about to claim a UI looks right."
type: procedure
---

# design-parity-judge — measure the render, don't eyeball it

**Origin (2026-06-12, Samer):** repeatedly I confirmed a UI *rendered* (a blue fill appeared) and
called it done — while the control clipped its own text, a dropdown was double its neighbours, and a
"live" element was a static mock. **A render passing ≠ a design passing**
(`feedback_render_verified_is_not_design_good`, `feedback_measured_visual_parity_gate`). This judge
makes the designer's eye **mechanical and measured** so a flat / clipped / oversized / static /
AI-generic render can never be signed off again. The checklist + scoring + AI-slop blacklist are
**adapted from the gstack `design-review` methodology** (and OpenAI "Designing Delightful Frontends",
Mar 2026), re-grounded in the Scrips Signal DS and Scrips tooling.

**Trigger:** after ANY UI renders (Storybook story, preview server, browser) and ALWAYS before you
write "done / works / looks good / at parity / matches the prototype / shipped".

**Hard rule (verification-gate compliant):** no claim of good/at-parity without the **measured gate
table + score in the message** — each gate, the measured value, pass/fail. A screenshot alone shows
it rendered, not that it passes. Eyeballing is not measuring.

---

## Grounding — Signal DS is the source of truth (NOT a generic DESIGN.md)

Calibrate every finding against the Scrips canon, in this order (upstream wins, per
`signal-ds-authority`):
1. **Tokens** — `scrips-signal-ds/tokens/design-tokens.ts` (+ `tokens.css`): the only legal colors,
   the `--spacing-*` (4px base), `--radius-*`, `--shadow-*`, `--font-size-*`, motion. A value off the
   token scale is a finding.
2. **DESIGN-STATE.md** — locked DS-NNN decisions + the REJECTED color list (`#0076F8`, `#007AFF`,
   `#00B8E3`, `#5C41B5`/purple, teal…). Brand primary = `#005FD4`. Any rejected hex = instant finding.
3. **Component contracts** (`contracts/*.json`) — the component's spec + FHIR binding.
4. **The prototype / Claude Design handoff** — for a PORT, the source design's measured values are the
   parity target (`feedback_port_graduated_handoff_not_rebuild_by_eye`).

Scrips is **APP UI** (dense clinical workspace), not a marketing page — apply the App-UI rules below,
not landing-page rules. Note: the generic checklist says "body ≥16px / flag Inter as generic" — for
Scrips those are **overridden**: the DS type scale is dense (13px body is correct, `--font-size-sm`)
and **Inter is the locked brand font (DS-017)**, not a generic-slop flag.

## Tooling (Scrips, not gstack `$B`)

Measure the live render with **`preview_eval`** (preview server) or **`javascript_tool`** (Claude-in-
Chrome tab). Screenshots via the preview/Chrome screenshot tools. This judge AUDITS + measures; the
**fix** loop is `design-to-dev-pipeline` / `graduate-and-retire` (root-cause atom defects to the DS).

---

## The parser — run on the live render, get the numbers

```js
(() => {
  const out = { clipped: [], controls: [], fonts: {}, flatBrand: [], colors: [], headings: [], touch: [], offGrid: [] };
  const SPACING = [0,4,8,12,16,20,24,32,40,48,64]; // --spacing-* (4px base)
  const h = el => Math.round(el.getBoundingClientRect().height);
  // G1 self-clipping
  for (const el of [...document.querySelectorAll('*')])
    if (el.clientHeight>0 && (el.scrollHeight>el.clientHeight+1 || el.scrollWidth>el.clientWidth+1) && /\S/.test(el.textContent) && el.children.length<=2)
      out.clipped.push({ t: el.textContent.trim().slice(0,24), box: el.clientHeight, content: el.scrollHeight });
  // G2 control-size coherence
  const ctrls = [...document.querySelectorAll('button,input,[role=combobox],select,textarea')].filter(e=>h(e)>0);
  const hs = ctrls.map(h).sort((a,b)=>a-b); const med = hs[Math.floor(hs.length/2)]||0;
  out.medianControlH = med;
  out.controls = ctrls.map(e=>({ t:(e.textContent||e.placeholder||e.getAttribute('aria-label')||'').trim().slice(0,16), h:h(e), oversized: med>0 && h(e)>med*1.4 }));
  // G3 fonts
  out.fonts = { body: getComputedStyle(document.body).fontFamily.slice(0,40), loaded:[...document.fonts].map(f=>f.family).filter((v,i,a)=>a.indexOf(v)===i) };
  // G5 flat brand
  for (const el of [...document.querySelectorAll('[class*=active],[aria-selected=true],[data-state=active],[class*=primary]')]) {
    const bg=getComputedStyle(el).backgroundColor; if(bg==='rgba(0, 0, 0, 0)'||bg==='transparent') out.flatBrand.push({t:el.textContent.trim().slice(0,18),bg});
  }
  // palette + heading scale + touch targets (gstack Phase-2 extraction)
  out.colors = [...new Set([...document.querySelectorAll('*')].slice(0,500).flatMap(e=>[getComputedStyle(e).color,getComputedStyle(e).backgroundColor]).filter(c=>c!=='rgba(0, 0, 0, 0)'))].slice(0,30);
  out.headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(x=>({tag:x.tagName,size:getComputedStyle(x).fontSize,weight:getComputedStyle(x).fontWeight}));
  out.touch = [...document.querySelectorAll('a,button,input,[role=button]')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.width<44||r.height<44)}).map(e=>({t:(e.textContent||'').trim().slice(0,20),w:Math.round(e.getBoundingClientRect().width),hh:h(e)})).slice(0,20);
  return out;
})()
```

---

## HARD GATES (measured, each fail-able) — the core

| # | Gate | Pass condition (measured) | Catches |
|---|---|---|---|
| **G1** | No self-clipping | every el `scrollHeight ≤ clientHeight+1` & `scrollWidth ≤ clientWidth+1` | text cropped top/bottom; label wrapping in a fixed-height pill |
| **G2** | Control-size coherence | no control `> 1.4×` the median control height in its group | a 56px dropdown next to 36px inputs |
| **G3** | Font loaded, not fallback | the locked Inter (DS-017) is in `document.fonts` and is what renders | oversized/wrong type from a never-loaded webfont |
| **G4** | Token-grid alignment | heights/gaps/radii land on the DS scale (4px / `--spacing-*` / `--radius-*`); a row shares a height band + baseline | arbitrary px, ragged rows, misaligned controls |
| **G5** | Real DS color, not flat | branded/active element bg resolves to a DS token (e.g. `rgb(0,95,212)`); zero rejected hex | flat segmented; "active" tab with no fill; black-and-white where the DS has color |
| **G6** | Parity-vs-source | on a PORT, key dims (control h, radii, gaps, labels) match the prototype/handoff within tolerance | a hand-built lookalike drifting from the graduated source |
| **G7** | Operational, not static (→ `design-judge`) | every "live" element maps to a real backend path, not a static label / seeded mock | the "Swap in" label that does nothing; a rule over seeded facts |

PASS only when G1–G6 are green by measurement and G7 is SHIPS/CONDITIONAL per `design-judge`. Any
FAIL → name the element + the measured number + the fix. **Gated ≠ passed**: if a gate fails on an
unmerged DS fix or backend dependency, say "FAIL — gated on <PR/dep>", never "done".

---

## CRAFT CHECKLIST (depth — Signal-DS-calibrated, adapted from gstack)

Each item is high / medium / polish severity. Measure where possible.

**Typography** — font count ≤3 (Inter/Readex/JetBrains Mono only); on the DS type scale
(`--font-size-*`, dense clinical 11/13/18/24 is correct); line-height ~1.5 body / 1.15–1.25 heading;
no skipped heading levels; weight contrast for hierarchy; curly quotes + `…` not `...`;
`tabular-nums` on number columns (clinical values).
**Color & contrast** — only DS tokens (zero rejected hex, zero raw hex literals); WCAG AA (body 4.5:1,
large 3:1, UI 3:1); semantic color = clinical meaning only (red/amber/green), never decorative; no
color-only encoding.
**Spacing & layout** — every gap/pad on the `--spacing-*` (4px) scale, no magic numbers; alignment
consistent (nothing floats off-grid); rhythm (related close, sections apart); radius hierarchy (not
uniform bubbly); max content/reading width set; no horizontal scroll.
**Interaction states** — hover on every interactive el; `focus-visible` ring (never bare
`outline:none`); active/pressed; disabled = reduced opacity + `not-allowed`; loading skeletons match
layout; empty states = message + action; error = specific + next step; touch targets ≥44px.
**Responsive** — sm/md/lg map to the capability ladder (display→capture→review); mobile layout is
*designed*, not stacked desktop; no horizontal scroll; ≥16px tap text on mobile.
**Motion** — ease-out enter / ease-in exit; 50–700ms (DS `--motion-*`); `prefers-reduced-motion`
respected; no `transition: all`; animate only transform/opacity.
**Content/microcopy** — specific button labels ("Save template" not "Submit"); no lorem; truncation
handled; active voice; destructive actions confirmed.

## AI-SLOP blacklist (instant findings — adapted; some already DS-rejected)

1. Purple/violet/indigo or blue→purple gradients (already DS-rejected — `#5C41B5`).
2. The 3-column "icon-in-colored-circle + title + 2-line desc ×3" feature grid (the most AI layout).
3. Icons in colored circles as decoration. 4. Centered-everything. 5. Uniform bubbly radius on all.
6. Decorative blobs / floating circles / wavy dividers. 7. Emoji as design elements (DS: no emoji
icons). 8. Colored left-border on cards as decoration (note: the DS DOES use a brand inset bar as a
*meaningful active-state* signal — that's intentional, not slop). 9. Generic hero copy.
10. Cookie-cutter uniform section rhythm. **Test: would a designer at a respected studio ship this?**

## App-UI rules (Scrips product context)
Calm surface hierarchy, strong typography, few colors, dense-but-readable, minimal chrome. Cards only
when the card IS the interaction (no decorative card mosaics). Section headings state the area /
action ("Selected vitals", "Swap into the encounter when…"). One accent. Lead with the DECISION, not
the data (Linear density). Premium = craft + subtle layered depth (shadow 2/4/6), never flat, never
color-soup. AI-native: the Orb / named-confidence (DS-035) is part of the surface, not decoration.

---

## Scoring (verdict)

- **Parity verdict:** PASS / FAIL (the hard gates G1–G7).
- **Design Score A–F** — weighted: hierarchy 15 · typography 15 · spacing 15 · color 10 · interaction
  10 · responsive 10 · content 10 · AI-slop 5 · motion 5 · perf-feel 5. Each category starts at A; a
  High finding = −1 letter, Medium = −½, Polish = note only.
- **AI-Slop Score A–F** — standalone, with a one-line verdict.
- **Severity** per finding: High (hurts first impression/trust) · Medium (felt subconsciously) ·
  Polish (good→great).

## Output format (paste, with real numbers)

```
PARITY VERDICT: PASS | FAIL    DESIGN SCORE: B    AI-SLOP: A
G1 clip:   pass/fail — <clipped: box vs content px>
G2 size:   pass/fail — median <N>px; oversized: <el @ Npx>
G3 font:   pass/fail — Inter loaded <y/n>; rendered <family>
G4 grid:   pass/fail — <off-grid values>
G5 color:  pass/fail — <flat/transparent branded els; any rejected hex>
G6 parity: pass/fail — <source→actual deltas>
G7 oper.:  SHIPS/CONDITIONAL/FICTIONAL (design-judge) — <static/mocked els>
Findings (sev · category · element · measured · fix)
Quick wins: 3–5 highest-impact <30-min fixes
```
Use the critique voice for qualitative notes: *"I notice… / I wonder… / What if… / I think… because…"* — always tied to the user (the time-pressured clinician) + a specific fix.

---

## Hard rules
1. **Measure, don't eyeball.** Every verdict cites a number from the parser.
2. **A render is not a pass.** "The fill appeared / it rendered" is G5-partial — run all gates.
3. **Root-cause atom failures upstream.** A clipped/flat/oversized DS atom is a DS-component or
   DS-distribution defect → fix in `scrips-signal-ds` via `graduate-and-retire`, not a consumer patch.
   (Origin cases: Select had no compact size; the DS shipped no component CSS; Segmented clipped long
   labels — each fixed at the DS source.)
4. **Calibrate to Signal DS, not generic rules.** Dense type + Inter are correct for Scrips; the brand
   inset bar is a meaningful state, not slop. Generic "≥16px / Inter-is-generic" do NOT apply here.
5. **Gated ≠ passed.** Name the blocking PR/dependency; never "done".

## MECE / cross-references
- `design-judge` — anti-fiction / operational axis (G7). This judge = the **visual** axis.
- `signal-ds-judge` — DS-canon / token / hierarchy correctness (pre-commit on signal-ds files).
- `graduate-and-retire` — when a gate failure root-causes to a DS atom/distribution defect.
- `design-to-dev-pipeline` / `claude-design-master-brief` — the pipeline + TASTE this gate enforces.
- `design-review` (gstack, EXTERNAL, auto-generated — do not hand-edit) — the source this was adapted
  from; use it as a generic fix-loop reference, but THIS skill is the Scrips-grounded gate.

**Attribution:** checklist/scoring/AI-slop adapted from gstack `design-review` + OpenAI "Designing
Delightful Frontends with GPT-5.4" (OpenAI Developers, Mar 2026 — citation web-verified 2026-06-12;
post-cutoff, so confirmed via live source, not memory); re-grounded in Signal DS + Scrips tooling 2026-06-12.
