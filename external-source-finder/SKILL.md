---
name: external-source-finder
description: Find high-quality external references and real exploit precedents to strengthen security/audit reports. Use when the user asks for citations, prior art, incident links, or proof that a finding class is known and exploitable.
---

# External Source Finder

## Overview

Use this skill when a report needs stronger external evidence. It gathers authoritative docs, advisories, audit findings, and exploit writeups, then returns citation-ready references grouped by finding.

## Workflow

### 1) Normalize Each Finding

For each finding, extract:
- Bug class (for example: uninitialized initializer takeover, msg.value trapping, reentrancy)
- Impact class (theft, freeze, DoS, privilege escalation)
- Affected component type (proxy, router, token integration, bridge, etc.)

### 2) Search in Priority Order

Prefer sources in this order:
1. Official project/library docs (OpenZeppelin, Solidity, protocol docs)
2. Vendor advisories/CVEs/GHSAs
3. Post-mortems from authoritative orgs
4. Reputable audit reports (ConsenSys Diligence, Trail of Bits, OpenZeppelin, Code4rena final reports)
5. Bug bounty reports with concrete exploitation details

Avoid low-signal SEO/security blogs unless no primary source exists.

Use query patterns from [source-hunt-playbook.md](references/source-hunt-playbook.md).

### 3) Build Evidence Per Finding

Target per finding:
- At least 2 documentation/advisory references
- At least 1 exploit or incident precedent (if available)
- Optional: 1 additional audit/competition finding with similar root cause

For each source, capture:
- Title
- URL
- Why it supports the finding (one sentence)
- Source type (`doc`, `advisory`, `incident`, `audit`, `bounty`)
- Publish/update date when available

### 4) Quality Gate

Before finalizing references:
- Verify each URL resolves and content matches claim
- Remove duplicates and weakly-related links
- Ensure each reference supports exploitability or impact, not just generic best practice
- Explicitly label any inference when source is indirect

### 5) Produce Citation-Ready Output

Use this structure in responses or report patches:

```md
## External References - <Finding ID>

- <Source Title> (<Source Type>)  
  <URL>  
  Relevance: <one sentence tied to this finding>
```

When the user asks to update a file, append references directly into the target report.

## Quick Trigger Phrases

Use this skill when user requests include phrases like:
- "find external sources"
- "add references"
- "prior art"
- "incident examples"
- "exploit examples"
- "make report more persuasive"
- "add citations"

## Notes

- Prefer authoritative primary sources over social posts.
- Include at least one exploit precedent for critical/high findings if available.
- Keep references concise and directly mapped to findings to avoid noise.
