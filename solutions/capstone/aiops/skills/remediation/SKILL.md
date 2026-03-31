---
name: remediation
description: Runbooks and procedures for safely remediating common service failures with appropriate risk controls.
---

# Remediation Skill

## Risk Classification

All remediation actions are classified by risk:

- **Low**: Minimal impact, fast rollback, safe to automate
- **Medium**: Some impact, requires approval, rollback available
- **High**: Significant impact, requires senior approval, complex rollback

## Runbooks

### Service Restart (Low Risk)
**When to use**: Process crashes, hung services, minor memory leaks

**Procedure**:
1. Execute: `execute_remediation("restart", "service-name")`
2. Monitor: Service comes back healthy within 30s
3. Verify: Health checks passing, traffic resuming

**Expected downtime**: 10-30 seconds

**Rollback**: N/A (restart is the rollback)

### Scale Up Resources (Low Risk)
**When to use**: Resource exhaustion (CPU, memory, connections)

**Procedure**:
1. Execute: `execute_remediation("scale_up", "service-name")`
2. Monitor: New instances starting, load distributing
3. Verify: Metrics returning to normal

**Expected impact**: None (adds capacity)

**Rollback**: Scale down after incident resolved

### Rollback Deployment (Medium Risk)
**When to use**: Recent deployment causing errors, regression detected

**Procedure**:
1. Identify previous stable version
2. Execute: `execute_remediation("rollback_deployment", "service-name")`
3. Monitor: Rollback progress, service health
4. Verify: Error rate dropping, functionality restored

**Expected downtime**: 30-90 seconds during rollback

**Rollback**: Re-deploy if rollback causes issues (rare)

### Connection Pool Reset (Medium Risk)
**When to use**: Connection pool exhaustion, leaked connections

**Procedure**:
1. Execute: `execute_remediation("reset_connection_pool", "service-name")`
2. Monitor: Pool draining and re-initializing
3. Verify: Connections available, errors cleared

**Expected impact**: Brief connection errors during reset

**Rollback**: Service restart if reset fails

### Increase Connection Pool Size (Low Risk)
**When to use**: Pool legitimately too small for load

**Procedure**:
1. Execute: `execute_remediation("increase_pool_size", "service-name")`
2. Monitor: Configuration update, pool expansion
3. Verify: Connections available, no exhaustion

**Expected impact**: None (increases capacity)

**Rollback**: Revert configuration change

### Clear Disk Space (Medium Risk)
**When to use**: Disk space exhaustion

**Procedure**:
1. Identify safe-to-delete files (old logs, temp files)
2. Execute: `execute_remediation("clear_disk_space", "service-name")`
3. Monitor: Disk usage decreasing
4. Verify: Service writing successfully

**Expected impact**: Minimal, may lose old logs

**Rollback**: N/A (files deleted)

## Remediation Plan Template

When proposing remediation, structure it:

1. **Root Cause**: Brief summary from diagnostics
2. **Proposed Action**: Specific remediation from runbook
3. **Risk Level**: Low/Medium/High
4. **Expected Impact**: Downtime, data loss, user impact
5. **Recovery Time**: How long until service restored
6. **Rollback Plan**: How to undo if it doesn't work
7. **Approval Required**: Yes (always for production)

## Follow-up Actions

After remediation, always recommend:

1. **Monitoring**: What to watch for recurrence
2. **Post-mortem**: Schedule incident review
3. **Prevention**: Long-term fixes (increase limits, fix leaks, etc.)
4. **Documentation**: Update runbooks with learnings
