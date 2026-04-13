# Skills Workspace

Curated collection of reusable agent skills and supporting references for security reviews, research, and automation. Each skill lives in its own folder with a SKILL.md prompt, optional agents/openai.yaml runner config, and references/ supporting docs.

## Directory Map
- behavioral-state-analysis — behavioral cues and threat engine patterns
- dos-griefing-analysis — DoS and gas-griefing patterns
- evm-security — general EVM audit guidance and checklists
- external-call-safety — external call and ERC20 edge-case patterns
- findings — JSONL findings library plus generated indexes
- input-arithmetic-safety — precision and validation patterns
- notion-research-documentation — research/reporting templates
- oracle-flashloan-analysis — oracle + flash loan vectors
- pdf — PDF helper skill
- playwright — Playwright automation skill
- proxy-upgrade-safety — proxy upgrade patterns and collision checks
- reentrancy-pattern-analysis — reentrancy variants and case studies
- security-best-practices — language/framework security quickstarts
- security-bug-bounty — workflow for preparing and submitting bug bounty reports
- security-ownership-map — ownership graph tooling
- security-threat-model — prompt-driven threat modeling templates
- semantic-guard-analysis — semantic guardrails and detection examples
- signature-replay-analysis — replay taxonomy and EIP-712 checks
- state-invariant-detection — invariant types and examples

## Findings Library
The findings library in findings/ stores JSONL records plus auto-generated indexes. Common tasks:

Current total findings in [findings/findings.jsonl](findings/findings.jsonl): 5.

```sh
# query records by tags/keywords
python3 findings/scripts/findings_query.py --tags auth tx-origin --limit 5
python3 findings/scripts/findings_query.py --query "stale oracle price" --limit 5

# regenerate indexes (update source paths in scripts if your corpus lives elsewhere)
python3 findings/scripts/build_competition_index.py
python3 findings/scripts/build_pdf_index.py
python3 findings/scripts/build_defihacklabs_index.py
python3 findings/scripts/build_defihacklabs_src_index.py
```

See findings/README.md for schema, tagging guidance, and workflow.

## Working With Skills
- Read each SKILL.md for intent, inputs, and expected outputs.
- references/ contains distilled patterns, checklists, and templates cited by the skill.
- agents/openai.yaml (when present) is a ready-made runner config you can copy or invoke.

## Development Notes
- Keep additions ASCII-only unless a file already uses Unicode intentionally.
- Respect .gitignore (.venv, .system).
- If adding new scripts, prefer small, dependency-light Python 3 helpers.
