#!/usr/bin/env python3
"""
lean-code-check — anti-bloat gate for Scrips repos (FE TS/React + BE .NET).
Enforces docs/engineering/lean-code-standard.md.

Usage:
  lean-code-check.py <repo-path> [--diff <base-ref>] [--json] [--quiet] [--suggest]

Flags:
  --diff <ref>  Gate only what this PR/branch changed vs <ref> (e.g. origin/main).
  --suggest     Print a concrete fix suggestion for every FLAG and FAIL finding.
  --json        Machine-readable output (includes suggestions[] when --suggest is set).
  --quiet       Suppress all output (exit code only).

Exit code: 0 = PASS, 1 = FLAG (reviewer override w/ reason), 2 = FAIL (block).
Duplication needs `npx jscpd` (auto-fetched); if unavailable it is reported UNMEASURED,
never silently passed.
"""
import sys, os, subprocess, json, tempfile, argparse, glob

THRESHOLDS = {
    "dup_flag_pct": 5.0, "dup_fail_pct": 10.0,
    "fe_file_flag": 600, "fe_file_fail": 1000,
    "be_file_flag": 800, "be_file_fail": 1200, "be_controller_flag": 500,
    "diff_additive_add_min": 150,     # adds >= this with 0 deletions = additive smell
    "churn_ratio_flag": 4.0,          # repo-mode add:delete ratio
}
SIZE_EXEMPT_FAIL = ("/types/", "-api.ts", ".d.ts")  # large-by-nature; reported, not failed

def sh(cmd, cwd=None, timeout=600):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return 1, "", str(e)

def detect_stack(repo):
    if glob.glob(os.path.join(repo, "**", "*.csproj"), recursive=True): return "be"
    if os.path.exists(os.path.join(repo, "package.json")): return "fe"
    if glob.glob(os.path.join(repo, "**", "*.cs"), recursive=True): return "be"
    return "fe"

def source_files(repo, stack):
    out = []
    if stack == "fe":
        root = os.path.join(repo, "src") if os.path.isdir(os.path.join(repo, "src")) else repo
        for dp, _, fs in os.walk(root):
            if "node_modules" in dp or "/dist/" in dp: continue
            for f in fs:
                if f.endswith((".ts", ".tsx")) and not f.endswith((".test.ts",".test.tsx",".spec.ts",".spec.tsx")):
                    out.append(os.path.join(dp, f))
    else:
        for dp, _, fs in os.walk(repo):
            if any(x in dp for x in ("/bin/","/obj/","/Connected Services/","/Migrations/")) or "Tests" in dp or "UnitTests" in dp: continue
            for f in fs:
                if f.endswith(".cs") and not f.endswith((".g.cs",)) and f != "Reference.cs":
                    out.append(os.path.join(dp, f))
    return out

def check_duplication(repo, stack):
    with tempfile.TemporaryDirectory() as td:
        target = os.path.join(repo, "src") if (stack=="fe" and os.path.isdir(os.path.join(repo,"src"))) else repo
        ign = ("**/node_modules/**,**/dist/**,**/*.test.*,**/*.spec.*,**/*.generated.*,**/*.d.ts" if stack=="fe"
               else "**/bin/**,**/obj/**,**/*Tests*/**,**/*UnitTests*/**,**/Connected Services/**,**/Reference.cs,**/*.g.cs,**/Migrations/**")
        fmt = "typescript,tsx,jsx" if stack=="fe" else "csharp"
        code,out,err = sh(["npx","--yes","jscpd",target,"--min-lines","10","--reporters","json",
                           "--output",td,"--silent","--format",fmt,"--ignore",ign], timeout=600)
        rep = os.path.join(td,"jscpd-report.json")
        if os.path.exists(rep):
            try:
                tot = json.load(open(rep)).get("statistics",{}).get("total",{})
                return {"measured":True,"pct":round(tot.get("percentage",0),2),"clones":tot.get("clones",0)}
            except Exception: pass
    return {"measured":False,"pct":None,"clones":None}

