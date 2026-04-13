# Source Hunt Playbook

Use these query templates to quickly find high-signal references.

## General Query Pattern

`<bug class> <affected system> advisory OR post-mortem OR exploit OR audit`

## Bug-Class Query Seeds

### Uninitialized Initializer / Ownership Takeover

- `uninitialized initializer contract takeover advisory`
- `OpenZeppelin Initializable uninitialized contract can be taken over`
- `UUPS uninitialized implementation vulnerability`
- `proxy initialization race exploit`

### Missing `msg.value` Validation / Trapped ETH

- `msg.value non-zero when not selling ETH audit finding`
- `stuck ETH due to payable branch without refund`
- `excess msg.value trapped in contract vulnerability`
- `router accepts ETH on ERC20 path stuck funds`

### Reentrancy

- `cross-function reentrancy incident post-mortem`
- `read-only reentrancy exploit`

### Access Control / Privilege Escalation

- `missing onlyOwner exploit incident`
- `access control misconfiguration smart contract exploit`

## Source Preference Rules

1. Official docs/advisories first.
2. Then reputable post-mortems and audits.
3. Then bug bounty writeups with concrete PoC.
4. Skip low-authority summaries if a primary source exists.

## Minimum Evidence Per Finding

- 2 authoritative docs/advisories
- 1 exploit/incident precedent (if available)
- 1 optional independent audit finding

