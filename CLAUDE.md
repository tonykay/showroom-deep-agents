# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Project Purpose

A zero-to-hero Antora-based multi-module workshop on **LangChain Deep Agents** (`pip install deepagents`). Built on the [Showroom template](https://github.com/rhpds/showroom_template_nookbag.git) for Red Hat Demo Platform. The workshop progresses from basics through advanced use cases, with strong coverage of:

- **Subagents** -- context-isolated child agents defined declaratively and loaded via YAML
- **Skills** -- progressive-disclosure capability files (Agent Skills spec / SKILL.md)
- **The Deep Agents CLI** -- Textual-based TUI for interactive agent work
- **Python SDK** -- `create_deep_agent()` factory, middleware stack, backends

## Key Reference Repositories

- Deep Agents SDK + CLI + examples: `https://github.com/langchain-ai/deepagents.git`
  - `examples/content-builder-agent/` -- canonical example: YAML subagents + skills + memory
  - `libs/deepagents/` -- core SDK source
  - `libs/cli/` -- CLI tool source
- Showroom template: `https://github.com/rhpds/showroom_template_nookbag.git`

## Build & Preview

```bash
# Local preview with Antora viewer (preferred)
podman run --rm --name antora -v $PWD:/antora -p 8080:8080 -i -t ghcr.io/juliaaano/antora-viewer

# On SELinux systems, append :z to the volume mount
podman run --rm --name antora -v $PWD:/antora:z -p 8080:8080 -i -t ghcr.io/juliaaano/antora-viewer

# Full local Showroom experience with terminal + code editor
./localroom.sh start
```

Output goes to `www/` (gitignored). Site config is in `site.yml`. GitHub Pages auto-deploys on push to main.

## Content Structure (Antora)

```
content/
  antora.yml              # Component descriptor (name, nav, asciidoc attributes)
  modules/ROOT/
    nav.adoc              # Left-nav table of contents
    pages/                # AsciiDoc page files (numbered: 01-overview.adoc, etc.)
    assets/images/        # Screenshots and diagrams
    examples/             # Downloadable code samples
    partials/             # Reusable content fragments
notebooks/                # Jupyter notebooks (downloadable via wget)
solutions/capstone/       # Complete AIOps capstone reference implementation
```

- **antora.yml** defines the component name, version, nav file, and asciidoc attributes
- **nav.adoc** controls the sidebar navigation; every page must be listed here via `xref:` links
- Pages are numbered for ordering: `01-overview.adoc`, `02-details.adoc`, `03-first-agent.adoc`, etc.

## Content Conventions (Showroom Workshop Format)

- Use **second-person narrative** ("You" not "participants")
- **Numbered steps** in every exercise (AsciiDoc ordered list `. Step:` syntax)
- Executable commands use `[source,role="execute"]` blocks (Showroom renders these as click-to-run with copy button)
- Non-executable code uses standard `[source,python]` / `[source,yaml]` etc.
- **Sample outputs** after commands: `.Sample output (your results may vary)` followed by plain `----` block (no role)
- **Long outputs** truncated: first ~5 lines, `...`, last ~5 lines
- **Separate file creation from execution**: `cat > file.py << 'EOF'` in one step, `uv run file.py` in the next
- File creation uses `cat > filename << 'EOF'` pattern inside execute blocks
- Images: `image::name.png[align="center",link=self,window=blank,width=700]`
- Keyboard keys use `kbd:[Ctrl+C]` syntax (experimental attribute is enabled)
- Each module ends with a summary section
- Tabs use `[tabs]` blocks (asciidoctor-tabs extension) — only for simple single-command variants, not multi-step content
- Workshop templates in `examples/workshop/templates/` for structural reference

## Code Example Conventions

All Python scripts in the workshop follow these patterns:

```python
import os
from deepagents import create_deep_agent
from utils import agent_response  # handles string and list content formats

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")
FAST_MODEL = os.environ.get("DEEPAGENTS_FAST_MODEL", "anthropic:claude-haiku-4-5-20251001")

agent = create_deep_agent(model=MODEL)
result = agent.invoke({"messages": [("user", "...")]})
print(agent_response(result))
```

- **`utils.py`** created in setup module -- `agent_response()` handles both string content (Anthropic) and list-of-blocks content (vLLM/LiteLLM endpoints)
- **`MODEL` from env var** -- students swap models with `export DEEPAGENTS_MODEL="openai:llama-scout-17b"` without editing code
- **`OPENAI_API_BASE`** for remote endpoints -- LangChain's OpenAI integration honors this automatically
- **`uv run script.py`** -- no `python` prefix needed, uv detects `.py`

## Backend Patterns

- **`FilesystemBackend(root_dir=WORKSPACE, virtual_mode=False)`** -- file operations only (read/write/edit/ls/glob/grep). Always pass absolute path via `os.path.abspath()` and add system prompt: `f"Your working directory is {WORKSPACE}."`
- **`LocalShellBackend(root_dir=WORKSPACE, virtual_mode=False)`** -- file operations + `execute` tool for shell commands. Required for any exercise needing shell execution.
- **`StateBackend`** -- ephemeral in-memory filesystem, no real disk writes. This is the DEFAULT backend (used when no `backend` parameter is passed). Do NOT instantiate directly (`StateBackend()` fails) -- just omit the `backend` parameter.
- The `execute` tool subprocess may not inherit user's PATH -- use basic commands (`ls`, `date`, `cat`) or absolute paths

## Site.yml Notes

- `@asciidoctor/tabs` extension enabled for tabbed content (Podman/Docker, oc/kubectl)
- `supplemental_files` override `footer-scripts.hbs` and `head-styles.hbs` -- **must preserve `clipboard.js`** for copy buttons
- Mermaid extension enabled for architecture diagrams
- GitHub Actions workflow installs both global and local `@asciidoctor/tabs` (supplemental_files reads from local `node_modules/`)

## Deep Agents Framework -- Key Concepts

### Core API

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[...],
    system_prompt="...",
    subagents=[...],
    skills=["./skills/"],
    memory=["./AGENTS.md"],
    backend=FilesystemBackend(root_dir="/path", virtual_mode=False),
)
```

Returns a compiled LangGraph `CompiledStateGraph`.

### Four Pillars

1. **Detailed System Prompt** -- comprehensive base prompt teaching tool use
2. **Planning (TodoListMiddleware)** -- `write_todos` tool for task breakdown
3. **Sub-agents** -- ephemeral child agents via `task` tool for context isolation
4. **Filesystem Access** -- `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep` (+ `execute` with LocalShellBackend)

### Known Issues with Models

- Reasoning models (qwen3-235b, gpt-oss-120b, o-series) crash `langchain-openai` with `TypeError` -- use non-reasoning models
- Remote OpenAI-compatible endpoints may return content as list of dicts -- `agent_response()` in utils.py handles this
- deepagents CLI has no `--system-prompt` flag -- custom system prompts are programmatic only

## Global Development Tools

- **Skill**: `~/.claude/skills/deep-agents-dev/SKILL.md` -- enforces all code patterns automatically when working with deepagents code (any project)
- **MCP Server**: `deepagents-docs` -- serves live docs from `https://docs.langchain.com/llms.txt` (LangChain, LangGraph, Deep Agents API)

## Style Notes

- Always use Pydantic V2 for structured outputs with OpenAI API
- Python code examples should use modern Python (3.13+, type hints)
- Use `uv` as the preferred package manager (never pip)
- Deep Agents model format is `"provider:model-name"` (e.g., `"anthropic:claude-sonnet-4-6"`)
