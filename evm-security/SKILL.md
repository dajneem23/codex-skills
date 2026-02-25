---
name: evm-security
description: Security assessment and hardening workflow for EVM smart contracts. Use when Codex needs to audit Solidity or Vyper code, review protocol architecture for abuse paths, validate access control and value-accounting invariants, assess upgradeable/proxy deployments, evaluate oracle/bridge/DEX integration risk, or produce prioritized remediation guidance with reproducible proof-of-concept tests.
---

# EVM Security

## Overview

Perform a repository-grounded EVM security review and produce actionable findings with severity, exploitability, and concrete fixes.
Use `references/vulnerability-checklist.md` for category-level checks, `references/past-exploit-checklist.md` for high-frequency exploit priors, `references/legacy-solidity-security-blog-map.md` to selectively load the local Sigma Prime legacy corpus at `/Users/tranthanh/Dev/Security/web3-audit/solidity-security-blog/README.md`, `references/public-audit-patterns.md` for cross-protocol audit priors, `references/competition-patterns.md` for competition-derived exploit patterns, `references/quillaudit-patterns.md` for historical ERC20/crowdsale audit pitfalls, `references/owasp-scs-alignment.md` for OWASP SCSVS/SCSTG/SCWE alignment, and `references/report-template.md` when formatting output.

## Competition-Derived Key Findings (Past-Audit-Competitions)

- Authorization binding failures are recurrent: weak owner checks (`tx.origin`, inconsistent modifiers) frequently enabled privileged abuse.
- Accounting and solvency desynchronization is a top recurring critical class across lending, staking, and fee-retention logic.
- Oracle correctness issues repeatedly escalated impact: stale prices, poor confidence validation, and manipulable spot dependencies.
- Replay/front-run classes remain common in signature and nonce flows, especially where domain binding or nonce lifecycle is weak.
- Griefing/DoS classes are often high impact when they block safety-critical operations (liquidation, claims, pause recovery).

## Review Workflow

1. Define scope and assumptions.
- Identify in-scope contracts, libraries, deployment targets, and privileged roles.
- Document trust boundaries: admin keys, keepers, multisigs, bridges, oracles, and off-chain services.
- Record threat assumptions before reviewing implementation details.

2. Map protocol behavior and value flow.
- Trace all state transitions that move value, mint/burn assets, or change user permissions.
- Capture key invariants in plain language before evaluating vulnerabilities.
- Flag any undocumented assumptions that are necessary for safety.

3. Execute vulnerability checks.
- Run through `references/vulnerability-checklist.md` and evaluate each category against concrete functions and code paths.
- Prioritize access control, external-call safety, accounting correctness, upgradeability safety, and integration risk.
- Treat missing checks as potential findings until disproven.
- Before checklist passes, pull priors from the local findings library to guide focus:
	- `./.venv/bin/python findings/scripts/findings_query.py --query "oracle price" --limit 5`
	- `./.venv/bin/python findings/scripts/findings_query.py --query "tx-origin" --limit 5`
	- `./.venv/bin/python findings/scripts/findings_query.py --query "permit nonce domain" --limit 5`
	- `./.venv/bin/python findings/scripts/findings_query.py --tags defihacklabs-src --limit 5`
	Keep the 3–10 returned priors visible as hints while running checklist passes.

4. Run exploit-prior pass.
- Apply `references/past-exploit-checklist.md` as a focused second pass.
- Assume high prior probability for business-logic flaws, price manipulation, access-control breaks, and reentrancy until disproven.
- Attempt to construct at least one realistic abuse sequence for each high-priority prior.

5. Run legacy Solidity corpus pass.
- Use `references/legacy-solidity-security-blog-map.md` to map suspicious code patterns to relevant sections in `/Users/tranthanh/Dev/Security/web3-audit/solidity-security-blog/README.md`.
- Load only relevant section(s) from the corpus instead of reading the full file.
- Distinguish compiler-era issues from still-relevant risks.
- For Solidity `>=0.8.x`, explicitly separate mitigated-by-default issues from residual logic risk.

6. Run external-audit corpus pass.
- Apply `references/public-audit-patterns.md` to check recurring audit classes that often become incidents later.
- Apply `references/competition-patterns.md` to check patterns repeatedly found in competitive audits.
- Apply `references/quillaudit-patterns.md` to catch recurring token/crowdsale authorization and accounting mistakes.
- Focus on decimal normalization, oracle confidence/staleness checks, privileged account binding, and token-behavior compatibility.
- Treat unresolved design assumptions as findings candidates until validated in code or tests.

7. Run OWASP SCS alignment pass.
- Apply `references/owasp-scs-alignment.md` and map coverage against SCSVS domains.
- Tag each high-confidence finding with OWASP Smart Contract Top 10 category when applicable.
- Attach relevant SCWE weakness IDs and SCSTG test IDs when a direct mapping is clear.

8. Validate exploitability and impact.
- Confirm whether a realistic attacker can trigger each issue under stated assumptions.
- Build minimal proof-of-concept steps for Critical and High findings.
- Distinguish direct fund loss, permanent denial of service, governance takeover, and griefing-only impact.

9. Recommend and verify remediations.
- Provide the smallest safe patch that closes the abuse path without breaking protocol invariants.
- Propose regression tests for every finding, with fuzz or invariant tests for systemic logic issues.
- Identify post-fix checks that must pass before deployment.

10. Produce final output.
- Use `references/report-template.md` for consistent sections and finding schema.
- Include exact file paths and line numbers for every finding when available.
- Call out residual risk, test gaps, and assumptions that remain unproven.

## Severity Guidance

- Mark as `Critical` when exploitability can cause immediate catastrophic loss or irreversible protocol compromise.
- Mark as `High` when exploitability can cause material loss, lock user funds, or seize privileged control.
- Mark as `Medium` when impact is bounded but meaningful, or exploitability requires specific preconditions.
- Mark as `Low` when impact is limited, defense-in-depth is weak, or exploitability is narrow.
- Mark as `Informational` for non-exploitable design quality or maintainability issues.

## Output Requirements

- List findings first, sorted by severity.
- For each finding include: title, severity, affected files, attack path, impact, and remediation.
- Include OWASP tags when available: Top10 category, SCSVS domain/control area, and SCWE weakness ID.
- When the local Sigma Prime corpus informed the finding, cite the section anchor (for example `reentrancy` or `unchecked-calls`) and explain whether the issue is legacy-only or currently exploitable.
- Provide at least one test recommendation per finding.
- State explicitly when no high-confidence findings are discovered.
