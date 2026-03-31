from langchain_core.tools import tool


@tool
def execute_remediation(action: str, target: str) -> str:
    """Execute a remediation action on a target system.

    REQUIRES HUMAN APPROVAL via interrupt mechanism.

    Args:
        action: The remediation action (e.g., 'restart', 'rollback_deployment')
        target: The target service or component
    """
    return f"[SIMULATED] Executed '{action}' on '{target}' — success"


@tool
def fetch_logs(service: str, minutes: int = 30) -> str:
    """Fetch recent logs from a service.

    Args:
        service: The service name
        minutes: How many minutes of logs to retrieve
    """
    return f"""[{service}] 2026-03-30T14:22:01Z ERROR Connection pool exhausted - max connections (100) reached
[{service}] 2026-03-30T14:22:03Z WARN Request queued - no available connections
[{service}] 2026-03-30T14:22:05Z ERROR Timeout waiting for database connection (30s)
[{service}] 2026-03-30T14:22:08Z ERROR 503 Service Unavailable returned to client
[{service}] 2026-03-30T14:22:10Z WARN Connection pool health check failed
[{service}] 2026-03-30T14:22:15Z ERROR OOM Kill: container memory limit (512Mi) exceeded
[{service}] 2026-03-30T14:22:18Z INFO Service restarted by orchestrator
[{service}] 2026-03-30T14:22:20Z WARN Connection pool re-initializing (0/100 connections)
[{service}] 2026-03-30T14:22:25Z ERROR Connection pool exhausted again after restart"""


@tool
def query_metrics(service: str, metric: str) -> str:
    """Query monitoring metrics for a service.

    Args:
        service: The service name
        metric: The metric to query (cpu, memory, connections, error_rate)
    """
    metrics = {
        "cpu": f"{service} CPU: 45% (normal: 20-30%)",
        "memory": f"{service} Memory: 498Mi / 512Mi (97% - CRITICAL)",
        "connections": f"{service} DB Connections: 100/100 (EXHAUSTED)",
        "error_rate": f"{service} Error Rate: 23% (normal: <1%)",
    }
    return metrics.get(metric, f"Unknown metric: {metric}")
