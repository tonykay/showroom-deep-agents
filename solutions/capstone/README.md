# Capstone Solution: AIOps Team

Reference implementation for Module 10 (Capstone: AIOps Team).

**This is the answer key** — use it to check your work or get unstuck, not as a shortcut.

## Structure

```
aiops/
  agent.py           # ops_manager orchestrator
  loader.py          # YAML subagent loader with tool/skill mapping
  tools.py           # Custom tools (fetch_logs, query_metrics, execute_remediation)
  subagents.yaml     # Three SRE specialist definitions
  AGENTS.md          # Operational context and memory
  skills/
    log-analysis/    # Error pattern detection procedures
    diagnostics/     # Root cause analysis decision trees
    remediation/     # Risk-classified runbooks
```

## Running

```bash
cd solutions/capstone
uv run python aiops/agent.py
```

Set `DEEPAGENTS_MODEL` to use a different model:

```bash
export DEEPAGENTS_MODEL="ollama:llama3.1:8b"
uv run python aiops/agent.py
```
