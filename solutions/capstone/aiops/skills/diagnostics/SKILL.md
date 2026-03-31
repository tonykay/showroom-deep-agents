---
name: diagnostics
description: Diagnostic decision trees and failure mode knowledge for determining root causes of service incidents.
---

# Diagnostic Skill

## Common Failure Modes

### Out of Memory (OOM)
**Symptoms**:
- OOM kill messages in logs
- Container restarts
- Memory metrics at/near limit

**Diagnostic Steps**:
1. Check memory trend before failure (gradual vs sudden)
2. Review application memory profile
3. Check for memory leaks (heap dumps if available)
4. Verify memory limits are appropriate

**Common Causes**:
- Memory leak in application code
- Undersized container limits
- Traffic spike exceeding capacity
- Memory-intensive operations (large queries, caching)

### Connection Pool Exhaustion
**Symptoms**:
- "Connection pool exhausted" errors
- Timeouts waiting for connections
- Service degradation under load

**Diagnostic Steps**:
1. Check current vs max connection settings
2. Review connection lifecycle (are connections released?)
3. Check for long-running queries holding connections
4. Verify downstream service health

**Common Causes**:
- Connection leaks (not closing properly)
- Pool sized too small for load
- Downstream service slowness
- Database performance issues

### Disk Space Exhaustion
**Symptoms**:
- "No space left on device"
- Write failures
- Application crashes

**Diagnostic Steps**:
1. Check disk usage metrics
2. Identify largest files/directories
3. Review log rotation policies
4. Check for unexpected data growth

**Common Causes**:
- Log rotation not configured
- Temporary file buildup
- Database/cache growth
- Failed cleanup jobs

### DNS/Network Issues
**Symptoms**:
- "Name resolution failed"
- "Connection timed out"
- Intermittent connectivity

**Diagnostic Steps**:
1. Check DNS resolution for affected services
2. Verify network connectivity paths
3. Review firewall/security group rules
4. Check for network congestion

**Common Causes**:
- DNS server issues
- Network partition
- Firewall rule changes
- Service mesh configuration

### Certificate Expiry
**Symptoms**:
- "Certificate has expired"
- TLS handshake failures
- Sudden service unavailability

**Diagnostic Steps**:
1. Check certificate expiration dates
2. Verify certificate chain validity
3. Review renewal automation
4. Check for certificate mismatch

**Common Causes**:
- Expired certificates
- Failed auto-renewal
- Certificate configuration errors

## Diagnostic Decision Tree

```
START: Service degradation or failure
  |
[Check recent changes]
  -> Recent deployment? -> Likely: Code regression or config change
  -> Infrastructure change? -> Likely: Resource/network issue
  -> No changes? -> Continue to symptoms
  |
[Examine error patterns]
  -> OOM/memory errors? -> Run OOM diagnostics
  -> Connection errors? -> Run connection pool diagnostics
  -> Disk errors? -> Run disk space diagnostics
  -> Network/timeout? -> Run network diagnostics
  -> Certificate errors? -> Run certificate diagnostics
  |
[Validate hypothesis]
  -> Query metrics to confirm
  -> Check correlating events
  -> Assess confidence (high/medium/low)
  |
[Recommend remediation]
```

## Confidence Assessment

Rate your diagnostic confidence:

- **High**: Clear evidence, well-known failure mode, metrics confirm
- **Medium**: Evidence present but some ambiguity, metrics partially confirm
- **Low**: Multiple possible causes, limited evidence, recommend deeper investigation
