ư# Competitive Audit Pattern Checklist (EVM)

Use this reference after baseline checks and exploit-prior checks.
These patterns were distilled from `~/Dev/Security/web3-audit/Past-Audit-Competitions`.

## Source Signals

- The corpus contains many cross-protocol findings with repeated issue classes in `*.md` reports.
- Filename-derived smart-contract subset: 758 reports.
- Severity mix from this subset: 126 `Critical`, 102 `High`, 103 `Medium`, 165 `Low`, 262 `Insight`.

Representative sources:
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/Mitigation Audit | Folks Finance/Mitigation Audit _ Folks Finance 34929 - [Smart Contract - Critical] Accounting Discrepancy in Fee Retention Leads to Protocol Insolvency and Fund Freezing.md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/ZeroLend/29288 - [SC - Critical] all NFTs can be stolen by calling VestedZeroNFT....md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/ZeroLend/29068 - [SC - Medium] AaveOracle contract does not verify price stale....md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/anvil/36554-sc-critical-time-based-collateral-pool-users-can-release-more-than-their-due-share-of-the-pool.md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/anvil/36501-sc-medium-signature-front-running-vulnerability-in-collateralvault.md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/ZeroLend/29342 - [SC - Insight] Lack of chainID validation allows reuse of sign....md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/Puffer Finance/28833 - [SC - Insight] Missing slippage protection in functions deposi....md`
- `~/Dev/Security/web3-audit/Past-Audit-Competitions/BadgerDAO (eBTC)/28659 - [SC - Insight] Reentrancy in BorrowerOperationsflashLoan enabl....md`

## Recurrent High-Impact Classes

### 1) Accounting Drift and Insolvency

- Protocol balance sheets diverge when liabilities/assets are updated asymmetrically.
- Fee withdrawal and interest accrual paths can inflate available liquidity.
- Epoch/reset accounting can let one cohort withdraw from another cohort's balance.

EVM checks:
- Enforce invariants after every state transition.
- `assets_on_chain + receivables >= user_claims + protocol_obligations`.
- `available_liquidity` must exclude already-withdrawable protocol fees.
- Recompute solvency before and after fee collection, repayments, and resets.
- Add invariant tests for repeated fee-collect and cross-epoch transitions.

### 2) Ownership and Authorization Binding Failures

- Existence checks are confused with authorization checks.
- Functions that mutate ownership-linked balances can be callable by non-owners.
- Unauthorized mint/split/claim paths appear in tokenized vesting and staking flows.
- `tx.origin`-based ownership checks enable phishing-style call-chain impersonation.

EVM checks:
- Require caller ownership or explicit approval at every ownership-sensitive entrypoint.
- Reject reliance on helper methods that only confirm token existence.
- Reject `tx.origin` for access control decisions; use `msg.sender` with explicit role binding.
- Add unauthorized-caller tests for each mutation path.

Attackathon-derived test case (Ethereum Protocol `#37577`, Insight):
- Pattern: Group-management owner checks compare against `tx.origin`, allowing malicious intermediate contracts to trigger privileged `lock`/`unlock` or membership updates.
- Abuse path: attacker deploys a forwarding contract, convinces owner to call it, forwarding call reaches target and passes `tx.origin == owner` gate.
- Impact: unauthorized privileged state transitions and potential loss of control over membership/admin state.
- Mitigation: migrate owner checks to `msg.sender`, centralize with `onlyOwner`/RBAC modifiers, and add regression tests for indirect-call phishing (`EOA -> malicious contract -> target`).

### 3) Signature, Permit, and Nonce Exploits

- Permit-style flows are front-runnable when nonce consumption is externally triggerable.
- Missing chain/domain binding allows cross-chain or fork replay.
- Signatures are reused when message scope is too broad.

EVM checks:
- Bind signatures to chain ID, verifying contract, action type, and critical parameters.
- Consume nonce only in the final authorized execution path.
- Include user-chosen deadlines and salt/nonces in signed payloads.
- Add tests for mempool front-run, replay on forked chain IDs, and cross-contract replay.

### 4) Oracle Freshness and Price Integrity

- Price feeds are used without staleness/freshness checks.
- Fallback logic triggers only on zero prices while stale prices still pass.

EVM checks:
- Validate round completeness, timestamp freshness, heartbeat, and deviation bounds.
- Reject stale-but-nonzero prices.
- Add tests for stale oracle, delayed updates, and fallback-switch scenarios.

### 5) Slippage and MEV-Sensitive User Flows

- Deposit/mint/convert paths omit user-provided minimum output constraints.
- Users receive fewer shares/assets than expected under volatile exchange rates.

EVM checks:
- Add `minOut` or `minShares` on all user-entry conversion paths.
- Revert if realized output is below user bounds.
- Add tests for sandwich and state-shift between `preview` and `execute`.

### 6) Reentrancy and Callback Composition

- Flashloan callback paths can reenter and bypass intended per-call caps.
- External calls without robust sequencing let attackers loop state mutations.

EVM checks:
- Apply reentrancy guards where callback-capable flows modify critical state.
- Update state before external calls; validate post-conditions afterward.
- Add nested-callback tests for flashloan and hook-compatible operations.

### 7) Governance and Voting Manipulation

- Vote power inflation, flawed gauge registration checks, or tainted ownership paths can capture governance.
- Privileged roles assigned to EOAs without operational controls increase takeover risk.

EVM checks:
- Enforce vote accounting invariants and snapshot integrity.
- Validate registration predicates with strict boolean logic and unique constraints.
- Prefer multisig/timelock ownership for critical admin roles.

### 8) DoS and Griefing Through Edge-State Transitions

- Front-runnable operations can invalidate honest transactions.
- Reset, pause, and claim sequencing bugs can permanently block user exits.

EVM checks:
- Design idempotent state transitions and bounded retry paths.
- Ensure one user's failure cannot permanently block global progress.
- Add adversarial tests for front-run invalidation and partial-progress rollbacks.

## Fast Triage Sequence

1. Balance-sheet integrity checks on borrow/repay/withdraw/fee-collect.
2. Authorization checks on ownership-sensitive token and vesting operations.
3. Permit/signature paths (domain, nonce lifecycle, replay resistance).
4. Oracle freshness and conversion logic for price-dependent actions.
5. Reentrancy and callback sequencing on flashloan or hook-enabled paths.
6. Governance vote accounting and admin-role hardening.
