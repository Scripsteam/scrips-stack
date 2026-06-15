#!/usr/bin/env python3
# TEAM telemetry — budget tracker (tokens + notional $), sliced BY PROJECT.
# Harvests per-message token usage Claude Code already records in local
# transcripts (so NO OTEL collector is needed) and attributes it to the project
# the work happened in (derived from the transcript folder = the cwd). Appends a
# 7-day snapshot to events.jsonl keyed by git email; push.sh ships it. Never blocks.
#
# Cost is NOTIONAL — Anthropic API list rates on measured tokens. A DERIVED figure
# for relative comparison across people/projects, not a billing actual.
import json, os, glob, subprocess
from datetime import datetime, timedelta, timezone

def git_email():
    # EFFECTIVE email (matches agent-track / task-gate) so a dev's budget keys to
    # the same identity as their dispatches/estimates.
    try: return subprocess.run(["git","config","user.email"],capture_output=True,text=True,timeout=5).stdout.strip() or "unknown"
    except Exception: return "unknown"

def project_from_dir(name):
    """Transcript folder (cwd with '/'->'-') -> project key. ~/scrips-repos/<repo>
    -> <repo>; worktrees -> the parent repo; home/scratch/tool-results -> 'misc'."""
    base = name.split("--claude-worktrees")[0].split("--claude-projects")[0]
    if "scrips-repos-" in base:
        return base.split("scrips-repos-", 1)[1] or "misc"
    parts = base.strip("-").split("-")
    rest = parts[2:] if len(parts) > 2 else []   # drop "Users-<user>"; home root -> []
    proj = "-".join(rest)
    # collapse scratch / cloud / non-work locations into one bucket
    if not proj or proj.startswith(("private-tmp", "tmp", "var-", "Library-")):
        return "misc"
    return proj

HOME = os.path.expanduser("~")
LOG = os.path.join(HOME, ".claude", "telemetry", "events.jsonl")
PROJ_GLOB = os.path.join(HOME, ".claude", "projects", "*")

RATES = {  # USD per million tokens: [input, output, cache_write, cache_read]
    "opus":   [15.0, 75.0, 18.75, 1.50],
    "sonnet": [3.0,  15.0, 3.75,  0.30],
    "haiku":  [1.0,  5.0,  1.25,  0.10],
}
def tier(model):
    m = (model or "").lower()
    for k in RATES:
        if k in m: return k
    return None

def cost_of(u, model):
    t = tier(model)
    if not t: return 0.0
    r = RATES[t]
    return ((u.get("input_tokens",0) or 0)*r[0] + (u.get("output_tokens",0) or 0)*r[1]
          + (u.get("cache_creation_input_tokens",0) or 0)*r[2]
          + (u.get("cache_read_input_tokens",0) or 0)*r[3]) / 1_000_000

def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    by_project = {}   # project -> {input,output,cache_write,cache_read,cost}
    unknown_models = set()

    for folder in glob.glob(PROJ_GLOB):
        if not os.path.isdir(folder): continue
        proj = project_from_dir(os.path.basename(folder))
        for path in glob.glob(os.path.join(folder, "*.jsonl")):
            try:
                with open(path) as f:
                    for line in f:
                        try: o = json.loads(line)
                        except Exception: continue
                        ts = o.get("timestamp")
                        if ts:
                            try:
                                if datetime.fromisoformat(ts.replace("Z","+00:00")) < cutoff: continue
                            except Exception: pass
                        msg = o.get("message") or {}
                        u = msg.get("usage") or o.get("usage")
                        if not u: continue
                        p = by_project.setdefault(proj, {"input":0,"output":0,"cache_write":0,"cache_read":0,"cost":0.0})
                        p["input"]       += u.get("input_tokens",0) or 0
                        p["output"]      += u.get("output_tokens",0) or 0
                        p["cache_write"] += u.get("cache_creation_input_tokens",0) or 0
                        p["cache_read"]  += u.get("cache_read_input_tokens",0) or 0
                        model = msg.get("model") or o.get("model")
                        p["cost"] += cost_of(u, model)
                        if model and not tier(model): unknown_models.add(model)
            except Exception: continue

    if not by_project: return
    def tot(p): return p["input"]+p["output"]+p["cache_write"]+p["cache_read"]
    total_tokens = sum(tot(p) for p in by_project.values())
    if total_tokens == 0: return
    snap = {
        "kind":"budget","ts":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dev":git_email(),"windowDays":7,
        "totalTokens":total_tokens,
        "tokens":{k:sum(p[k] for p in by_project.values()) for k in ("input","output","cache_write","cache_read")},
        "notionalCostUsd":round(sum(p["cost"] for p in by_project.values()),2),
        "byProject":{proj:{"totalTokens":tot(p),"output":p["output"],"notionalCostUsd":round(p["cost"],2)}
                     for proj,p in sorted(by_project.items(), key=lambda x:-tot(x[1]))},
        "unknownModels":sorted(unknown_models),
    }
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG,"a") as f: f.write(json.dumps(snap)+"\n")
    print(f"budget: {total_tokens:,} tokens across {len(by_project)} projects, ~${snap['notionalCostUsd']:,.0f} notional (7d) for {snap['dev']}")

if __name__ == "__main__":
    main()
