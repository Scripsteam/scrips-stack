#!/usr/bin/env python3
"""
ds-color-gate.py
PreToolUse hook for Edit / Write / MultiEdit / NotebookEdit.

WHY THIS EXISTS (read once, never investigate the blue drift again):
  DS-015 (2026-05-16) darkened the brand primary blue/500 from #0076F8 -> #005FD4
  for WCAG AA. The *token* moved, but #0076F8 had already been hand-copied as a raw
  hex literal into dozens of files. Raw hex literals don't cascade when a token moves,
  so the old blue keeps resurfacing. This hook makes it mechanically impossible to
  COMMIT a rejected color hex (or its rgb()/rgba() form) into a code file.

NO-DUAL-MAINTENANCE (the whole point):
  The denylist AND the canonical replacement values are READ AT RUNTIME from the single
  source of truth — scrips-signal-ds/tokens/design-tokens.ts (REJECTED_COLORS + the blue
  ramp). Nothing is hand-copied here, so this guard can never itself drift. When the DS
  changes, the hook follows automatically.

Behaviour:
  - Scans only code files (.ts/.tsx/.js/.jsx/.mjs/.cjs/.css/.scss/.less/.dart/.html/.vue/.svelte).
  - Skips canonical token sources, the rejected list, and all .md docs (they legitimately
    quote rejected values).
  - On a hit, BLOCKS with the canonical answer inline (which token to use + its live hex).
  - Fails OPEN (exit 0) if the DS source can't be read — never blocks spuriously.
"""
import sys
import json
import re
from pathlib import Path

DS_SOURCE = Path.home() / "scrips-repos" / "scrips-signal-ds" / "tokens" / "design-tokens.ts"

CODE_EXTS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".css", ".scss",
             ".less", ".dart", ".html", ".htm", ".vue", ".svelte"}

# Path fragments that are allowed to contain rejected hexes (canonical sources / denylists / docs).
ALLOW_PATH_FRAGMENTS = (
    "scrips-signal-ds/tokens/design-tokens.ts",
    "tokens/tokens.css",
    "design-tokens.ts",
    "rejected",            # any *REJECTED* file
    "design-state",        # DESIGN-STATE.md
    "changelog",
    "ds-color-gate.py",    # this hook
)


def load_canonical():
    """Return (rejected_hexes:set[str upper], blue_ramp:dict[str->hex]) from the single source."""
    try:
        src = DS_SOURCE.read_text(encoding="utf-8")
    except Exception:
        return None, None

    # REJECTED_COLORS = [ ... '#XXXXXX', ... ]
    rejected = set()
    m = re.search(r"REJECTED_COLORS\s*=\s*\[(.*?)\]", src, re.DOTALL)
    if m:
        # ONLY quoted array entries ('#XXXXXX') — never hexes mentioned in trailing
        # comments (e.g. "// superseded by #005FD4"), which would wrongly block the
        # canonical color.
        for hx in re.findall(r"['\"]#([0-9A-Fa-f]{6})['\"]", m.group(1)):
            rejected.add("#" + hx.upper())

    # blue: { 100: '#..', ... 500: '#005FD4', ... }
    blue = {}
    bm = re.search(r"blue\s*:\s*\{(.*?)\}", src, re.DOTALL)
    if bm:
        for step, hx in re.findall(r"(\d{3})\s*:\s*'#([0-9A-Fa-f]{6})'", bm.group(1)):
            blue[step] = "#" + hx.upper()

    return rejected, blue


def hex_to_rgb_regex(hexstr):
    """Build a regex matching rgb()/rgba() decimal form of a hex, tolerant of spaces."""
    h = hexstr.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return re.compile(r"rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\b" % (r, g, b))


def collect_new_text(ti):
    parts = []
    for k in ("content", "new_string", "new_str"):
        v = ti.get(k)
        if isinstance(v, str):
            parts.append(v)
    for e in (ti.get("edits") or []):
        if isinstance(e, dict) and isinstance(e.get("new_string"), str):
            parts.append(e["new_string"])
    return "\n".join(parts)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    ti = data.get("tool_input", data)
    file_path = (ti.get("file_path") or ti.get("notebook_path") or "").lower()
    if not file_path:
        sys.exit(0)

    # only code files
    ext = "." + file_path.rsplit(".", 1)[-1] if "." in file_path else ""
    if ext not in CODE_EXTS:
        sys.exit(0)

    # allowlisted canonical sources / docs
    if any(frag in file_path for frag in ALLOW_PATH_FRAGMENTS):
        sys.exit(0)

    blob = collect_new_text(ti)
    if not blob:
        sys.exit(0)

    rejected, blue = load_canonical()
    if not rejected:            # fail open — never block when the source can't be read
        sys.exit(0)

    blob_up = blob.upper()
    hits = []
    for hx in sorted(rejected):
        if hx in blob_up:
            hits.append(hx)
        elif hex_to_rgb_regex(hx).search(blob):
            hits.append(hx + " (as rgb/rgba)")

    if not hits:
        sys.exit(0)

    primary = blue.get("500", "#005FD4")
    hover = blue.get("600", "#004BA5")
    active = blue.get("700", "#004795")

    reason = (
        "DS-COLOR GATE — REJECTED color blocked: " + ", ".join(hits) + "\n\n"
        "These hexes are in scrips-signal-ds REJECTED_COLORS (the single source of truth). "
        "The most common offender, #0076F8, is the PRE-DS-015 primary — superseded by "
        + primary + " on 2026-05-16 for WCAG AA. Raw hex literals don't cascade when the "
        "token moves; that is the entire root cause of the recurring blue drift.\n\n"
        "DO NOT hardcode blue hex. Use the token instead:\n"
        "  - primary action      -> var(--color-brand-primary)      = blue/500 " + primary + "\n"
        "  - hover               -> var(--color-interactive-hover)  = blue/600 " + hover + "\n"
        "  - active / emphasis   -> var(--color-interactive-active) = blue/700 " + active + "\n"
        "  (TS/JS: import { semantic, colors } from '@scripsteam/scrips-signal-ds/tokens')\n\n"
        "Source of truth: scrips-signal-ds/tokens/design-tokens.ts -> "
        "@scripsteam/scrips-signal-ds/tokens.css. This is mechanically enforced — "
        "the canonical blue is settled, no need to re-investigate. Replace the literal with "
        "the token and retry."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
