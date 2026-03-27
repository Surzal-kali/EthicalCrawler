# Legal and Ethical Security Testing Instruction

## Core Principle

**MUST ALWAYS** require explicit written authorization before performing any security testing, penetration testing, or monitoring activities. Unauthorized access or monitoring is illegal and violates computer crime laws.

## Authorization Requirements

Before any security testing activity, verify:
1. Written authorization exists and is accessible
2. Documented scope and targets are clearly defined
3. Explicit consent from system owners is obtained
4. Authorization covers all planned activities

## Ethical Boundaries

- Only test systems you own or have explicit permission to test
- Never attempt unauthorized access, exploitation, or monitoring
- Respect privacy and data protection regulations (GDPR, CCPA, etc.)
- Use tools only for educational and authorized security testing purposes
- Document all activities and report findings responsibly

## Scope Limitations

- Strictly adhere to authorized scope
- Do not expand testing beyond authorized boundaries
- Report any scope violations immediately
- Terminate activities if authorization is revoked

## Educational Purpose

All security testing activities must be:
- For educational purposes only
- Conducted with proper authorization
- Used to improve security awareness
- Never for malicious or unauthorized purposes

## Reporting Requirements

- Document all authorization details in `/consent/` directory
- Report findings to authorized stakeholders
- Provide remediation recommendations
- Maintain audit trail of all activities

## Violation Protocol

If authorization is unclear or revoked:
1. Immediately cease all activities
2. Document the situation
3. Report to authorized personnel
4. Do not proceed with any testing

## Implementation Guidelines

When implementing security testing features:

1. **Pre-Flight Checks**
   - Verify authorization document exists
   - Confirm scope matches planned activities
   - Check for any restrictions or conditions

2. **Authorization Verification**
   - Display authorization requirements to user
   - Require explicit acknowledgment
   - Store acknowledgment in audit log

3. **Scope Enforcement**
   - Validate targets against authorized scope
   - Reject requests outside authorized boundaries
   - Log all authorization checks

4. **Activity Monitoring**
   - Track all operations against authorization
   - Alert if scope is exceeded
   - Provide real-time compliance status

5. **Documentation**
   - Log all activities with timestamps
   - Record authorization references
   - Generate post-session reports

## Common Anti-Patterns

❌ **DON'T**:
- Assume authorization exists without verification
- Proceed with testing if authorization is unclear
- Expand scope without explicit permission
- Use tools for unauthorized monitoring
- Skip authorization checks for "educational" purposes

✅ **DO**:
- Always verify authorization before any operation
- Document all authorization checks
- Maintain clear audit trail
- Report scope violations immediately
- Terminate activities if authorization is revoked

## Example Authorization Flow

```pseudocode
FUNCTION verify_authorization(target):
    IF authorization_document_exists() THEN
        IF authorization_scope.includes(target) THEN
            IF user_acknowledges_requirements() THEN
                RETURN true
            ELSE
                RETURN false
        ELSE
            RETURN false
    ELSE
        RETURN false
```

## Integration with EthicalCrawler

This instruction applies to all components:
- System Profiler
- Network Scanner
- Web Crawler
- SQL Searcher
- Remote Coordinator

All components must enforce authorization requirements before performing any security operations.

---

**IMPORTANT**: This instruction is a hard requirement. Never proceed with security testing without explicit written authorization.