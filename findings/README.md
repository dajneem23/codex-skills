# Findings Library

Lightweight, local repository for past findings and patterns. Keep records in JSONL for easy appending and simple filtering. Use the query script to pull relevant findings by tags or keywords at audit start.

## Contents
- `findings.jsonl` — canonical store of findings (append-only).
- `schema.md` — field definitions and required/optional fields.
- `tags.md` — controlled vocabulary for categories and surfaces.
- `scripts/findings_query.py` — minimal query helper (tags + keyword match).
- `competition_index.jsonl` — auto-generated index over Past-Audit-Competitions (pointers only).
- `pdf_index.jsonl` — auto-generated index over audit-report PDFs (pointers + first 800 chars of extracted text).
- `defihacklabs_index.jsonl` — auto-generated index over SunWeb3 DeFiHackLabs incident list (pointers + summary from anchors).
- `defihacklabs_src_index.jsonl` — auto-generated index over SunWeb3 DeFiHackLabs Solidity PoCs under `src/`.

## Workflow
1. Add findings to `findings.jsonl` (one JSON object per line) using the schema and tags.
2. Regenerate the competition index if the corpus changes:
	```
	python3 scripts/build_competition_index.py
	```
3. Regenerate the PDF index for `/Users/tranthanh/Dev/Security/web3-audit/audit-reports`:
	```
	python3 scripts/build_pdf_index.py
	```
4. Regenerate the DeFiHackLabs index for `/Users/tranthanh/Dev/Security/sunweb3-Defihacklabs`:
	```
	python3 scripts/build_defihacklabs_index.py
	```
5. Regenerate the DeFiHackLabs src index for `/Users/tranthanh/Dev/Security/sunweb3-Defihacklabs/src`:
	```
	python3 scripts/build_defihacklabs_src_index.py
	```
6. At audit start, run the query helper to fetch top-N relevant records by tags/keywords (loads competition/pdf/defihacklabs indexes by default):
	```
	python3 scripts/findings_query.py --tags auth tx-origin --limit 5
	python3 scripts/findings_query.py --query "stale oracle price" --limit 5
	```
7. Load the small result set into context; open full source links only as needed.

## Tips
- Keep `root_cause`, `attack_path`, and `mitigation` concise (1–3 sentences each).
- Include `source_path` or `source_link` to jump to the original report/PoC.
- Tag severity using your existing scale (Critical, High, Medium, Low, Info).
- When referencing code, prefer repo-relative paths and line ranges.
- Avoid duplicating nearly identical findings; instead, add multiple `source_link` entries or `related_ids`.
