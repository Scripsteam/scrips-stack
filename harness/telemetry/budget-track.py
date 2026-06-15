#!/usr/bin/env python3
# TEAM telemetry — budget tracker (tokens + notional $). Harvests per-message
# token usage that Claude Code already records in its local transcripts — so NO
# OTEL collector is needed. Appends a rolling 7-day snapshot to events.jsonl,
# keyed by git email; push.sh ships it; aggregate.py rolls it up. Never blocks.
#
# Cost is NOTIONAL — Anthropic API list rates applied to measured tokens. It is a
# DERIVED figure for relative comparison, not a billing actual (Claude Code may be
# on a subscription plan). The digest labels it as such.
import json, os, glob, subprocess
from datetime import datetime, timedelta, timezone

def git_email():
    try: return subprocess.run(["git","config","--global","user.email"],capture_output=True,text=True,timeout=5).stdout.strip() or "unknown"
    except Exception: return "unknown"

HOME = os.path.expanduser("~")
LOG = os.path.join(HOME, ".claude", "telemetry", "events.jsonl")
TX_GLOB = os.path.join(HOME, ".claude", "projects", "*", "*.jsonl")

# Anthropic list rates, USD per million tokens: [input, output, cache_write, cache_read]
RATES = {
    "opus":   [15.0, 75.0, 18.75, 1.50],
    "sonnet": [3.0,  15.0, 3.75,  0.30],
    "haiku":  [1.0,  5.0,  1.25,  0.10],
}
def tier(model):
    m = (model or "").lower()
    for k in RATES:
        if k in m: return k
    return None  # unknown model — tokens counted, cost left out (flagged)

def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    tok = {"input":0,"output":0,"cache_write":0,"cache_read":0}
    by_model = {}
    cost = 0.0
    unknown_models = set()
    for path in glob.glob(TX_GLOB):
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
                    i  = u.get("input_tokens",0) or 0
                    ot = u.get("output_tokens",0) or 0
                    cw = u.get("cache_creation_input_tokens",0) or 0
                    cr = u.get("cache_read_input_tokens",0) or 0
                    tok["input"]+=i; tok["output"]+=ot; tok["cache_write"]+=cw; tok["cache_read"]+=cr
                    model = msg.get("model") or o.get("model")
                    t = tier(model)
                    bm = by_model.setdefault(model or "unknown", {"input":0,"output":0,"cache_write":0,"cache_read":0})
                    bm["input"]+=i; bm["output"]+=ot; bm["cache_write"]+=cw; bm["cache_read"]+=cr
                    if t:
                        r = RATES[t]
                        cost += (i*r[0] + ot*r[1] + cw*r[2] + cr*r[3]) / 1_000_000
                    elif model:
                        unknown_models.add(model)
        except Exception: continue

    total_tokens = sum(tok.values())
    if total_tokens == 0:
        return  # nothing to report this window
    snap = {
        "kind":"budget","ts":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dev":git_email(),"windowDays":7,"tokens":tok,"totalTokens":total_tokens,
        "notionalCostUsd":round(cost,2),"unknownModels":sorted(unknown_models),
    }
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG,"a") as f: f.write(json.dumps(snap)+"\n")
    print(f"budget: {total_tokens:,} tokens, ~${cost:,.2f} notional (7d) for {snap['dev']}")

if __name__ == "__main__":
    main()
