#!/usr/bin/env python3
"""
scan.py — high-recall candidate finder for the backend-performance-audit skill.

This is the FIND step, not the decide step. It is deliberately noisy: it points
the auditing agent at code worth reading. Every hit is a *candidate* to confirm
by reading context, not a finding. Triage happens in the skill workflow.

Usage:
    python3 scan.py --repo <path> [--stack auto|dotnet|node|sql|generic] \
                    [--out candidates.jsonl] [--max-per-pattern 0]

Output: JSONL, one object per candidate:
    {"file","line","category","stack","pattern","match","note"}

Stdlib only. Uses ripgrep (`rg`) if present for speed; otherwise walks in Python.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# Each rule: (category, regex, note). Notes carry the false-positive warning so
# the triaging agent knows what to verify. Regexes are intentionally broad.
RULES = {
    "dotnet": [
        ("DB-N+1", r"\b(foreach|for|while)\s*\(", "loop header — inspect body for a per-iteration DB call / lazy nav access"),
        ("DB-N+1", r"\.(Find|FirstOrDefault|First|SingleOrDefault|Single|Any|Count)(Async)?\s*\(", "query op — flag only if inside a loop over scaling data"),
        ("DB-unbounded", r"\.ToList(Async)?\s*\(\s*\)", "materialization — check the query is bounded (Where/Take) and table can't grow unbounded"),
        ("DB-overfetch", r"\bSELECT\s+\*", "select-* — projecting a DTO is usually cheaper; group across sites"),
        ("DB-clienteval", r"\.AsEnumerable\s*\(\s*\)|\.ToList\s*\(\s*\)\s*\.\s*(Where|Sum|GroupBy|OrderBy|Count|Select)", "possible client-side eval after materializing"),
        ("DB-index", r"LIKE\s+'%|\b(YEAR|MONTH|DAY|LOWER|UPPER|CONVERT|CAST)\s*\([^)]*\)\s*(=|>|<|LIKE)", "non-SARGable / index-defeating predicate"),
        ("DB-conn", r"new\s+(SqlConnection|DbContext|\w*DbContext)\s*\(", "connection/context construction — confirm not per-row / outside DI"),
        ("CONCURRENCY-block", r"\.Result\b|\.Wait\s*\(\s*\)|\.GetAwaiter\s*\(\s*\)\s*\.GetResult\s*\(\s*\)|Thread\.Sleep\s*\(", "sync-over-async / blocking — Critical only on a request path"),
        ("CONCURRENCY-block", r"\b(File\.ReadAllText|File\.ReadAllBytes|File\.WriteAllText|new\s+WebClient)\b", "sync I/O — flag if reachable from an async/request path"),
        ("IO-client", r"new\s+HttpClient\s*\(|new\s+SmtpClient\s*\(", "client per call → socket exhaustion; prefer IHttpClientFactory/singleton"),
        ("ALGO", r"new\s+Regex\s*\(", "regex compiled per call — hoist to static / [GeneratedRegex]"),
        ("ALGO", r"\+=\s*\"|\+=\s*\$\"", "string concat in possible loop — use StringBuilder if hot"),
        ("OBSERV", r"_logger\.(LogInformation|LogDebug|LogTrace)\s*\(\s*\$\"", "interpolated log — costly inside hot loops"),
    ],
    "node": [
        ("DB-N+1", r"\b(for|for\s*\(|\.map\s*\(\s*async|\.forEach\s*\(\s*async)\b", "loop/async-map — inspect for per-iteration query"),
        ("DB-N+1", r"\b(prisma|repository|repo|db|knex)\b\s*\.|\.(findOne|findUnique|findByPk|findFirst|query)\s*\(", "query op — flag only inside a loop over scaling data"),
        ("DB-unbounded", r"\.(findMany|findAll)\s*\(\s*\)|\bSELECT\s+\*", "unbounded read — check for take/limit/where"),
        ("CONCURRENCY-serial", r"for\s*(await)?\s*\(.*\bof\b|\bfor\s*\(", "loop — if body awaits independent work, parallelize with capped Promise.all"),
        ("CONCURRENCY-block", r"\b(readFileSync|writeFileSync|execSync|\w+Sync)\s*\(", "sync call on event loop — Critical on a request path"),
        ("IO-client", r"new\s+(http\.Agent|https\.Agent)\s*\(|axios\.create\s*\(", "client/agent — confirm reused as singleton, keep-alive, timeout set"),
        ("ALGO", r"\.(find|includes|indexOf)\s*\(", "linear search — O(n^2) if inside a loop over another array; use a Map/Set"),
        ("ALGO", r"new\s+RegExp\s*\(", "regex per call / possible ReDoS"),
        ("OBSERV", r"console\.(log|debug)\s*\(", "log call — costly inside hot loops"),
    ],
    "sql": [
        ("DB-overfetch", r"SELECT\s+\*", "select-* — name needed columns; breaks covering indexes"),
        ("DB-unbounded", r"SELECT\b(?!.*\b(TOP|OFFSET|FETCH|LIMIT)\b)", "select without row cap — check it feeds a bounded consumer"),
        ("DB-index", r"LIKE\s+'%", "leading-wildcard LIKE — cannot use a normal index"),
        ("DB-index", r"\b(YEAR|MONTH|DAY|LOWER|UPPER|CONVERT|CAST|ISNULL)\s*\([^)]*\)\s*(=|>|<|LIKE)", "function on filtered column — non-SARGable"),
        ("ALGO", r"\b(DECLARE\s+\w+\s+CURSOR|WHILE\s+@@FETCH_STATUS)\b", "cursor / row-by-row loop — prefer set-based"),
        ("ALGO", r"CREATE\s+FUNCTION", "scalar UDF — can force row-by-row eval if used in SELECT/WHERE"),
        ("DB-conn", r"\bBEGIN\s+TRAN", "transaction — confirm it doesn't span external/slow work"),
    ],
    "generic": [
        ("CONCURRENCY-block", r"\b(time\.sleep|Thread\.sleep|sleep)\s*\(", "sleep — flag if on a request path"),
        ("DB-N+1", r"\b(select_related|prefetch_related|JOIN\s+FETCH|@EntityGraph)\b", "presence/absence of eager-load hints — check ORM loops nearby"),
        ("ALGO", r"\.(apply|iterrows)\s*\(", "row-wise pandas op — vectorize if hot"),
        ("IO-client", r"new\s+RestTemplate\s*\(|requests\.(get|post|put|delete)\s*\(", "per-call HTTP — reuse a Session/client, set timeout"),
    ],
}

# Extensions worth scanning per stack (others skipped to cut noise).
EXTS = {
    "dotnet": {".cs", ".cshtml"},
    "node": {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"},
    "sql": {".sql"},
    "generic": {".cs", ".ts", ".js", ".py", ".java", ".go", ".sql", ".rb"},
}
SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", "build", ".next",
             "vendor", "__pycache__", ".venv", "venv", "packages", "migrations.bak"}


def detect_stacks(repo):
    stacks = set()
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith((".csproj", ".sln")):
                stacks.add("dotnet")
            if f == "package.json":
                stacks.add("node")
            if f.endswith(".sql"):
                stacks.add("sql")
    stacks.add("generic")  # always
    return sorted(stacks) if stacks else ["generic"]


def have_rg():
    return shutil.which("rg") is not None


def scan_with_rg(repo, stack, exts, max_per):
    out = []
    for category, pattern, note in RULES[stack]:
        globs = []
        for e in exts:
            globs += ["-g", f"*{e}"]
        cmd = ["rg", "--no-heading", "--line-number", "--color", "never",
               "-e", pattern] + globs + ["--", repo]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except Exception:
            continue
        count = 0
        for line in res.stdout.splitlines():
            # format: path:lineno:content
            parts = line.split(":", 2)
            if len(parts) < 3:
                continue
            path, lineno, content = parts
            if any(s in path.split(os.sep) for s in SKIP_DIRS):
                continue
            out.append({
                "file": os.path.relpath(path, repo), "line": int(lineno),
                "category": category, "stack": stack, "pattern": pattern,
                "match": content.strip()[:200], "note": note,
            })
            count += 1
            if max_per and count >= max_per:
                break
    return out


def scan_with_python(repo, stack, exts, max_per):
    compiled = [(c, re.compile(p, re.IGNORECASE), p, n) for c, p, n in RULES[stack]]
    counts = {}
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1] not in exts:
                continue
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    for i, content in enumerate(fh, 1):
                        for category, rx, pat, note in compiled:
                            if rx.search(content):
                                key = (category, pat)
                                if max_per and counts.get(key, 0) >= max_per:
                                    continue
                                counts[key] = counts.get(key, 0) + 1
                                out.append({
                                    "file": os.path.relpath(path, repo), "line": i,
                                    "category": category, "stack": stack,
                                    "pattern": pat, "match": content.strip()[:200],
                                    "note": note,
                                })
            except Exception:
                continue
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--stack", default="auto",
                    choices=["auto", "dotnet", "node", "sql", "generic"])
    ap.add_argument("--out", default="candidates.jsonl")
    ap.add_argument("--max-per-pattern", type=int, default=0,
                    help="cap hits per pattern (0 = unlimited)")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        sys.exit(f"not a directory: {repo}")

    stacks = detect_stacks(repo) if args.stack == "auto" else [args.stack]
    if args.stack != "auto" and args.stack != "generic":
        stacks = [args.stack, "generic"]

    use_rg = have_rg()
    all_hits = []
    for stack in stacks:
        exts = EXTS.get(stack, EXTS["generic"])
        hits = (scan_with_rg if use_rg else scan_with_python)(
            repo, stack, exts, args.max_per_pattern)
        all_hits.extend(hits)

    # de-dup identical (file,line,category)
    seen = set()
    deduped = []
    for h in all_hits:
        k = (h["file"], h["line"], h["category"])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(h)

    with open(args.out, "w", encoding="utf-8") as fh:
        for h in deduped:
            fh.write(json.dumps(h) + "\n")

    by_cat = {}
    for h in deduped:
        by_cat[h["category"]] = by_cat.get(h["category"], 0) + 1
    engine = "ripgrep" if use_rg else "python"
    print(f"[scan] repo={repo}")
    print(f"[scan] stacks={stacks} engine={engine}")
    print(f"[scan] {len(deduped)} candidates -> {args.out}")
    for c in sorted(by_cat, key=lambda x: -by_cat[x]):
        print(f"        {by_cat[c]:>5}  {c}")
    print("[scan] NOTE: candidates are high-recall and unconfirmed. "
          "Read context before recording any as a finding.")


if __name__ == "__main__":
    main()
