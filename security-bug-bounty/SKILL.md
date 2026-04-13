---
name: "security-bug-bounty"
description: "Guide users through preparing, submitting, and following up on security bug bounty reports. Trigger when the user asks about writing or filing a bug bounty report, wants triage advice, or needs to structure impact/reproduction details for coordinated disclosure or platform submissions."
---

# Security Bug Bounty

## Overview
Provide a structured flow to capture exploitability, impact, reproduction, and remediation for bug bounty submissions. Focus on clarity, minimal repro steps, and evidence (logs, PoCs, screenshots). Default to responsible disclosure and respect program rules.

## Workflow
1) Scope check
- Confirm target program, allowed attack surface, exclusions, and testing environment (staging vs mainnet/main prod). Decline off-scope or forbidden actions.

2) Issue characterization
- Identify vulnerability class (auth, accounting, oracle, replay, reentrancy, dos, upgrade, web, misc). State preconditions and threat model.
- Capture affected assets/endpoints, versions/commit hashes, and privilege level required.

3) Reproduction
- Provide numbered minimal steps, inputs, and expected vs actual outcomes.
- Include transaction hashes, block numbers, cURL snippets, or test scripts as evidence.
- If blockchain: specify chain, contract addresses, function selectors, token assumptions, price/oracle dependencies, and whether flashloans/manipulation are required.

4) Impact
- Quantify impact: fund loss, privilege escalation, permanent DoS, data exfiltration, or integrity break. Estimate worst-case loss and affected users/scope.
- Note exploit reliability and required capital (if any).

5) Mitigation
- Propose smallest safe fix (code/logic/config), plus regression test idea. If unsure, suggest defense-in-depth controls and monitoring.

6) Disclosure packaging
- Choose format: platform template (HackerOne/Immunefi/etc.) or standalone markdown.
- Include supporting artifacts: PoC scripts, logs, screenshots, or links to on-chain txns.
- Add a clear summary: title, severity rationale, root cause, attack path, impact, and fix.

7) Follow-up
- Track CVE/program IDs, coordinate timelines, and be responsive to triager questions. Avoid sharing sensitive details publicly until cleared.

## Templates
Use this concise markdown skeleton when drafting a report:

Title: <short vulnerability name>

Summary:
- Location: <service/contract/file>
- Class: <auth/accounting/oracle/replay/reentrancy/dos/upgrade/web>
- Impact: <fund loss/priv-escalation/dos/data>
- Preconditions: <what attacker needs>

Reproduction:
1. <step>
2. <step>
3. <step>

Expected vs Actual:
- Expected: <safe behavior>
- Actual: <vulnerable outcome>

Impact:
- <quantified effect + scope>

Mitigation:
- <smallest fix>
- Tests: <regression idea>

Artifacts:
- <tx hashes/logs/PoC link>

## Guidance
- Be precise, avoid speculation, and keep steps reproducible.
- Never include private keys or secrets; redacted logs are fine.
- If unsure about severity, map to High when direct fund loss or privilege gain is possible; otherwise Medium, and clearly justify.
- Respect rate limits and ToS; avoid stressing production systems.
