# Findings Schema (JSONL)

Each line in `findings.jsonl` is a JSON object with these fields:

Required:
- `id` (string): Stable identifier, e.g., `FND-0001`.
- `title` (string): Short, descriptive.
- `severity` (string): One of `Critical|High|Medium|Low|Info`.
- `category` (string): Use controlled tags from `tags.md` (e.g., `auth`, `accounting`, `oracle`, `replay`, `reentrancy`, `dos`, `upgrade`).
- `root_cause` (string): 1–3 sentences.
- `attack_path` (string): 1–5 steps in prose.
- `impact` (string): 1–2 sentences, quantified when possible.
- `mitigation` (string): 1–3 sentences or a minimal patch description.

Recommended:
- `code_context` (object): `{ "paths": ["contracts/Vault.sol"], "lines": "L120-L155" }`.
- `tags` (array of strings): Additional surfaces, e.g., `erc4626`, `permit`, `twap`, `uups`, `pause`, `fee-on-transfer`.
- `source` (object): `{ "type": "competition|internal", "link": "https://...", "date": "2024-12-09" }`.
- `related_ids` (array of strings): Cross-reference similar findings.
- `test_recommendation` (string): Brief regression test idea.

Optional:
- `poc` (string): Short PoC steps or gist link.
- `notes` (string): Freeform comments.

Example entry is in `findings.jsonl`.