def check_sizes(repo, stack):
    flag, fail = [], []
    ff, fl = (THRESHOLDS["fe_file_flag"],THRESHOLDS["fe_file_fail"]) if stack=="fe" else (THRESHOLDS["be_file_flag"],THRESHOLDS["be_file_fail"])
    for p in source_files(repo, stack):
        try: n = sum(1 for _ in open(p,encoding="utf-8",errors="ignore"))
        except Exception: continue
        rel = os.path.relpath(p, repo)
        budget_flag = THRESHOLDS["be_controller_flag"] if (stack=="be" and p.endswith("Controller.cs")) else ff
        if n > fl and not (stack=="fe" and any(x in p for x in SIZE_EXEMPT_FAIL)):
            fail.append((rel,n))
        elif n > budget_flag:
            flag.append((rel,n))
    flag.sort(key=lambda x:-x[1]); fail.sort(key=lambda x:-x[1])
    return flag, fail

def check_dupe_named(repo, stack):
    pats = []
    exts = ("ts","tsx") if stack=="fe" else ("cs",)
    import re
    rx = re.compile(r'[-_.](v[0-9]|copy|old|new|backup|bak|legacy|deprecated|duplicate|original)\.(%s)$' % "|".join(exts), re.I)
    for p in source_files(repo, stack):
        if rx.search(os.path.basename(p)): pats.append(os.path.relpath(p,repo))
    return pats

def git_numstat(repo, args):
    code,out,_ = sh(["git","-C",repo,"log" if "log" in args else "diff"]+args)
    return out

def check_churn(repo):
    code,out,_ = sh(["git","-C",repo,"log","-80","--numstat","--pretty=tformat:"])
    add=dele=0
    for line in out.splitlines():
        parts=line.split("\t")
        if len(parts)==3 and parts[0].isdigit() and parts[1].isdigit():
            add+=int(parts[0]); dele+=int(parts[1])
    ratio = round(add/dele,1) if dele else float(add)
    return {"added":add,"deleted":dele,"ratio":ratio}

def check_diff(repo, base):
    code,out,_ = sh(["git","-C",repo,"diff","--numstat",f"{base}...HEAD"])
    add=dele=0
    for line in out.splitlines():
        parts=line.split("\t")
        if len(parts)>=3 and parts[0].isdigit() and parts[1].isdigit():
            add+=int(parts[0]); dele+=int(parts[1])
    code,out2,_ = sh(["git","-C",repo,"diff","--name-status",f"{base}...HEAD"])
    A=sum(1 for l in out2.splitlines() if l.startswith("A\t")); M=sum(1 for l in out2.splitlines() if l.startswith("M\t"))
    return {"added":add,"deleted":dele,"new_files":A,"modified_files":M}

