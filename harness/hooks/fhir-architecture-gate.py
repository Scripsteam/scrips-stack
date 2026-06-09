#!/usr/bin/env python3
"""
FHIR Architecture Gate Hook

Pre-commit hook that validates FHIR-related changes against ADR-FHIR-001.

Rules enforced:
1. Any commit touching FHIR server code or resource definitions must reference
   ADR-FHIR-001 or a FHIR-specific ADR in the commit message.
2. Commits must document source-of-truth ownership for any new FHIR resource types.
3. Sync/federation changes must reference an architectural decision before merging.

Violations block commit; warnings are logged but non-blocking.
"""

import os
import sys
import re
from pathlib import Path

FHIR_PATTERNS = [
    r"fhir",
    r"hl7",
    r"resource-definition",
    r"sync-pipeline",
    r"cdc",
    r"change-data-capture",
    r"facade",
    r"hybrid",
    r"observation|patient|encounter|practitioner",  # Common FHIR resource types
]

ADR_PATTERN = r"ADR-FHIR-\d+|ADR-\d+\s*\(FHIR"

def get_staged_files():
    """Get list of staged files from git."""
    result = os.popen("git diff --cached --name-only").read().strip().split("\n")
    return [f for f in result if f]

def get_commit_message():
    """Get the commit message being prepared."""
    try:
        with open(os.path.expanduser("~/.git/COMMIT_EDITMSG"), "r") as f:
            return f.read()
    except:
        return ""

def is_fhir_change(file_path):
    """Check if file is FHIR-related."""
    content = ""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return False

    # Check filename
    if any(re.search(p, file_path, re.IGNORECASE) for p in FHIR_PATTERNS):
        return True

    # Check file content
    if any(re.search(p, content, re.IGNORECASE) for p in FHIR_PATTERNS):
        return True

    return False

def check_adr_reference(message):
    """Check if commit message references a FHIR ADR."""
    return bool(re.search(ADR_PATTERN, message, re.IGNORECASE))

def check_source_of_truth_documented(files):
    """
    Check if source-of-truth is documented for FHIR resource types.
    Look for comments or docstrings that identify ownership.
    """
    warnings = []

    for file_path in files:
        if not is_fhir_change(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Check for resource definitions without ownership docs
            if re.search(r"class\s+\w+Resource|def\s+\w+_resource|fhir.*resource", content, re.IGNORECASE):
                if not re.search(r"source.of.truth|owned.by|master.data|sync", content, re.IGNORECASE):
                    warnings.append(f"  ⚠ {file_path}: Resource definition lacks source-of-truth documentation")
        except:
            pass

    return warnings

def main():
    files = get_staged_files()
    message = get_commit_message()

    fhir_files = [f for f in files if is_fhir_change(f)]

    if not fhir_files:
        sys.exit(0)  # No FHIR changes, pass

    errors = []
    warnings = []

    # Rule 1: Check for ADR reference
    if not check_adr_reference(message):
        errors.append("✗ FHIR change detected but commit message lacks ADR reference.")
        errors.append("  Add one of: ADR-FHIR-001, ADR-FHIR-002, or reference the relevant architecture decision.")

    # Rule 2: Check source-of-truth documentation
    sot_warnings = check_source_of_truth_documented(fhir_files)
    warnings.extend(sot_warnings)

    # Output
    if warnings:
        print("\nFHIR Architecture Gate — Warnings:")
        for w in warnings:
            print(w)
        print()

    if errors:
        print("\nFHIR Architecture Gate — Blocked:")
        for e in errors:
            print(e)
        print("\nReference: ~/.claude/skills/fhir-architecture-assessment.md")
        print("Decision framework: Scrips Vault > 06-decisions > ADR-FHIR-001\n")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
