# EVM Security Report Template

Use this structure for final responses.

## Scope

- Target repository/path:
- In-scope contracts:
- Out-of-scope items:
- Threat assumptions:

## Findings

List findings in descending severity.

### [Severity] Finding Title

- Affected files: `path/to/file.sol:line`
- Confidence: High | Medium | Low
- Attack path: Short step-by-step abuse sequence.
- Impact: What can be lost, broken, or controlled.
- Evidence: Relevant code behavior and preconditions.
- Remediation: Minimal patch direction.
- Test recommendation: Unit, fuzz, or invariant test to prevent regression.

## Additional Risks

- Document lower-confidence concerns, assumptions, and ecosystem dependencies.

## Verification Notes

- Summarize what was validated directly.
- Summarize what remains untested or assumption-dependent.

## Conclusion

- Provide prioritized next actions.
- State residual risk after proposed fixes.
