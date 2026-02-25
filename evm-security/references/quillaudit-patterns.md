# QuillAudit-Derived EVM Patterns

Use this as an additional prior after `vulnerability-checklist.md` and `past-exploit-checklist.md`.
These checks are distilled from `~/Dev/Security/QuillAudit_Reports` (especially its markdown audit reports) and are useful for token, crowdsale, and legacy codebases.

## Source Signals

- Corpus scale: large multi-report archive with predominantly smart-contract audit PDFs and markdown reports.
- Markdown subset repeatedly flags allowance races, initialization/ownership mistakes, pausable misuse, and sale-stage/accounting issues.
- Several reports include issue `Status` fields (`Fixed`, `Not yet Fixed`, `Not Fixed`), making retest discipline important.

## 1) Initialization and Ownership Binding

- Ensure `initialize`-style functions are one-time and role-restricted.
- Reject constructors/initializers that accept unsafe actor bindings (beneficiary equals owner/deployer unless explicitly intended).
- Validate zero-address checks use `address(0)` comparisons.
- Verify ownership transfer and acceptance flows cannot be hijacked or stuck.

Fast checks:
- Attempt unauthorized initialization on fresh deployment state.
- Attempt re-initialization after first successful initialization.
- Attempt privileged calls from non-owner and stale-owner addresses.

## 2) ERC20 Approval and Allowance Safety

- Treat raw `approve` nonzero->nonzero transitions as risky unless intentionally handled.
- Confirm allowance mutation logic is consistent across `approve`, `increaseAllowance`, and `decreaseAllowance`.
- Detect storage-shadowing or split allowance mappings that desynchronize views and enforcement.

Fast checks:
- Front-run style sequence: set allowance A, spender spends, owner updates allowance.
- Repeated increase/decrease cycles across mixed spender addresses.

## 3) Pause and Emergency Controls

- Verify pause state is enforced on every value-moving path, not only `transfer`.
- Ensure `pause`/`unpause` are idempotent and role-protected.
- Confirm emergency controls do not create permanent lockup for legitimate withdrawals/recovery paths.

Fast checks:
- Run core flows while paused and ensure protected flows revert.
- Attempt pause/unpause from unauthorized actors.

## 4) Supply and Accounting Invariants (Mint/Burn/Distribute)

- Enforce `minted + distributable <= maxSupply` invariants under all paths.
- Check burn logic emits canonical transfer events when required by downstream tooling/indexers.
- Reject negative/zero-value edge cases where business rules expect strict positivity.
- Verify reserved pools (team/bounty/airdrop/sale) cannot be overdrawn or double-counted.

Fast checks:
- Mint and distribute near supply boundaries.
- Burn from direct holder and delegated `burnFrom` paths.
- Replay stage transitions with partial reserve consumption.

## 5) External Call Ordering and Reentrancy

- For workflows making external calls, update state before interaction.
- Recheck call chains in factory/manager patterns where one contract mutates another.
- Treat callback-capable integrations as reentrancy candidates even if no ETH transfer occurs.

Fast checks:
- Simulate callback reentry around create/settle/vote/claim flows.
- Validate post-conditions after external call failure and success.

## 6) Stage Machine and Lifecycle Gating

- Confirm stage transitions are monotonic where documentation says they are.
- Validate whitelist/eligibility logic respects current sale stage.
- Check that finalization paths cannot be blocked by contradictory `require` conditions.

Fast checks:
- Attempt out-of-order stage transitions.
- Attempt late whitelisting for closed stages.
- Attempt finalize-and-burn when supply or balances hit edge conditions.

## 7) Legacy Solidity and Security Hygiene

- Flag legacy compiler/version patterns and deprecated syntax in inherited code.
- Verify constructors, events (`emit`), and hashing/encoding semantics are explicit and modernized.
- Ensure access modifiers are explicit and consistent.

Note:
- Hygiene issues are often low severity alone, but can conceal high-impact logic bugs in old codebases.

## 8) Status-Aware Retest Discipline

When prior audits mark issues as fixed:
1. Reproduce the original issue trigger.
2. Verify the patch blocks the trigger.
3. Add a regression test locking expected behavior.

When issues are marked not fixed:
1. Treat as active risk until disproven in current code.
2. Reassess exploitability with current architecture and integrations.
