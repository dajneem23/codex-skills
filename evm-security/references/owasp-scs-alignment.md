# OWASP SCS Alignment (SCSVS, SCSTG, SCWE)

Use this file to align EVM audits to OWASP Smart Contract Security guidance from:
- https://github.com/OWASP/owasp-scs
- https://scs.owasp.org

This reference is intentionally concise. Use it as a tagging and coverage framework, not a replacement for protocol-specific threat modeling.

## 1) Smart Contract Top 10 (2026) Tags

Tag findings with one of these when applicable:
- `SC01` Access Control Vulnerabilities
- `SC02` Price Oracle Manipulation
- `SC03` Logic Errors
- `SC04` Lack of Input Validation
- `SC05` Reentrancy
- `SC06` Unchecked External Calls
- `SC07` Flash Loan Attacks
- `SC08` Integer Overflow and Underflow
- `SC09` Insecure Randomness
- `SC10` Denial of Service

## 2) SCSVS Coverage Areas

Use these domains as a coverage checklist for audit scoping and reporting:
- `S1` Architecture, Design and Threat Modeling
- `S2` Code
- `S3` Governance and Access Control
- `S4` Authentication, Authorization and Identity
- `S5` Business Logic and Economic Security
- `S6` Cryptography and Secrets Management
- `S7` Components and Dependencies
- `S8` Oracle and Data Feeds
- `S9` Bridge and Cross-Chain Security
- `S10` DeFi and Financial Components
- `S11` Testing and Verification
- `S12` Documentation and Observability

Minimum practice:
1. Mark each domain as `Reviewed`, `Partially Reviewed`, or `Not in Scope`.
2. Convert every `Partially Reviewed` safety assumption into a test requirement or residual-risk note.

## 3) SCSTG Test Areas for EVM Reviews

Use SCSTG test IDs to link findings and recommended tests.
Prefer exact IDs from the official SCSTG checklist page when you can map confidently.

Examples of high-signal SCSTG anchors:
- `SCSTG-TEST-0001` Verify secure implementation of multi-signature controls.
- `SCSTG-TEST-0004` Verify contract implementation against common vulnerability classes.
- `SCSTG-TEST-0012` Verify token contract implementation.
- `SCSTG-TEST-0013` Verify secure implementation of cryptographic signature verification.
- `SCSTG-TEST-0014` Test gas usage in loops and max iterations.
- `SCSTG-TEST-0016` Test arithmetic and logic security.

When exact IDs are unclear, tag the closest SCSTG family and avoid inventing IDs.

## 4) SCWE Weakness Tagging

Add SCWE IDs to findings when there is a direct weakness mapping.

High-signal mappings:
- Missing/weak authorization -> SCWE access-control family
- Reentrancy or callback state corruption -> SCWE reentrancy/call-ordering family
- Oracle freshness/confidence validation gaps -> SCWE oracle validation family
- Arithmetic overflow/underflow/precision bugs -> SCWE arithmetic family
- Unchecked external call outcomes -> SCWE external-call handling family

Rule:
- Only tag an SCWE ID if the behavior clearly matches the weakness definition.
- If uncertain, keep Top10 + SCSVS tags and omit SCWE ID.

## 5) Reporting Template Add-on

For each finding, append:
- `OWASP Top10`: `SCxx` (if applicable)
- `SCSVS`: `Sx` domain(s)
- `SCSTG`: test ID or family
- `SCWE`: weakness ID (optional, only when confident)

Example:
- OWASP Top10: `SC05 Reentrancy`
- SCSVS: `S2 Code`, `S5 Business Logic and Economic Security`
- SCSTG: `SCSTG-TEST-0023` family (external interactions)
- SCWE: mapped reentrancy weakness ID
