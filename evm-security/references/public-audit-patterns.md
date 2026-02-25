# Public Audit Patterns to Recheck in EVM

Use this reference as a third-pass filter after baseline vulnerability checks and exploit-prior checks.
These patterns are recurring findings from `~/Dev/Security/public-audits`.

## Source Signals

- Dataset summary in `~/Dev/Security/public-audits/README.md` shows repeated Critical/High findings across DeFi primitives (AMMs, staking, launchpads, bridge integrations).
- Detailed recurring examples were extracted from `~/Dev/Security/public-audits/reports/Perena_Audit_Final_report.pdf`, `~/Dev/Security/public-audits/reports/cantina_oro_february2025.pdf`, `~/Dev/Security/public-audits/reports/Layer_N_report.pdf`, and `~/Dev/Security/public-audits/reports/sparkn-findings.md`.

## Recurrent Finding Classes

### 1) Decimal and Precision Bugs

- Incorrect decimal conversion.
- Division-before-multiplication precision loss.
- Overflow/underflow in mint and supply calculations.
- Wrong fee-rate arithmetic causing value leakage.

EVM checks:
- Normalize units once at boundaries and keep internal accounting in fixed precision.
- Prefer `mulDiv`-style math for ratio calculations.
- Add tests around mixed decimals (6/8/18), near-zero amounts, and near-limit values.

### 2) Validation and Account Binding Gaps

- Missing validation of mint/token identities.
- Missing seed/bump-style binding (equivalent to weak address binding in EVM).
- Bypass conditions from weak account existence checks.

EVM checks:
- Validate every user-supplied token/address/market against allowlists and expected mappings.
- Bind critical operations to canonical contract addresses and immutable IDs.
- Reject zero-address and stale-config paths where safety depends on specific accounts.

### 3) Access Control and Privileged Path Abuse

- Privileged calls with incomplete authority checks.
- Unsafe signer/privilege use in sensitive flows.
- Governance/admin paths that allow unsafe state transitions.

EVM checks:
- Enumerate all privileged entrypoints and validate role checks per function, not per module.
- Enforce two-step admin transitions and explicit timelock requirements where relevant.
- Add tests for unauthorized caller, wrong-role caller, and stale-role caller.

### 4) Oracle and Price Integrity

- Wrong price conversion logic.
- Missing oracle confidence/freshness validation.
- Pool drain paths when price assumptions are weak.

EVM checks:
- Enforce staleness, heartbeat, and deviation bounds on every price read.
- Never trust spot prices for mint/borrow/liquidation decisions.
- Add failure-mode tests for stale, zero, extreme, and manipulated prices.

### 5) Multi-Step State Abuse and Replay-Like Drains

- Repeated unstake/claim path abuse.
- Order-dependent flows that allow re-use of state before finalization.
- DoS through account lifecycle corner cases.

EVM checks:
- Mark state transitions before external effects.
- Add idempotency guards and one-time consumption semantics for claim/unstake tickets.
- Verify emergency and recovery paths cannot permanently lock funds.

### 6) Token Behavior Compatibility

- Logic breaks with fee-on-transfer and non-standard token behavior.
- Blacklist/freeze semantics causing unexpected DoS.

EVM checks:
- Explicitly gate unsupported token behaviors or normalize accounting for them.
- Add integration tests for fee-on-transfer, rebasing, and blacklistable tokens.
- Ensure transfer failure in fee collection does not freeze unrelated user withdrawals.

## Fast Application During Reviews

1. For each value-moving function, identify assumptions about decimals, token behavior, and price source quality.
2. For each privileged function, verify caller binding, parameter binding, and one-time initialization assumptions.
3. For each claim/unstake/mint/burn flow, test repeat-calls and edge-state transitions.
4. Convert every unresolved assumption into either a finding or a mandatory regression test.
