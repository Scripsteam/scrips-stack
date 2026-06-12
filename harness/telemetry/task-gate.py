#!/usr/bin/env python3
# TEAM telemetry — estimate-vs-actual capture. Portable per-dev path. Never blocks.
# PreToolUse:TaskCreate (estimatedMin) + PreToolUse:TaskUpdate completed (actualMin via metadata).
import json, sys, subprocess
from pathlib import Path
from datetime import datetime

def git_email():
    # EFFECTIVE email (local > includeIf > global), NOT --global. See agent-track.py.
    try: return subprocess.run(["git","config","user.email"],capture_output=True,text=True,timeout=5).stdout.strip() or "unknown"
    except Exception: return "unknown"

LOG = Path.home() / ".claude" / "telemetry" / "events.jsonl"
def log(d):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    with LOG.open("a") as f: f.write(json.dumps(d)+"\n")
def main():
    out={"decision":"approve","reason":"telemetry","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":""}}
    raw=sys.stdin.read().strip()
    if raw:
        try:
            p=json.loads(raw); tool=p.get("tool_name") or p.get("toolName"); tin=p.get("tool_input") or {}
            meta=tin.get("metadata") or {}
            now=datetime.now().isoformat(timespec="seconds"); dev=git_email()
            if tool=="TaskCreate" and meta.get("estimatedMin") is not None:
                log({"kind":"estimate","ts":now,"dev":dev,"taskId":tin.get("subject","")[:80],
                     "estimatedMin":meta.get("estimatedMin"),"category":meta.get("category","other")})
            if tool=="TaskUpdate" and tin.get("status")=="completed" and meta.get("actualMin") is not None:
                log({"kind":"actual","ts":now,"dev":dev,"taskId":tin.get("taskId"),
                     "actualMin":meta.get("actualMin"),"scopeAlignment":meta.get("scopeAlignment")})
        except Exception: pass
    print(json.dumps(out))
main()