def make_suggestions(findings, fsize, failsize, dn, dup, churn_data, diff_data, stack):
    """Return a list of concrete, file-specific fix suggestions for every FLAG/FAIL."""
    suggestions = []
    size_done = False  # emit size suggestions once, even if both FLAG and FAIL fire
    for sev, msg in findings:
        if sev not in ("FLAG","FAIL"): continue

        if "duplication" in msg and "%" in msg:
            suggestions.append(
                "Duplication: run `npx jscpd src/ --min-lines 10 --reporters console` to see exact "
                "clone pairs, then extract shared logic into a util/hook/service. "
                "Target: pull each clone group into one shared file before the next PR."
            )

        elif ("hard size cap" in msg or "size budget" in msg) and not size_done:
            size_done = True
            seen_files = set()
            all_over = []
            for item in (failsize + fsize):
                if item[0] not in seen_files:
                    seen_files.add(item[0]); all_over.append(item)
            all_over.sort(key=lambda x: -x[1])
            for rel, lines in all_over[:3]:
                name = os.path.basename(rel)
                if stack == "fe":
                    if "types" in rel or rel.endswith((".d.ts","-api.ts")):
                        suggestions.append(
                            f"Large type file `{rel}` ({lines} lines): split by domain — "
                            f"e.g. `{name.replace('.ts','-core.ts')}` (shared primitives) + one file per entity. "
                            "Type files are exempt from FAIL but not from review."
                        )
                    else:
                        suggestions.append(
                            f"God file `{rel}` ({lines} lines): identify cohesive slices and extract each to its own file. "
                            f"Start with the largest logical group (e.g. a sub-form, a modal, a section). "
                            f"Target: no file over {1000 if stack=='fe' else 1200} lines."
                        )
                else:
                    suggestions.append(
                        f"God class `{rel}` ({lines} lines): extract one responsibility per PR — "
                        "start with private helpers that don't depend on instance state (move to a static helper class). "
                        f"Controllers: split by resource group. Services: extract a domain sub-service. "
                        f"Target: ≤800 lines (≤500 for Controllers)."
                    )

        elif "additive smell" in msg and diff_data:
            a_add = diff_data.get("added",0)
            suggestions.append(
                f"Additive diff (+{a_add} / -0): this PR adds code without removing what it replaces. "
                "Before merging: (1) grep for old implementation names and delete them, "
                "(2) check if any file the PR touches had a prior version — delete it in the same PR. "
                "Target add:delete ratio ≤ 2:1."
            )

        elif "churn" in msg and churn_data:
            ratio = churn_data.get("ratio", 0)
            suggestions.append(
                f"Repo churn {ratio}:1 (last 80 commits): the repo is growing faster than it shrinks. "
                "Next sprint: for every new feature, delete the code it supersedes in the same PR. "
                "Consider a dedicated 'delete sprint' targeting the top 5 god files identified above."
            )

        elif "duplicate-named" in msg:
            suggestions.append(
                f"Duplicate-named files ({msg}): delete the stale copy or merge and remove it. "
                "A file named `.old`, `.copy`, `.backup`, or `.legacy` is a sign the refactor wasn't finished."
            )

    return suggestions


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo"); ap.add_argument("--diff",default=None)
    ap.add_argument("--json",action="store_true"); ap.add_argument("--quiet",action="store_true")
    ap.add_argument("--suggest",action="store_true")
    a=ap.parse_args()
    repo=os.path.abspath(os.path.expanduser(a.repo))
    if not os.path.isdir(repo): print(f"no such repo: {repo}"); sys.exit(2)
    stack=detect_stack(repo)
    mode = "diff" if a.diff else "audit"
    findings=[]; verdict="PASS"
    def bump(v):
        nonlocal verdict
        order={"PASS":0,"FLAG":1,"FAIL":2}
        if order[v]>order[verdict]: verdict=v

    # touched files (diff mode) — gate only on what the PR changed
    touched=set()
    if mode=="diff":
        _,ns,_=sh(["git","-C",repo,"diff","--name-status",f"{a.diff}...HEAD"])
        for l in ns.splitlines():
            p=l.split("\t")
            if len(p)>=2 and p[0][0] in ("A","M"): touched.add(p[-1])

    dup=check_duplication(repo,stack)
    if not dup["measured"]:
        findings.append(("WARN","duplication UNMEASURED (jscpd unavailable) — do not read as clean"))
    elif mode=="diff":
        findings.append(("INFO",f"repo duplication {dup['pct']}% ({dup['clones']} clones) — baseline, not gated on a diff"))
    else:
        if dup["pct"]>=THRESHOLDS["dup_fail_pct"]: bump("FAIL"); findings.append(("FAIL",f"duplication {dup['pct']}% ({dup['clones']} clones) ≥ {THRESHOLDS['dup_fail_pct']}%"))
        elif dup["pct"]>=THRESHOLDS["dup_flag_pct"]: bump("FLAG"); findings.append(("FLAG",f"duplication {dup['pct']}% ({dup['clones']} clones) ≥ {THRESHOLDS['dup_flag_pct']}%"))
        else: findings.append(("OK",f"duplication {dup['pct']}% ({dup['clones']} clones)"))

    fsize,failsize=check_sizes(repo,stack)
    if mode=="diff":
        tf=[x for x in failsize if x[0] in touched]; tfl=[x for x in fsize if x[0] in touched]
        if tf: bump("FAIL"); findings.append(("FAIL",f"{len(tf)} file(s) THIS DIFF touched over hard size cap: {tf[0][0]} ({tf[0][1]} lines)"))
        if tfl: bump("FLAG"); findings.append(("FLAG",f"{len(tfl)} file(s) THIS DIFF touched over size budget: {tfl[0][0]} ({tfl[0][1]} lines)"))
        if not tf and not tfl: findings.append(("OK","no touched file over size budget"))
        if failsize or fsize: findings.append(("INFO",f"repo baseline: {len(failsize)} over cap / {len(fsize)} over budget (pre-existing, not gated)"))
    else:
        if failsize: bump("FAIL"); findings.append(("FAIL",f"{len(failsize)} file(s) over hard size cap, largest: {failsize[0][0]} ({failsize[0][1]} lines)"))
        if fsize: bump("FLAG"); findings.append(("FLAG",f"{len(fsize)} file(s) over size budget, largest: {fsize[0][0]} ({fsize[0][1]} lines)"))
        if not fsize and not failsize: findings.append(("OK","all files within size budget"))

    dn=check_dupe_named(repo,stack)
    dn_gate = [x for x in dn if x in touched] if mode=="diff" else dn
    if dn_gate: bump("FAIL"); findings.append(("FAIL",f"{len(dn_gate)} duplicate-named file(s): {', '.join(dn_gate[:3])}"))

    extra={}
    if mode=="diff":
        d=check_diff(repo,a.diff); extra["diff"]=d
        if d["deleted"]==0 and d["added"]>=THRESHOLDS["diff_additive_add_min"]:
            bump("FLAG"); findings.append(("FLAG",f"additive smell: +{d['added']} / -0 lines (added without changing/removing anything)"))
        else:
            findings.append(("OK",f"diff +{d['added']} / -{d['deleted']}, {d['new_files']} new / {d['modified_files']} modified files"))
    else:
        c=check_churn(repo); extra["churn"]=c
        if c["ratio"]>=THRESHOLDS["churn_ratio_flag"]:
            bump("FLAG"); findings.append(("FLAG",f"repo add:delete churn {c['ratio']}:1 (+{c['added']}/-{c['deleted']}, last 80 commits) ≥ {THRESHOLDS['churn_ratio_flag']}:1"))
        else:
            findings.append(("OK",f"repo churn {c['ratio']}:1 (+{c['added']}/-{c['deleted']})"))

    churn_data = extra.get("churn")
    diff_data  = extra.get("diff")
    suggestions = make_suggestions(findings, fsize, failsize, dn, dup, churn_data, diff_data, stack) if a.suggest else []

    result={"repo":os.path.basename(repo),"stack":stack,"verdict":verdict,
            "duplication":dup,"size_flag":len(fsize),"size_fail":len(failsize),
            "dupe_named":dn,"findings":findings,**extra}
    if suggestions:
        result["suggestions"] = suggestions

    if a.json:
        print(json.dumps(result,indent=2))
    elif not a.quiet:
        icon={"PASS":"✅","FLAG":"🟠","FAIL":"🔴"}[verdict]
        print(f"\n{icon} lean-code-check  {result['repo']} [{stack.upper()}]  →  {verdict}")
        for sev,msg in findings:
            mark={"OK":"  ·","FLAG":"  🟠","FAIL":"  🔴","WARN":"  ⚠️","INFO":"  ℹ️"}.get(sev,"  ·")
            print(f"{mark} {msg}")
        if suggestions:
            print(f"\n  ── Fix suggestions ──")
            for i, s in enumerate(suggestions, 1):
                print(f"  {i}. {s}")
        print(f"\n  standard: docs/engineering/lean-code-standard.md")
    sys.exit({"PASS":0,"FLAG":1,"FAIL":2}[verdict])

if __name__=="__main__":
    main()
