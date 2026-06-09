#!/usr/bin/env python3
"""
bash-destructive-gate.py
PreToolUse hook for Bash. Detects destructive commands and BLOCKS execution.
Requires explicit Samer sign-off on the specific action before proceeding.
"""
import sys
import json
import re

DESTRUCTIVE_PATTERNS = [
    (r'\baz\b.*\bdelete\b',                          "az … delete"),
    (r'\baz\b.*\bremove\b',                          "az … remove"),
    (r'\baz\b.*\bgroup\b.*\bdelete\b',               "az group delete (RG wipe)"),
    (r'\bkubectl\b.*\bdelete\b',                     "kubectl delete"),
    (r'\bkubectl\b.*\bpatch\b.*\bdelete\b',          "kubectl patch (delete)"),
    (r'\brm\s+-[a-z]*r[a-z]*f',                     "rm -rf / rm -fr"),
    (r'\bterraform\b.*\bdestroy\b',                  "terraform destroy"),
    (r'\bterraform\b.*\bapply\b',                    "terraform apply"),
    (r'\bDROP\s+(TABLE|DATABASE|SCHEMA)\b',          "SQL DROP"),
    (r'\bgh\b.*\brepo\b.*\bdelete\b',               "gh repo delete"),
    (r'\bgit\s+push\b.*--force(?:-with-lease)?',     "git push --force / --force-with-lease"),
    (r'\bgit\s+reset\b.*--hard',                     "git reset --hard"),
    (r'\bgit\s+branch\s+-[A-Za-z]*D',               "git branch -D (force-delete branch)"),
    (r'\bgit\s+clean\s+-[a-z]*f',                   "git clean -f (discard untracked files)"),
    (r'\bgit\s+(checkout|restore)\s+--\s*\.',        "git checkout/restore . (discard all local changes)"),
    (r'\bdocker\s+system\s+prune',                   "docker system prune"),
    (r'\bdocker\s+rm\s+-[a-z]*f',                   "docker rm -f"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    cmd = data.get("command", "")
    matched = []
    seen_labels = set()
    for pattern, label in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE) and label not in seen_labels:
            matched.append(label)
            seen_labels.add(label)

    if not matched:
        sys.exit(0)

    reason = (
        "INFRA GATE — DESTRUCTIVE COMMAND BLOCKED: " + ", ".join(matched) + "\n\n"
        "Before this command can run, confirm all three with Samer:\n"
        "1. What exactly will be deleted/modified? Name it specifically.\n"
        "2. Is this reversible? If no, say so explicitly.\n"
        "3. Did Samer explicitly approve THIS specific action in THIS session?\n"
        "   ('Do the cleanup' / 'handle it' is NOT approval for a specific delete.)\n\n"
        "STOP: Ask Samer for sign-off, then re-run after approval."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
