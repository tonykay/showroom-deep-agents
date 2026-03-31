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
```

Output goes to `www/` (gitignored). Site config is in `site.yml`.

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
```

- **antora.yml** defines the component name, version, nav file, and asciidoc attributes (including runtime-injected vars like `{guid}`, `{bastion_public_hostname}`)
- **nav.adoc** controls the sidebar navigation; every page must be listed here via `xref:` links
- Pages are numbered for ordering: `01-overview.adoc`, `02-details.adoc`, `03-module-01.adoc`, etc.

## Content Conventions (Showroom Workshop Format)

- Use **second-person narrative** ("You" not "participants")
- Executable commands use `[source,role="execute"]` blocks (Showroom renders these as click-to-run)
- Non-executable code uses standard `[source,python]` / `[source,yaml]` etc.
- File creation uses `cat > filename << 'EOF'` pattern inside execute blocks
- Images: `image::name.png[align="center",link=self,window=blank,width=700]`
- Each module ends with a summary section: what was accomplished, key takeaways, next steps preview
- Workshop templates live in `examples/workshop/templates/` -- use these as structural references
- Demo templates live in `examples/demo/templates/`

## Deep Agents Framework -- Key Concepts for Content

### Core API

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[...],
    system_prompt="...",
    subagents=[...],           # SubAgent | CompiledSubAgent | AsyncSubAgent
    skills=["./skills/"],      # Paths to skill directories
    memory=["./AGENTS.md"],    # Paths to AGENTS.md files
    backend=FilesystemBackend(root_dir="/"),
)
```

Returns a compiled LangGraph `CompiledStateGraph`.

### Four Pillars

1. **Detailed System Prompt** -- comprehensive base prompt teaching tool use
2. **Planning (TodoListMiddleware)** -- `write_todos` tool for task breakdown
3. **Sub-agents** -- ephemeral child agents via `task` tool for context isolation
4. **Filesystem Access** -- `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `execute`

### Subagent Patterns

Subagents are `TypedDict` dicts with `name`, `description`, `system_prompt`, and optional `tools`, `model`, `skills`. The SDK does NOT natively load from YAML -- the content-builder-agent example uses a custom `load_subagents()` helper:

```yaml
# subagents.yaml
researcher:
  description: >
    ALWAYS use this first to research any topic...
  model: anthropic:claude-haiku-4-5-20251001
  system_prompt: |
    You are a research assistant...
  tools:
    - web_search
```

```python
def load_subagents(config_path):
    available_tools = {"web_search": web_search}
    config = yaml.safe_load(open(config_path))
    return [{"name": name, **spec, "tools": [available_tools[t] for t in spec.get("tools", [])]}
            for name, spec in config.items()]
```

### Skills

Follow the Agent Skills spec (agentskills.io). Progressive disclosure -- only name/description loaded initially; full SKILL.md read on demand.

```
skills/
  blog-post/
    SKILL.md    # YAML frontmatter (name, description) + markdown instructions
```

### Middleware Stack (applied in order)

TodoList -> Skills -> Filesystem -> SubAgent -> Summarization -> PatchToolCalls -> AnthropicPromptCaching -> Memory -> HumanInTheLoop

### Three Subagent Types

- **SubAgent** (declarative dict, sync) -- most common
- **CompiledSubAgent** (wraps any LangGraph Runnable)
- **AsyncSubAgent** (remote LangGraph deployment, non-blocking)

### Backend System

Pluggable: `FilesystemBackend`, `StateBackend`, `StoreBackend`, `CompositeBackend`, `SandboxBackendProtocol`

## Workshop Module Plan (Reference)

The workshop should cover these topics progressively:

1. **Overview & Setup** -- What Deep Agents are, install, first agent
2. **Core Concepts** -- System prompts, planning/todos, filesystem tools
3. **Subagents** -- Defining subagents, YAML configuration, the `task` tool, context isolation
4. **Skills** -- SKILL.md format, progressive disclosure, skill directories, layering
5. **Memory** -- AGENTS.md spec, self-updating memory, MemoryMiddleware
6. **Multi-Agent Applications** -- Combining subagents + skills, the content-builder pattern
7. **CLI** -- deepagents-cli TUI, headless mode, custom skills in CLI
8. **Advanced** -- Custom backends, CompositeBackend, AsyncSubAgent, human-in-the-loop

## Style Notes

- Always use Pydantic V2 for structured outputs with OpenAI API
- Python code examples should use modern Python (3.10+ match statements, type hints)
- Use `uv` as the preferred package manager in examples where applicable
- Deep Agents model format is `"provider:model-name"` (e.g., `"anthropic:claude-sonnet-4-6"`)
