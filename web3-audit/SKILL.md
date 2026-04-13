# Web3 Bug Bounty Audit Skill

## Threat Model — Check First

Before analyzing any contract, identify the trust boundaries:

1. **List all privileged roles** (ADMIN, OWNER, MULTISIG, RELAYER, EMERGENCY, MINTER, etc.)
2. **Assume privileged roles are trusted** unless the program explicitly says otherwise
3. **Only findings exploitable by external unprivileged users are valid** for most bug bounties
4. If a bug requires a trusted role to misbehave, it's out of scope — don't waste time on it

## What Gets Rejected

These patterns are almost always marked invalid:

- **"Compromised relayer/admin can drain funds"** — that's the trust model, not a bug
- **"Missing on-chain dedup for relayer-only function"** — dedup is handled off-chain by design
- **"Signature missing fields X, Y"** — if exploitation requires the relayer to sign something it wouldn't sign off-chain, triagers say "relayer wouldn't do that"
- **"Fixed-window rate limit can be burst at boundary"** — standard design pattern, not a vulnerability
- **"Admin can set bad parameters"** — trusted role, intended behavior
- **"Off-chain component could be bypassed"** — off-chain infra is part of the security model

## What Gets Accepted

Focus on these attack surfaces:

- **External user calling public functions** (no role required)
- **Reentrancy** in user-facing functions
- **Access control bypass** — actually calling privileged functions without the role
- **Proxy/upgrade takeover** — uninitialized implementation, open `initialize()`
- **Token handling bugs** — fee-on-transfer, rebasing, weird ERC20 in user-facing paths
- **Integer overflow/underflow** in user-controlled math
- **Price manipulation / oracle issues**
- **Cross-chain message validation** that users can forge without needing a trusted role
- **Griefing** — user can permanently brick other users' funds
- **Front-running** user transactions for profit

## Workflow

1. Read the program scope and rules carefully
2. Map trust boundaries and roles
3. For each function, ask: "Can an **unprivileged external caller** exploit this?"
4. If the answer involves "if the admin/relayer does X wrong" — skip it
5. Write PoC only for issues where the attacker is a regular user
6. Before submitting, re-check: does this finding assume any trusted role misbehavior?

## Severity Calibration

- **Critical**: Unconditional drain by external user, no preconditions
- **High**: External user exploit with realistic preconditions, significant fund loss
- **Medium**: External user exploit with unlikely preconditions, or limited impact
- **Low/Info**: Code quality, best practices — most programs don't pay for these

If your finding needs 3+ preconditions or "the admin configured it wrong," it's probably Low/Info at best.

## Lessons Learned (Whitechain Bridge, March 2026)

- Findings 8, 9 rejected: signature hash missing `address(this)`, `mapId`, `originTokenAddress` — triagers said relayer is trusted and wouldn't misprocess
- Finding 4 (externalId replay) — same issue, `receiveTokens` is `onlyRole(RELAYER_ROLE)`
- Finding 5 (daily limit burst) — intended design, standard fixed-window pattern
- Key takeaway: **the relayer's off-chain logic is considered part of the security model**, not just the on-chain code

## Lessons Learned (MultipliVault, March 2026)

- "FlashRedeem allows arbitrary asset payout" was filed as Critical — **invalid**
  - `vault.flashRedeem()` is `requiresAuth`; in production only the `VaultFundManager` contract (which correctly derives `assetsWithFee = convertToAssets(shares)`) and the vault **owner** can call it
  - The only exploit path required the vault owner to call the function directly — that's trusted-admin rug, not a bug
- "Redemption fulfillment can underpay users" — same pattern: `fulfillRedeem` is `requiresAuth`, only `FUND_MANAGER_CONTRACT_ROLE` and owner can call it
- **Rule: Before filing a `requiresAuth` / `onlyRole` function as vulnerable, trace the deployment script to see WHO actually gets that role. If it's only trusted contracts + owner, it's not a valid external exploit.**
- Two Medium findings (redeem accounting decoupling, fee change between request/fulfillment) were triaged as Informative — programs often consider admin-operated async flows as design choices, not bugs
- Key takeaway: **For async vault patterns (request → fulfill), if the fulfill step is admin-only, the admin controls the parameters by design. Focus on user-facing request/deposit/withdraw paths instead.**

## Lessons Learned (Whitechain Network, March 2026)

- Finding 7 (Mint no burn verification) filed as High, downgraded to Medium, then **confirmed as intended design by team**:
  - `Mint()` in `core/vm/evm.go` is restricted to `operator/owner` role
  - Owner validates cross-chain burn events **off-chain** before submitting mint TX
  - No on-chain burn hash verification, no dedup registry — all by design
  - Team response: *"The behavior you described is intentional and part of the system design."*
- Fabricated/replayed burn hashes are not additional exploit vectors — owner can already mint anything up to `mintLimit` regardless of hash validity
- **Rule: Protocol-level mint/bridge functions restricted to a single trusted operator follow the same pattern as relayer-only functions. The off-chain validation IS the security model. "Admin can mint with fake hash" = "admin can rug" = out of scope.**
- Finding 5 (GetReceiptsMsg DoS) was a known upstream geth issue (Attackathon #38598), not Whitechain-specific — check if findings are inherited vs fork-specific before filing
- Key takeaway: **When code comments explicitly say "we deliberately avoided an oracle" and the function is owner-only, the trusted operator model is intentional. Don't file centralization risk as a protocol exploit.**
