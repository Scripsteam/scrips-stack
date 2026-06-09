#!/usr/bin/env python3
"""
FHIR Architecture Auto-Trigger Hook

UserPromptSubmit hook that detects FHIR-related work and proactively
invokes the FHIR Architecture Advisor Agent.

Triggers on:
- Direct mentions: FHIR, HL7, interop, data exposure
- Data types: Patient, Observation, Encounter, Practitioner, Medication, Claim
- Patterns: "how should we expose", "sync", "federation", "source of truth"
- Regulatory: mentions of regulations + data + external consumers

Recommendation: Auto-spawn agent with assessment task.
"""

import re
import sys
import json
import os

FHIR_KEYWORDS = [
    r"\bfhir\b",
    r"\bhl7\b",
    r"\binteroperab",
    r"\bdata\s*expos",
    r"\bdata\s*syndic",
    r"\bpatient\s*record",
    r"\bclinical\s*data",
    r"\bhealth\s*record",
    r"\bobs.*interop",
]

HEALTH_PLATFORMS = [
    r"\bhealth\s*samurai\b",
    r"\baidbox\b",
    r"\bemr\b",
    r"\behr\b",
    r"\bhis\b",  # Health Information System
    r"\blims\b",  # Lab Information Management
    r"\bphr\b",  # Personal Health Record
]

RESOURCE_TYPES = [
    r"\bPatient\b",
    r"\bObservation\b",
    r"\bEncounter\b",
    r"\bPractitioner\b",
    r"\bMedication",
    r"\bClaim\b",
    r"\bCarePlan\b",
    r"\bServiceRequest\b",
]

ARCHITECTURE_PATTERNS = [
    r"how\s+should\s+we\s+(expose|structure|store|design|architect|build|model|handle)",
    r"architecture.*health",
    r"data.*model",
    r"database.*design",
    r"schema.*design",
    r"api.*design",
    r"source.*of.*truth",
    r"sync.*legacy",
    r"federation",
    r"regulated.*data",
    r"external.*consumer",
    r"rewrite.*application",
    r"backend.*work",
    r"backend.*architecture",
    r"data.*migration",
]

BACKEND_PATTERNS = [
    r"\bbackend\b",
    r"\bserver\s*architecture",
    r"\bapi\s*(design|arch)",
    r"\bdatabase.*schema",
    r"\bdata.*model",
    r"\bintegrat.*system",
    r"\bdata.*layer",
]

def should_trigger(prompt):
    """Determine if FHIR advisor should be invoked."""
    prompt_lower = prompt.lower()

    # Check for direct FHIR mention
    for keyword in FHIR_KEYWORDS:
        if re.search(keyword, prompt_lower):
            return True, "FHIR/HL7 keyword detected"

    # Check for health platforms (Health Samurai, Aidbox, EMR, EHR, etc.)
    for platform in HEALTH_PLATFORMS:
        if re.search(platform, prompt_lower):
            return True, f"Health platform mentioned (could involve healthcare data)"

    # Check for resource types
    for resource in RESOURCE_TYPES:
        if re.search(resource, prompt):  # Case-sensitive for resource types
            return True, "FHIR resource type mentioned"

    # Check for architecture patterns (any architectural decision)
    for pattern in ARCHITECTURE_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True, "Architecture decision pattern detected (could involve healthcare data)"

    # Check for backend/data work patterns
    for pattern in BACKEND_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True, "Backend/data work detected (could involve healthcare data)"

    return False, None

def main():
    try:
        # Read stdin (Claude will provide the prompt)
        prompt = sys.stdin.read().strip()
    except:
        sys.exit(0)

    should_fire, reason = should_trigger(prompt)

    if not should_fire:
        sys.exit(0)

    # Output hook recommendation
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"""
FHIR ARCHITECTURE ADVISOR — Auto-triggered

Reason: {reason}

This prompt involves healthcare data, interoperability, or regulatory exposure.
Proactively assess architecture NOW before design locks in.

Next step: The FHIR Architecture Advisor agent will assess the 9 clarification
questions and recommend a model (Facade / Hybrid / FHIR-native) + phase plan.

See: ADR-FHIR-001 (Scrips Vault) for the full decision framework.
""".strip()
        }
    }

    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
