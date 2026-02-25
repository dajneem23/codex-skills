# Legacy Solidity Security Blog Map

Source corpus:
- `/Users/tranthanh/Dev/Security/web3-audit/solidity-security-blog/README.md`

Use this map to load only relevant parts of the corpus during audits.

## Usage Rules

1. Identify compiler range first (`pragma solidity`).
2. Select section(s) below by matching code smell or attack surface.
3. For Solidity `>=0.8.x`, mark whether issue class is mitigated by compiler defaults, then check for residual logic-level risk.
4. Preserve anchor IDs in finding notes for traceability.

## Section Map

- `reentrancy`: External calls before state updates, callback paths, hooks, and nested token callbacks.
- `ouflow`: Arithmetic overflow and underflow. Treat as high priority for `<0.8.x`; for `>=0.8.x`, focus on `unchecked` blocks and cast truncation.
- `ether`: Balance assumptions using `address(this).balance`, forced ETH via `selfdestruct`, and accounting that relies on exact balance.
- `delegatecall`: Proxy/library execution context confusion, slot collisions, and unsafe delegate targets.
- `visibility`: Missing visibility or unintended external exposure (mostly legacy, but still relevant for inherited code).
- `entropy`: Randomness derived from miner-controlled or predictable chain fields.
- `contract-reference`: Blind trust in external contract behavior, interface mismatches, and hostile integrations.
- `short-address`: ABI short address issues (mostly off-chain/client era bug); verify modern ABI tooling assumptions.
- `unchecked-calls`: Ignored success flags from low-level calls.
- `race-conditions`: Transaction ordering dependence, mempool frontrunning, allowance race patterns.
- `dos`: Unbounded loops, reverting recipients, push-payment fanout, and gas griefing.
- `block-timestamp`: Timestamp dependence for critical logic and miner influence windows.
- `constructors`: Constructor naming/initialization issues in older compiler eras and upgradeable initialization mistakes.
- `storage`: Uninitialized storage pointers and storage aliasing hazards.
- `precision`: Integer rounding, decimal normalization, and fixed-point precision loss.
- `tx-origin`: Authorization with `tx.origin` instead of `msg.sender`.
- `ethereum-quirks`: Edge-case EVM behaviors that can break assumptions.
- `hacks`: Historical exploit examples for abuse-sequence priors.

## Practical Selection Hints

- Start with `reentrancy`, `unchecked-calls`, `dos`, `race-conditions`, and `precision` for most DeFi protocols.
- Add `delegatecall` and `constructors` for proxy or factory systems.
- Add `ether` when native ETH accounting matters.
- Add `entropy` only when contracts implement randomness.
- Add `tx-origin` and `visibility` as quick auth hardening checks.
