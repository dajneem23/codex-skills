# EVM Security

A comprehensive security assessment and hardening workflow for EVM smart contracts. This skill provides systematic audit methodology for Solidity and Vyper code, covering vulnerability detection, exploit pattern matching, and remediation guidance.

## Purpose

Use this skill when you need to:
- Audit Solidity or Vyper smart contracts
- Review protocol architecture for abuse paths
- Validate access control and value-accounting invariants
- Assess upgradeable/proxy deployments
- Evaluate oracle/bridge/DEX integration risks
- Produce prioritized remediation guidance with proof-of-concept tests

## Components

### SKILL.md
The main skill definition containing the complete security review workflow, including:
- 9-step review process from scoping to final reporting
- Severity classification guidelines (Critical → Informational)
- Output formatting requirements with OWASP alignment

### References

Comprehensive vulnerability knowledge base:

- **`vulnerability-checklist.md`** - Category-level security checks
- **`past-exploit-checklist.md`** - High-frequency exploit patterns from historical incidents
- **`public-audit-patterns.md`** - Cross-protocol audit findings and recurring issues
- **`competition-patterns.md`** - Exploit patterns from competitive audit platforms
- **`quillaudit-patterns.md`** - Historical ERC20/crowdsale audit pitfalls
- **`owasp-scs-alignment.md`** - OWASP SCSVS/SCSTG/SCWE alignment mappings
- **`report-template.md`** - Structured output format for security findings

### Agents

Custom agent configurations for automated security workflows (OpenAI agent specification).

## Review Workflow

The skill follows a systematic 9-step process:

1. **Define Scope** - Identify contracts, roles, trust boundaries
2. **Map Protocol Behavior** - Trace value flow and state transitions
3. **Execute Vulnerability Checks** - Apply comprehensive checklist
4. **Run Exploit-Prior Pass** - Match against historical exploit patterns
5. **Run External-Audit Corpus Pass** - Apply public audit learnings
6. **Run OWASP SCS Alignment** - Map to OWASP standards
7. **Validate Exploitability** - Confirm realistic attack paths
8. **Recommend Remediations** - Provide minimal safe patches
9. **Produce Final Output** - Generate structured report with findings

## Severity Classification

- **Critical** - Immediate catastrophic loss or irreversible compromise
- **High** - Material loss, fund lockup, or privileged control seizure
- **Medium** - Bounded impact or specific preconditions required
- **Low** - Limited impact or narrow exploitability
- **Informational** - Non-exploitable quality/maintainability issues

## Output Format

Each finding includes:
- Title and severity rating
- Affected files with line numbers
- Attack path description
- Impact assessment
- Concrete remediation steps
- OWASP tags (Top 10, SCSVS, SCWE)
- Test recommendations

## Usage

This is a Codex skill designed to be invoked when security assessment of EVM smart contracts is required. The skill systematically applies multiple reference checklists and produces actionable, prioritized findings with reproducible proof-of-concept tests.

## License

This skill is part of the Codex skills repository.
