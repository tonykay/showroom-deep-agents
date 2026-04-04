import os
from pathlib import Path
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from loader import load_subagents
from tools import execute_remediation, fetch_logs, query_metrics
from utils import agent_response

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")

# Create the ops_manager orchestrator
agent = create_deep_agent(
    model=MODEL,
    system_prompt="""You are an AIOps operations manager coordinating incident response.

## Your Process

When an incident is reported:

1. **Analyze**: Delegate to sre_log_analyst to examine logs and metrics
2. **Diagnose**: Send findings to sre_diagnostician for root cause analysis
3. **Remediate**: If needed, delegate to sre_remediator with approval gate
4. **Report**: Compile a final incident report with timeline and actions

## Delegation Strategy

- Use clear, specific task descriptions when delegating
- Provide context from previous steps to each subagent
- Coordinate the handoffs between specialists
- Ensure human approval for any remediation actions

## Incident Report Format

Your final output should include:
- Incident summary (what happened, when, impact)
- Timeline of investigation and actions
- Root cause analysis
- Remediation actions taken
- Follow-up recommendations""",
    memory=["./aiops/AGENTS.md"],
    skills=["./aiops/skills/"],
    subagents=load_subagents(Path("aiops/subagents.yaml")),
    tools=[fetch_logs, query_metrics, execute_remediation],
    interrupt_on={"execute_remediation": True},
    backend=FilesystemBackend(root_dir="./aiops"),
)

if __name__ == "__main__":
    # Test with a realistic incident
    result = agent.invoke({"messages": [("user",
        "INCIDENT ALERT: Service 'payment-api' is returning 503 errors. "
        "Error rate spiked from <1% to 23% in the last 10 minutes. "
        "Multiple customers reporting failed transactions. "
        "Investigate and propose remediation."
    )]})

    print(agent_response(result))
