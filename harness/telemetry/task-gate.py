#!/usr/bin/env python3
# TEAM telemetry — estimate-vs-actual capture. Portable per-dev path. Never blocks.
# PreToolUse:TaskCreate (estimatedMin) + PreToolUse:TaskUpdate completed (actualMin via metadata).
import json, sys, subprocess
from pathlib import Path
from datetime import datetime

import os
def git_email(cwd=None):
    # EFFECTIVE email (local > includeIf > global), NOT --global. See agent-track.py.
    try:
        return subprocess.run(["git","config","user.email"],capture_output=True,text=True,timeout=5,
            cwd=cwd if cwd and os.path.isdir(cwd) else None).stdout.strip() or "unknown"
    except Exception: return "unknown"

def project_from_cwd(cwd):
    if not cwd: return "unknown"
    if "/scrips-repos/" in cwd:
        seg = cwd.split("/scrips-repos/",1)[1].split("/")[0]
        return "worktree" if seg == ".worktrees" else seg
    return os.path.basename(cwd.rstrip("/")) or "unknown"

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
            cwd=p.get("cwd"); proj=meta.get("project") or project_from_cwd(cwd)
            now=datetime.now().isoformat(timespec="seconds"); dev=git_email(cwd)
            # Pair estimate↔actual by a STABLE key. The harness task id isn't known
            # pre-create, and create has no taskId while update has no subject — so a
            # caller-supplied metadata.calibrationId (the Jira ticket, e.g. PROD-1234)
            # is the only thing present on BOTH ends. Prefer it; fall back so the event
            # still records, but only calibrationId-tagged pairs actually pair up.
            if tool=="TaskCreate" and meta.get("estimatedMin") is not None:
                key = meta.get("calibrationId") or tin.get("subject","")[:80]
                log({"kind":"estimate","ts":now,"dev":dev,"project":proj,"taskId":key,
                     "estimatedMin":meta.get("estimatedMin"),"category":meta.get("category","other")})
            if tool=="TaskUpdate" and tin.get("status")=="completed" and meta.get("actualMin") is not None:
                key = meta.get("calibrationId") or tin.get("taskId")
                log({"kind":"actual","ts":now,"dev":dev,"project":proj,"taskId":key,
                     "actualMin":meta.get("actualMin"),"scopeAlignment":meta.get("scopeAlignment")})
        except Exception: pass
    print(json.dumps(out))
main()
