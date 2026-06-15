#!/usr/bin/env python3
# TEAM telemetry — agent-dispatch tracker ("the talk"), tagged with the PROJECT
# the dispatch happened in (from the hook cwd). Portable: writes to a per-machine
# path (~/.claude/telemetry/events.jsonl), keyed by git email. PreToolUse:Agent.
# Never blocks.
import json, sys, os, subprocess
from pathlib import Path
from datetime import datetime

def git_email(cwd=None):
    # EFFECTIVE email (local > includeIf > global), NOT --global. Devs whose scrips
    # identity is set per-dir via includeIf would otherwise log under their personal
    # global email and show up as a stranger in the team digest. Resolve in the work
    # dir (cwd) so includeIf actually applies.
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
def main():
    out={"decision":"approve","reason":"telemetry","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":""}}
    raw=sys.stdin.read().strip()
    if raw:
        try:
            p=json.loads(raw); tin=p.get("tool_input") or p.get("toolInput") or {}
            cwd=p.get("cwd")
            LOG.parent.mkdir(parents=True,exist_ok=True)
            with LOG.open("a") as f:
                f.write(json.dumps({"kind":"dispatch","ts":datetime.now().isoformat(timespec="seconds"),
                    "dev":git_email(cwd),"project":project_from_cwd(cwd),
                    "subagent_type":tin.get("subagent_type","general-purpose"),
                    "description":tin.get("description","")[:160],"prompt_chars":len(tin.get("prompt",""))})+"\n")
        except Exception: pass
    print(json.dumps(out))
main()
