---
name: log-analysis
description: Expert procedures for analyzing application and infrastructure logs to identify error patterns, anomalies, and failure sequences.
---

# Log Analysis Skill

## Error Pattern Detection

When analyzing logs, look for these common patterns:

### Connection Pool Exhaustion
- `Connection pool exhausted`
- `max connections reached`
- `Timeout waiting for connection`
- Often followed by cascading failures

### Out of Memory (OOM)
- `OOM Kill`
- `container memory limit exceeded`
- `java.lang.OutOfMemoryError`
- `GC overhead limit exceeded`
- Usually preceded by gradual memory growth

### Database Issues
- `deadlock detected`
- `too many connections`
- `connection refused`
- `query timeout`
- Check for long-running queries

### Network Problems
- `connection reset by peer`
- `connection timed out`
- `no route to host`
- `DNS resolution failed`

## Anomaly Detection

Watch for deviations from normal patterns:

1. **Frequency anomalies**: Error rates spiking from <1% to >5%
2. **Timing anomalies**: Response times jumping 10x or more
3. **Volume anomalies**: Traffic patterns changing dramatically
4. **Sequence anomalies**: Errors in unexpected order

## Correlation Analysis

Look for correlations between events:

- Error spikes correlated with deployments
- Resource exhaustion preceding service failures
- Cascading failures (A fails, then B, then C)
- Time-based patterns (daily cycles, weekly patterns)

## Output Format

Structure your findings:
1. **Timeline**: Chronological sequence of key events
2. **Patterns**: Identified error patterns with examples
3. **Anomalies**: Deviations from baseline behavior
4. **Metrics**: Supporting data (error rates, response times, resource usage)
5. **Hypothesis**: Initial theory about what went wrong
