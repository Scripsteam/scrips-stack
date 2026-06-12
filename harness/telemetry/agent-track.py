#!/usr/bin/env python3
# TEAM telemetry — agent-dispatch tracker ("the talk"). Portable: writes to a
# standard per-machine path (~/.claude/telemetry/events.jsonl), keyed by git email.
# PreToolUse:Agent. Never blocks.
import json, sys, subprocess
from pathlib import Path
from datetime import datetime

def git_email():
    # EFFECTIVE email (local > includeIf > global), NOT --global. Devs whose scrips
    # identity is set per-dir via includeIf would otherwise log under their personal
    # global email and show up as a stranger in the team digest.
    try: return subprocess.run(["git","config","user.email"],capture_output=True,text=True,timeout=5).stdout.strip() or "unknown"
    except Exception: return "unknown"

LOG = Path.home() / ".claude" / "telemetry" / "events.jsonl"
def main():
    out={"decision":"approve","reason":"telemetry","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":""}}
    raw=sys.stdin.read().strip()
    if raw:
        try:
            p=json.loads(raw); tin=p.get("tool_input") or p.get("toolInput") or {}
            LOG.parent.mkdir(parents=True,exist_ok=True)
            with LOG.open("a") as f:
                f.write(json.dumps({"kind":"dispatch","ts":datetime.now().isoformat(timespec="seconds"),
                    "dev":git_email(),"subagent_type":tin.get("subagent_type","general-purpose"),
                    "description":tin.get("description","")[:160],"prompt_chars":len(tin.get("prompt",""))})+"\n")
        except Exception: pass
    print(json.dumps(out))
main()
