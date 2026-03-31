# AIOps Team Operational Context

## Environment

**Production Environment**:
- 3 application servers (payment-api, inventory-api, user-api)
- 1 PostgreSQL database (primary + read replica)
- 1 Redis cache cluster
- Kubernetes orchestration
- Prometheus + Grafana monitoring

**Resource Limits**:
- Application containers: 512Mi memory, 1 CPU
- Database: 4Gi memory, 2 CPU
- Redis: 2Gi memory, 1 CPU

**Connection Pools**:
- Default max connections: 100 per service
- Database max connections: 500 total
- Typical load: 20-30 connections per service

## Known Failure Modes

1. **Connection Pool Exhaustion** (seen 3 times in last month)
   - Usually during traffic spikes
   - Often combined with slow database queries
   - Resolution: increase pool size or optimize queries

2. **Memory Leaks** (payment-api specifically)
   - Gradual memory growth over 3-4 days
   - Requires weekly restarts as workaround
   - Fix in progress: PR #1247

3. **Database Deadlocks** (rare but recurring)
   - Complex transaction interactions
   - Usually during bulk operations
   - Retry logic handles most cases

## Escalation Procedures

**Low Risk Actions** (no escalation required):
- Service restart
- Scale up resources
- Clear disk space

**Medium Risk Actions** (notify on-call lead):
- Rollback deployment
- Connection pool reset
- Configuration changes

**High Risk Actions** (require senior approval):
- Database failover
- Emergency maintenance
- Data restoration

## Recent Incidents

**2026-03-28**: payment-api OOM due to traffic spike during flash sale
- Resolution: scaled up from 3 to 6 instances
- Prevention: auto-scaling rules updated

**2026-03-25**: inventory-api connection pool exhaustion
- Resolution: increased pool size from 100 to 150
- Prevention: monitoring alert added

**2026-03-20**: user-api deployment rollback (authentication regression)
- Resolution: rolled back to v2.4.1
- Prevention: added auth integration tests
