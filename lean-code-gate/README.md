# lean-code-gate (kit)

The anti-bloat CI gate. Stops agents/devs writing new code instead of refactoring/deleting — catches duplication, god-files, and additive diffs. Enforces `docs/engineering/lean-code-standard.md` (in claude-os).

## What's here
- `lean-code-check.py` — the check (duplication via jscpd, file-size budgets, additive-diff smell). Diff-mode gates only what a PR changed; audit-mode sweeps a whole repo. Exit: 0 PASS / 1 FLAG / 2 FAIL.
- `lean-code-check.yml` — GitHub Actions workflow. Blocks merge on FAIL, warns on FLAG.

**Canonical source of `lean-code-check.py` is `~/claude-os/scripts/lean-code-check.py`** — this is a vendored copy for CI distribution. The `lean-code-check` skill keeps them in sync; don't edit this copy directly.

## Adopt in a repo (per repo — team / Samer-gated, one PR each)
```
mkdir -p .github/workflows .github/scripts
cp <kit>/lean-code-check.yml  .github/workflows/lean-code-check.yml
cp <kit>/lean-code-check.py   .github/scripts/lean-code-check.py
```
Commit + open a PR. Once merged, mark the check **required** in branch protection so FAIL blocks merge.

## Run locally (pre-handback — what the sprint-runners call)
```
python3 ~/claude-os/scripts/lean-code-check.py <repo> --diff <base-ref>   # PR gate
python3 ~/claude-os/scripts/lean-code-check.py <repo>                     # whole-repo audit
```

## Tuning
Thresholds live in `THRESHOLDS` at the top of the script and mirror the standard's table. Change both together.

**Origin:** 2026-06-28 — built after a diagnostic measured FE 5.7:1 add:delete + 6.6% dup and BE 11% dup / 3,766-line PatientService.cs. See `claude-os/artifacts/agentic-os/2026-06-28-code-bloat-diagnostic.html`.
