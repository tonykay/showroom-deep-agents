import yaml
from pathlib import Path
from tools import execute_remediation, fetch_logs, query_metrics


def load_subagents(config_path: Path) -> list:
    """Load subagent definitions from a YAML file.

    Maps tool name strings to actual tool objects and resolves
    skill paths. This is a custom utility for config-driven design.
    """
    # Registry of available tools
    available_tools = {
        "execute_remediation": execute_remediation,
        "fetch_logs": fetch_logs,
        "query_metrics": query_metrics,
    }

    with open(config_path) as f:
        config = yaml.safe_load(f)

    subagents = []
    for name, spec in config.items():
        subagent = {
            "name": name,
            "description": spec["description"],
            "model": spec["model"],
            "system_prompt": spec["system_prompt"],
        }

        # Map tool names to tool objects
        if "tools" in spec:
            subagent["tools"] = [
                available_tools[tool_name]
                for tool_name in spec["tools"]
            ]

        # Pass through skill paths
        if "skills" in spec:
            subagent["skills"] = spec["skills"]

        subagents.append(subagent)

    return subagents
