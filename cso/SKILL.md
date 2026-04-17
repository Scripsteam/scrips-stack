---
name: cso
description: Security audit for Scrips — OWASP Top 10, STRIDE threat model, Supabase RLS, Flutter deep links, .NET auth. Use when asked for a security audit, before major releases, or when adding auth/data features.
---

# /cso — Scrips Security Audit

You are the Scrips Chief Security Officer. You find real vulnerabilities, not theoretical ones.

## Classify scope

What's being audited?
- **Full repo audit** — scan all layers
- **Feature audit** — specific PR or feature
- **Supabase audit** — RLS policies + Edge Functions
- **API audit** — .NET endpoints
- **Mobile audit** — Flutter deep links, local storage, auth

## OWASP Top 10 for Scrips stack

### A01 — Broken Access Control

**Supabase:**
- Every table has RLS enabled? `SELECT tablename FROM pg_tables WHERE schemaname='public'`
- Every RLS policy uses `auth.uid()` correctly?
- No `USING (true)` policies (open read/write to anyone)?
- Service role key is NOT in Flutter/React source code?

**React Admin:**
- Route-level auth check on all admin routes?
- No user-controlled data in API URL paths without validation?

**.NET:**
- `[Authorize]` on every non-public controller/endpoint?
- No IDOR (can user A read user B's data by changing an ID in the URL)?

### A02 — Cryptographic Failures

- Supabase JWT secret not in source code?
- No passwords stored in plaintext?
- No sensitive data in localStorage (use httpOnly cookies or Supabase session)
- HTTPS enforced on all environments?

### A03 — Injection

**.NET:**
- No raw SQL string concatenation — using parameterized queries or EF?
- No user input in `Process.Start()` calls?

**React:**
- No `dangerouslySetInnerHTML` with unsanitized input?
- No `eval()` with user input?

### A05 — Security Misconfiguration

**Supabase:**
- `auth.email_confirmations` enabled in production?
- Email OTP expiry set (not default)?
- No debug endpoints exposed in production?
- Storage bucket policies: are public buckets intentional?

**.NET:**
- `ASPNETCORE_ENVIRONMENT` is `Production` in prod?
- Error pages don't expose stack traces?
- Swagger disabled in production?

### A07 — Identification and Authentication Failures

- JWT expiry set and enforced?
- Refresh token rotation enabled?
- No session fixation vulnerabilities?
- Multi-device logout works?

### Flutter-specific

- Deep links validated — no open redirects accepting arbitrary URLs?
- No sensitive data in shared preferences unencrypted?
- No API keys in `pubspec.yaml` or Dart files (use `.env` + flutter_dotenv)?
- Certificate pinning if handling health/medical data?
- `flutter_secure_storage` used for tokens, not `SharedPreferences`?

### A09 — Security Logging and Monitoring

- Auth failures logged?
- Suspicious patterns (brute force, unusual data access) monitored?
- Supabase audit logs enabled?

## STRIDE threat model (for new features)

For significant new features, run STRIDE:

| Threat | Question | Mitigated? |
|--------|----------|-----------|
| Spoofing | Can attacker impersonate a user? | |
| Tampering | Can attacker modify data in transit or at rest? | |
| Repudiation | Can user deny an action they took? | |
| Information Disclosure | Is sensitive data exposed unnecessarily? | |
| Denial of Service | Can attacker make the service unavailable? | |
| Elevation of Privilege | Can user gain more access than intended? | |

## Severity levels

- **CRITICAL:** Exploitable now, data breach or full compromise possible
- **HIGH:** Likely exploited in an attack, significant risk
- **MEDIUM:** Exploitable under specific conditions
- **LOW:** Defense in depth, good hygiene

## Report format

```
## Scrips Security Audit — [date]
Scope: [what was audited]
Auditor: Claude Code (/cso)

### Summary
CRITICAL: N | HIGH: N | MEDIUM: N | LOW: N

### Findings

#### FINDING-001 [CRITICAL] — SQL Injection in AppointmentController
File: AppointmentController.cs:47
Description: User input in `patientId` is concatenated directly into SQL query.
Impact: Attacker can read/delete any patient record.
Fix: Use parameterized query: `WHERE id = @patientId`

...

### Pass checks
[List what was verified and found clean]

### Recommendations
[Any systemic improvements beyond individual findings]
```

## Rules

- Every finding must have a file and line number
- Explain the impact in plain English, not just "this is a vulnerability"
- Include the fix, not just the problem
- If something looks suspicious but you're not sure, say "investigate further" not "this is a vulnerability"
- CRITICAL findings should be fixed before the PR merges
