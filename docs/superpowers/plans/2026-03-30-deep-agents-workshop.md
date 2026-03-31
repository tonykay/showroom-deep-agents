# Deep Agents Workshop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 10-module Antora/Showroom workshop teaching LangChain Deep Agents from first agent through a production AIOps multi-agent capstone.

**Architecture:** Antora static site using the Showroom template. Each module is a standalone `.adoc` file in `content/modules/ROOT/pages/`. Navigation controlled by `nav.adoc`. Code examples are inline in AsciiDoc with `[source,role="execute"]` for terminal commands and `[source,python]` for readable code. The existing template pages (Showroom docs) are removed and replaced with workshop content.

**Tech Stack:** Antora, AsciiDoc, Showroom UI bundle, Podman/Docker for builds

**Design Spec:** `docs/superpowers/specs/2026-03-30-deep-agents-workshop-design.md`

**Verification command (use after every content task):**
```bash
# Build Antora site and check for errors
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

If `podman` is unavailable, use `docker` instead. A successful build shows `Site generation complete!` with no errors. Warnings about missing images are acceptable during development.

**Parallelization note:** Tasks 3-16 (individual content pages) are independent of each other and can be executed in parallel by subagents. Only Task 1 (scaffold) and Task 2 (nav) must complete first, as they establish the file structure other tasks depend on.

---

## File Structure

### Files to delete (existing template content)
All files in `content/modules/ROOT/pages/` — these are Showroom's own documentation and will be replaced with workshop content:
- `agnosticv-config.adoc`, `architecture.adoc`, `attribute-example.adoc`, `content-repo.adoc`, `contributing.adoc`, `deployer.adoc`, `images.adoc`, `index.adoc`, `nookbag.adoc`, `ocp-integration.adoc`, `ocp4-role-reference.adoc`, `quick-start.adoc`, `ui-config.adoc`, `user-data.adoc`, `vm-role-reference.adoc`

### Files to modify
- `content/antora.yml` — update component name, title, and attributes for the Deep Agents workshop
- `site.yml` — update site title and URL
- `ui-config.yml` — update tabs for workshop context (Deep Agents docs link)
- `content/modules/ROOT/nav.adoc` — replace with workshop navigation

### Files to create
- `content/modules/ROOT/pages/index.adoc` — Welcome page
- `content/modules/ROOT/pages/01-overview.adoc` — Workshop overview
- `content/modules/ROOT/pages/02-details.adoc` — Environment setup
- `content/modules/ROOT/pages/03-first-agent.adoc` — Module 1
- `content/modules/ROOT/pages/04-system-prompts-planning.adoc` — Module 2
- `content/modules/ROOT/pages/05-filesystem-backends.adoc` — Module 3
- `content/modules/ROOT/pages/06-custom-tools.adoc` — Module 4
- `content/modules/ROOT/pages/07-subagent-fundamentals.adoc` — Module 5
- `content/modules/ROOT/pages/08-yaml-subagents.adoc` — Module 6
- `content/modules/ROOT/pages/09-skills.adoc` — Module 7
- `content/modules/ROOT/pages/10-memory.adoc` — Module 8
- `content/modules/ROOT/pages/11-cli.adoc` — Module 9
- `content/modules/ROOT/pages/12-capstone-aiops.adoc` — Module 10
- `content/modules/ROOT/pages/99-conclusion.adoc` — Wrap-up

---

## Task 1: Scaffold — Config files and cleanup

**Files:**
- Modify: `content/antora.yml`
- Modify: `site.yml`
- Modify: `ui-config.yml`
- Delete: all existing files in `content/modules/ROOT/pages/`

This task sets up the project identity and removes the Showroom template docs that will be replaced by workshop content.

- [ ] **Step 1: Delete existing template pages**

```bash
rm content/modules/ROOT/pages/*.adoc
```

- [ ] **Step 2: Update `content/antora.yml`**

Replace the entire file with:

```yaml
name: modules
title: Deep Agents Workshop
version: ~
nav:
  - modules/ROOT/nav.adoc

asciidoc:
  attributes:
    experimental: true
    page-pagination: true
    source-highlighter: rouge
```

The Showroom-specific attributes (`guid`, `bastion_public_hostname`, etc.) are removed since this is a local-laptop workshop with no provisioned infrastructure.

- [ ] **Step 3: Update `site.yml`**

Replace the entire file with:

```yaml
---
site:
  title: "Deep Agents: From First Agent to Production Multi-Agent Systems"
  url: https://github.com/rhpds/showroom_template_nookbag
  start_page: modules::index.adoc

content:
  sources:
    - url: .
      start_path: content

ui:
  bundle:
    url: https://github.com/rhpds/rhdp_showroom_theme/releases/download/rh-summit-2025/ui-bundle.zip
    snapshot: true

antora:
  extensions:
    - require: '@sntke/antora-mermaid-extension'
      mermaid_library_url: https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs
      script_stem: header-scripts
      mermaid_initialize_options:
        start_on_load: true

output:
  dir: ./www
```

- [ ] **Step 4: Update `ui-config.yml`**

Replace the entire file with:

```yaml
---
type: showroom

default_width: 30
persist_url_state: true

view_switcher:
  enabled: true
  default_mode: split

tabs:
  - name: Deep Agents Docs
    url: 'https://github.com/langchain-ai/deepagents'
```

- [ ] **Step 5: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

Expected: Build may warn about missing `index.adoc` (since we deleted it and haven't created the new one yet). That's fine — this confirms the config is valid YAML and Antora can parse it.

- [ ] **Step 6: Commit**

```bash
git add -A content/modules/ROOT/pages/ content/antora.yml site.yml ui-config.yml
git commit -m "scaffold: replace template with Deep Agents workshop config

Remove Showroom template docs, update antora.yml, site.yml, and
ui-config.yml for the Deep Agents workshop."
```

---

## Task 2: Navigation — `nav.adoc`

**Files:**
- Create: `content/modules/ROOT/nav.adoc` (overwrite existing)

This task defines the full sidebar navigation for the workshop. All page xrefs are included even though the pages don't exist yet — they'll be created in subsequent tasks.

- [ ] **Step 1: Write `nav.adoc`**

```asciidoc
* xref:index.adoc[Deep Agents Workshop]

.Getting Started
* xref:01-overview.adoc[Workshop Overview]
* xref:02-details.adoc[Environment Setup]

.Foundations
* xref:03-first-agent.adoc[Your First Deep Agent]
* xref:04-system-prompts-planning.adoc[System Prompts & Planning]
* xref:05-filesystem-backends.adoc[Filesystem Tools & Backends]
* xref:06-custom-tools.adoc[Custom Tools]

.Multi-Agent Systems
* xref:07-subagent-fundamentals.adoc[Subagent Fundamentals]
* xref:08-yaml-subagents.adoc[YAML Subagents & the Loader Pattern]
* xref:09-skills.adoc[Skills & Progressive Disclosure]
* xref:10-memory.adoc[Memory & AGENTS.md]

.CLI & Capstone
* xref:11-cli.adoc[The Deep Agents CLI]
* xref:12-capstone-aiops.adoc[Capstone: AIOps Team]

.Wrap-Up
* xref:99-conclusion.adoc[Conclusion & Next Steps]
```

- [ ] **Step 2: Commit**

```bash
git add content/modules/ROOT/nav.adoc
git commit -m "nav: add full workshop sidebar navigation"
```

---

## Task 3: Welcome Page — `index.adoc`

**Files:**
- Create: `content/modules/ROOT/pages/index.adoc`

The landing page. Brief, welcoming, sets expectations.

- [ ] **Step 1: Write `index.adoc`**

Content requirements:
- Title: "Deep Agents: From First Agent to Production Multi-Agent Systems"
- Subtitle/tagline: hands-on workshop building real AI agent systems with LangChain's Deep Agents framework
- "What you'll learn" section: 4-5 bullet points covering the four pillars, subagents, skills, CLI, and the AIOps capstone
- "How this workshop works" section: explain top-down approach (working agent first, then peel back layers), self-contained modules with capstone synthesis, estimated ~8 hours total
- "Prerequisites" section: Python experience, familiarity with LLM APIs (OpenAI/Anthropic SDK), no LangChain/LangGraph experience required
- "Let's get started" call-to-action pointing to the overview page
- Use second-person narrative throughout

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

Expected: `Site generation complete!` — warnings about missing pages referenced in nav.adoc are acceptable.

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/index.adoc
git commit -m "content: add workshop welcome page"
```

---

## Task 4: Workshop Overview — `01-overview.adoc`

**Files:**
- Create: `content/modules/ROOT/pages/01-overview.adoc`

- [ ] **Step 1: Write `01-overview.adoc`**

Content requirements:
- Title: "Workshop Overview"
- **"What are Deep Agents?"** section: Explain what Deep Agents is -- an open-source "agent harness" by LangChain (MIT licensed). Beyond simple tool-calling LLM loops. Inspired by Claude Code. `pip install deepagents` / `uv add deepagents`. Include the ecosystem positioning: `deepagents` = agent harness (opinionated, ready-to-run), `langchain` = agent framework (building blocks), `langgraph` = agent runtime (execution infrastructure). Note that `create_deep_agent()` returns a compiled LangGraph graph.
- **"The Four Pillars"** section: Brief overview of each pillar with 2-3 sentences each:
  1. Detailed System Prompt -- comprehensive base prompt teaching the model how to use tools
  2. Planning (TodoListMiddleware) -- `write_todos` tool for task breakdown, context engineering strategy
  3. Sub-agents -- ephemeral child agents with isolated context windows via the `task` tool
  4. Filesystem Access -- built-in tools (`read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `execute`) with pluggable backends
- **"What you'll build"** section: Module-by-module summary table (module number, title, 1-line description). End with the AIOps capstone preview.
- **"Target audience"** section: Python developers familiar with LLM APIs, light LangChain/LangGraph refreshers provided where relevant
- Use a mermaid diagram showing the four pillars architecture (this tests the mermaid extension configured in site.yml):

```
[mermaid]
....
graph TD
    A[Deep Agent] --> B[System Prompt]
    A --> C[Planning / Todos]
    A --> D[Sub-agents]
    A --> E[Filesystem / Backends]
    D --> F[task tool]
    F --> G[Isolated Context]
....
```

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/01-overview.adoc
git commit -m "content: add workshop overview with four pillars introduction"
```

---

## Task 5: Environment Setup — `02-details.adoc`

**Files:**
- Create: `content/modules/ROOT/pages/02-details.adoc`

- [ ] **Step 1: Write `02-details.adoc`**

Content requirements:
- Title: "Environment Setup"
- All commands use `[source,role="execute"]` blocks so they're click-to-run in the Showroom terminal
- **"Install Python 3.13+"** section: verify with `python3 --version`. Brief note on pyenv/brew if needed.
- **"Install uv"** section:

```
[source,role="execute"]
----
curl -LsSf https://astral.sh/uv/install.sh | sh
----
```

Verify: `uv --version`

- **"Create your workshop project"** section:

```
[source,role="execute"]
----
uv init deep-agents-workshop
cd deep-agents-workshop
uv add deepagents
----
```

- **"Set your API key"** section:

```
[source,role="execute"]
----
export ANTHROPIC_API_KEY="your-key-here"
----
```

Explain where to get a key (console.anthropic.com), note that it's needed for all modules.

- **"Validate your setup"** section: create and run a validation script:

```
[source,role="execute"]
----
cat > validate_setup.py << 'EOF'
from deepagents import create_deep_agent

agent = create_deep_agent()
print("Deep Agents installed successfully!")
print(f"Agent type: {type(agent).__name__}")
EOF
uv run python validate_setup.py
----
```

Expected output: prints success message and `CompiledStateGraph`.

- **"Install the Deep Agents CLI"** section:

```
[source,role="execute"]
----
curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash
----
```

Verify: `deepagents --help`

- **"Optional: Local Showroom experience"** section: brief mention of `./localroom.sh start` for the full split-pane UI. Not required but recommended.

- **"Troubleshooting"** section: common issues (Python version too old, API key not set, uv not on PATH)

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/02-details.adoc
git commit -m "content: add environment setup guide"
```

---

## Task 6: Module 1 — Your First Deep Agent (`03-first-agent.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/03-first-agent.adoc`

- [ ] **Step 1: Write `03-first-agent.adoc`**

Content requirements:
- Title: "Your First Deep Agent"
- `:source-highlighter: rouge` attribute
- Brief intro: you'll have a working agent in under 5 minutes
- **Learning objectives** section (4 bullets)

- **Exercise 1: Hello Deep Agent** — create and run a minimal agent:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(model="anthropic:claude-sonnet-4-6")

result = agent.invoke({"messages": [("user", "What tools do you have available?")]})

for message in result["messages"]:
    print(f"{message.type}: {message.content[:200]}")
```

Write this to a file with `cat > hello_agent.py << 'EOF'` then run with `uv run python hello_agent.py`. Explain what comes back -- the response is a dict with a `messages` key containing the conversation history. Point out that the agent mentions its built-in tools (filesystem tools, write_todos, task).

- **Exercise 2: Streaming responses** — switch to streaming:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(model="anthropic:claude-sonnet-4-6")

for event in agent.stream({"messages": [("user", "Write a haiku about Python programming")]}):
    for key, value in event.items():
        if key == "messages":
            for msg in value:
                if hasattr(msg, 'content') and msg.content:
                    print(msg.content, end="", flush=True)
print()
```

Explain the LangGraph event stream format. Each event is a dict keyed by the node that produced it.

- **Exercise 3: Exploring defaults** — ask the agent what it can do. Have the student invoke the agent with a prompt like "List all the tools you have access to and briefly describe each one." Discuss the output -- the agent should mention `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `execute`, `write_todos`, and `task`. Explain that these are the four pillars in action: filesystem tools (Pillar 4), planning via write_todos (Pillar 2), and sub-agents via task (Pillar 3). Pillar 1 (the system prompt) is what taught the agent how to describe and use all of these.

- **Exercise 4: CLI first look** — run the same prompt interactively:

```
[source,role="execute"]
----
deepagents
----
```

Brief walkthrough: type a message, see streaming response, observe tool calls rendered in the TUI. Exit with Ctrl+C. Note: "We'll explore the CLI in depth in Module 11, but you'll see CLI callouts throughout the workshop."

- **Module summary**: what you accomplished (created and invoked a deep agent, streamed responses, explored built-in capabilities, used the CLI), key takeaways (create_deep_agent() gives you a fully-equipped agent out of the box, it returns a LangGraph CompiledStateGraph, the four pillars are already working), next module preview (customizing system prompts and planning).

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/03-first-agent.adoc
git commit -m "content: add Module 1 — Your First Deep Agent"
```

---

## Task 7: Module 2 — System Prompts & Planning (`04-system-prompts-planning.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/04-system-prompts-planning.adoc`

- [ ] **Step 1: Write `04-system-prompts-planning.adoc`**

Content requirements:
- Title: "System Prompts & Planning"
- Brief intro connecting to Module 1: now that you have a working agent, let's control how it thinks and plans

- **Exercise 1: Custom system prompts** — create an agent with a persona:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="""You are a senior Python code reviewer.
When reviewing code, always check for:
1. Type safety and proper type hints
2. Error handling
3. Security vulnerabilities
4. Performance considerations

Be direct and specific in your feedback.""",
)

result = agent.invoke({"messages": [("user", """Review this code:

def get_user(id):
    data = eval(open(f"users/{id}.json").read())
    return data
""")]})

print(result["messages"][-1].content)
```

Explain that `system_prompt` is prepended to the `BASE_AGENT_PROMPT` — the agent still has all its built-in capabilities, but now also has your custom instructions.

- **Exercise 2: The base prompt** — explore what `BASE_AGENT_PROMPT` contains:

```python
from deepagents.graph import BASE_AGENT_PROMPT

print(BASE_AGENT_PROMPT[:2000])
print(f"\n... ({len(BASE_AGENT_PROMPT)} total characters)")
```

Discuss what's in there: detailed tool usage instructions, behavioral guidelines, output formatting rules. This is the "detailed system prompt" pillar — it's not just "you are a helpful assistant", it's a comprehensive instruction manual.

- **Exercise 3: Planning with todos** — give the agent a complex multi-step task and observe planning:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(model="anthropic:claude-sonnet-4-6")

result = agent.invoke({"messages": [("user",
    "Create a Python project structure for a REST API with "
    "user authentication, database models, and tests. "
    "Plan out the work first, then create the files."
)]})

for msg in result["messages"]:
    if hasattr(msg, 'tool_calls'):
        for tc in msg.tool_calls:
            if tc['name'] == 'write_todos':
                print("Planning step detected!")
                print(f"Todos: {tc['args']}")
```

Explain that `write_todos` is the `TodoListMiddleware` in action — it's a simple tool, but serves as a context engineering strategy that keeps the agent organized on multi-step tasks.

- **Exercise 4: Guiding planning behavior** — use system prompt to influence how the agent plans:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="""Before starting any task:
1. Always create a todo list with write_todos
2. Break work into steps of no more than 3 files each
3. Complete and check off each step before moving to the next
4. Never skip the planning phase""",
)
```

Run with the same complex task and compare the planning behavior to the unprompted version.

- **CLI callout**: `deepagents --system-prompt "You are a Python expert..."` — show the CLI flag

- **Module summary**: accomplished, takeaways (system prompt prepends to base, base prompt is comprehensive, todos are context engineering), next preview (filesystem tools and backends)

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/04-system-prompts-planning.adoc
git commit -m "content: add Module 2 — System Prompts & Planning"
```

---

## Task 8: Module 3 — Filesystem Tools & Backends (`05-filesystem-backends.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/05-filesystem-backends.adoc`

- [ ] **Step 1: Write `05-filesystem-backends.adoc`**

Content requirements:
- Title: "Filesystem Tools & Backends"
- Brief intro: the agent's ability to read, write, and navigate files is what makes it useful for real development tasks

- **Exercise 1: Built-in file tools** — give the agent a task that exercises multiple file tools:

```python
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    backend=FilesystemBackend(root_dir="./workspace"),
)

result = agent.invoke({"messages": [("user",
    "Create a directory called 'myproject' with a README.md and a main.py file. "
    "The README should describe the project. The main.py should have a hello world function. "
    "Then list the files you created and read back the README to verify it."
)]})

print(result["messages"][-1].content)
```

First create the workspace dir: `mkdir -p workspace`. Walk through the response showing which tools the agent used (`write_file`, `ls`, `read_file`).

- **Exercise 2: The `execute` tool** — demonstrate shell command execution:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    backend=FilesystemBackend(root_dir="./workspace"),
)

result = agent.invoke({"messages": [("user",
    "Run 'python --version' and 'uv --version' to check what's installed, "
    "then run 'ls -la' to show the current directory."
)]})
```

Discuss sandboxing considerations — the `execute` tool runs real commands. The `root_dir` scoping on FilesystemBackend constrains file operations but `execute` can still access the broader system.

- **Exercise 3: FilesystemBackend** — demonstrate `root_dir` scoping:

```python
from deepagents.backends import FilesystemBackend

backend = FilesystemBackend(root_dir="./workspace/myproject")

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    backend=backend,
)

result = agent.invoke({"messages": [("user",
    "List all files in the current directory. "
    "Then try to read /etc/passwd."
)]})
```

Show that the agent can see files in `./workspace/myproject` but file operations outside `root_dir` are scoped. Discuss when and why you'd want this containment.

- **Exercise 4: StateBackend** — switch to ephemeral in-memory storage:

```python
from deepagents.backends import StateBackend

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    backend=StateBackend(),
)

result = agent.invoke({"messages": [("user",
    "Create a file called 'notes.txt' with some content. "
    "Then read it back to verify."
)]})

print(result["messages"][-1].content)
```

Explain that `StateBackend` stores files in LangGraph state — nothing touches the real filesystem. Useful for testing, sandboxed environments, and when you don't want agents writing to disk. Files only live for the duration of the conversation.

- **Exercise 5: Brief intro to CompositeBackend** — preview only, detailed use in capstone:

```python
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend

backend = CompositeBackend(
    mounts={
        "/workspace": FilesystemBackend(root_dir="./workspace"),
        "/scratch": StateBackend(),
    }
)
```

Explain the concept: layer multiple backends so different paths route to different storage. In the capstone, we'll use this to give the AIOps agent access to log files on disk while keeping scratch work in memory.

- **CLI callout**: note that the CLI uses `FilesystemBackend` rooted at the current working directory by default

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/05-filesystem-backends.adoc
git commit -m "content: add Module 3 — Filesystem Tools & Backends"
```

---

## Task 9: Module 4 — Custom Tools (`06-custom-tools.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/06-custom-tools.adoc`

- [ ] **Step 1: Write `06-custom-tools.adoc`**

Content requirements:
- Title: "Custom Tools"
- Brief intro: the built-in tools cover filesystem operations, but real agents need domain-specific capabilities

- **Exercise 1: Simple tool** — a basic `@tool` function:

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent

@tool
def word_count(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[word_count],
)

result = agent.invoke({"messages": [("user",
    "How many words are in this sentence: "
    "'The quick brown fox jumps over the lazy dog'"
)]})

print(result["messages"][-1].content)
```

Explain: custom tools are passed via `tools=[...]` and added alongside (not replacing) the built-in tools. The `@tool` decorator comes from `langchain_core`.

- **Exercise 2: Tool with structured input** — Pydantic V2 input schema:

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from deepagents import create_deep_agent

class CodeAnalysisInput(BaseModel):
    code: str = Field(description="The Python code to analyze")
    check_types: bool = Field(default=True, description="Whether to check for type hints")
    check_docstrings: bool = Field(default=True, description="Whether to check for docstrings")

@tool(args_schema=CodeAnalysisInput)
def analyze_code(code: str, check_types: bool = True, check_docstrings: bool = True) -> str:
    """Analyze Python code for quality issues like missing type hints and docstrings."""
    issues = []
    if check_types and "->" not in code and ":" not in code:
        issues.append("No type hints found")
    if check_docstrings and '"""' not in code and "'''" not in code:
        issues.append("No docstrings found")
    if not issues:
        return "Code looks good!"
    return "Issues found: " + ", ".join(issues)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[analyze_code],
)
```

Discuss: Pydantic V2 models give the LLM a rich schema with field descriptions, making tool selection and argument generation more reliable.

- **Exercise 3: Tool design patterns** — discussion exercise (not code). Cover:
  - Tool descriptions are the primary routing signal — the agent reads them to decide which tool to call
  - Keep descriptions specific and action-oriented ("Fetch the current weather for a city" not "Weather tool")
  - When to use a tool vs. system prompt instruction: tools for actions with side effects or external data; system prompt for behavioral guidance
  - One tool per concern — don't make swiss-army-knife tools

- **Exercise 4: Multiple tools** — add several tools and observe routing:

```python
@tool
def get_timestamp() -> str:
    """Get the current date and time in ISO format."""
    from datetime import datetime
    return datetime.now().isoformat()

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely. Only supports basic arithmetic."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: only basic arithmetic is supported"
    return str(eval(expression))

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[word_count, analyze_code, get_timestamp, calculate],
)
```

Have the student ask questions that should route to different tools and observe the agent's choices.

- **Exercise 5: Interrupt on tool call** — human-in-the-loop:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[word_count, calculate],
    interrupt_on={"calculate": True},
)
```

Explain: when `interrupt_on` is configured, the agent pauses before executing the specified tool and waits for approval. This is critical for tools with side effects (database writes, API calls, file deletions). Show how to handle the interrupt in the invoke loop — the agent returns with a pending tool call that you can approve or reject before continuing.

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/06-custom-tools.adoc
git commit -m "content: add Module 4 — Custom Tools"
```

---

## Task 10: Module 5 — Subagent Fundamentals (`07-subagent-fundamentals.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/07-subagent-fundamentals.adoc`

- [ ] **Step 1: Write `07-subagent-fundamentals.adoc`**

Content requirements:
- Title: "Subagent Fundamentals"
- Intro: this is the third pillar — sub-agents solve the context bloat problem that makes long-running agents degrade

- **Exercise 1: The context bloat problem** — motivational exercise. Explain the "dumb zone": as a conversation grows, the model's effective reasoning degrades because it has too much context to attend to. Subagents solve this by getting a fresh, isolated context window for each delegated task. Use a diagram:

```
[mermaid]
....
graph LR
    A[Main Agent<br/>Full Context] -->|task| B[Subagent<br/>Fresh Context]
    B -->|result| A
    A -->|task| C[Subagent<br/>Fresh Context]
    C -->|result| A
....
```

- **Exercise 2: Your first subagent** — define and use a subagent:

```python
from deepagents import create_deep_agent

researcher = {
    "name": "researcher",
    "description": "Use this subagent to research topics and gather information. It focuses on finding facts and summarizing them clearly.",
    "system_prompt": """You are a research assistant. When given a topic:
1. Break it down into key aspects
2. Provide factual, well-organized information
3. Cite your reasoning
4. Keep responses concise but thorough""",
}

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[researcher],
)

result = agent.invoke({"messages": [("user",
    "Research the key differences between REST and GraphQL APIs. "
    "Delegate this to your research subagent."
)]})

print(result["messages"][-1].content)
```

Explain the `SubAgent` TypedDict structure: `name` (unique identifier), `description` (routing signal — the main agent reads this to decide when to delegate), `system_prompt` (the subagent's instructions).

- **Exercise 3: The `task` tool** — observe delegation:

```python
for msg in result["messages"]:
    if hasattr(msg, 'tool_calls'):
        for tc in msg.tool_calls:
            if tc['name'] == 'task':
                print(f"Delegated to: {tc['args'].get('subagent_type')}")
                print(f"Task description: {tc['args'].get('description')[:100]}...")
```

Explain that the main agent uses the `task` tool with `subagent_type` and `description` arguments. The subagent runs in its own context, does the work, and returns the result.

- **Exercise 4: Subagent descriptions as routing** — experiment with description wording. Create two subagents with overlapping capabilities but different descriptions, give the agent ambiguous tasks, observe which subagent it chooses. Change the descriptions and re-run to see how routing changes. Key lesson: descriptions are the primary routing mechanism.

- **Exercise 5: Model routing** — assign different models:

```python
researcher = {
    "name": "researcher",
    "description": "Research topics and gather factual information.",
    "system_prompt": "You are a research assistant...",
    "model": "anthropic:claude-haiku-4-5-20251001",
}

analyst = {
    "name": "analyst",
    "description": "Perform deep analysis requiring careful reasoning.",
    "system_prompt": "You are an analytical expert...",
    "model": "anthropic:claude-sonnet-4-6",
}

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[researcher, analyst],
)
```

Explain: use cheaper/faster models (Haiku) for routine tasks like research, and more capable models (Sonnet/Opus) for complex reasoning. This optimizes cost and latency without sacrificing quality where it matters.

- **Exercise 6: The default `general-purpose` subagent** — explain that if you don't define a subagent named `general-purpose`, one is automatically added with all the same tools as the main agent. It's useful purely for context isolation — when you want a subtask handled in a fresh context without defining a specialist. Show it in action by asking the agent to delegate a task without specifying a subagent type.

- **CLI callout**: the CLI's `task` tool works identically — when you use the CLI, it can delegate to subagents just like the programmatic version

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/07-subagent-fundamentals.adoc
git commit -m "content: add Module 5 — Subagent Fundamentals"
```

---

## Task 11: Module 6 — YAML Subagents & the Loader Pattern (`08-yaml-subagents.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/08-yaml-subagents.adoc`

- [ ] **Step 1: Write `08-yaml-subagents.adoc`**

Content requirements:
- Title: "YAML Subagents & the Loader Pattern"
- Intro: in Module 5 you defined subagents in Python dicts. That works, but as your agent team grows, mixing configuration with code becomes hard to maintain. The Deep Agents content-builder-agent example demonstrates a pattern: define subagents in YAML.

- **Exercise 1: The content-builder-agent pattern** — walk through the canonical example. Show the full `subagents.yaml` from the content-builder-agent example:

```yaml
researcher:
  description: >
    ALWAYS use this first to research any topic before writing content.
    Searches the web for current information, statistics, and sources.
  model: anthropic:claude-haiku-4-5-20251001
  system_prompt: |
    You are a research assistant. You have access to web_search
    and write_file tools.

    ## Your Tools
    - web_search(query, max_results=5, topic="general") - Search the web
    - write_file(file_path, content) - Save your findings

    ## Your Process
    1. Use web_search to find information on the topic
    2. Make 2-3 targeted searches with specific queries
    3. Synthesize findings into a clear summary
    4. Save your research to a file for the main agent
  tools:
    - web_search
```

Explain each field and why the description is so directive ("ALWAYS use this first...") — it's the routing signal.

- **Exercise 2: Build a `load_subagents()` helper** — the core pattern:

```python
import yaml
from pathlib import Path
from langchain_core.tools import tool

# Define available tools that can be referenced by name in YAML
@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for information on a topic."""
    return f"[Simulated search results for: {query}]"

def load_subagents(config_path: Path) -> list:
    """Load subagent definitions from a YAML file.

    Maps tool name strings in YAML to actual tool objects.
    This is a custom utility — deepagents doesn't natively
    load subagents from files.
    """
    available_tools = {
        "web_search": web_search,
    }

    with open(config_path) as f:
        config = yaml.safe_load(f)

    subagents = []
    for name, spec in config.items():
        subagent = {
            "name": name,
            "description": spec["description"],
            "system_prompt": spec["system_prompt"],
        }
        if "model" in spec:
            subagent["model"] = spec["model"]
        if "tools" in spec:
            subagent["tools"] = [available_tools[t] for t in spec["tools"]]
        subagents.append(subagent)

    return subagents
```

Have students create this file, then create a `subagents.yaml` with a `researcher` subagent, load it, and pass to `create_deep_agent()`.

- **Exercise 3: Multi-subagent YAML** — extend the YAML with 3 subagents:

```yaml
researcher:
  description: >
    Use to research topics before writing. Gathers facts and sources.
  model: anthropic:claude-haiku-4-5-20251001
  system_prompt: |
    You are a research assistant. Gather information and save findings.
  tools:
    - web_search

writer:
  description: >
    Use after research is complete to write polished content.
    Reads research files and produces well-structured output.
  model: anthropic:claude-sonnet-4-6
  system_prompt: |
    You are a professional writer. Read the research files provided
    and produce clear, well-structured content. Use markdown formatting.

reviewer:
  description: >
    Use after content is written to review for quality and accuracy.
    Reads the written content and provides specific feedback.
  model: anthropic:claude-sonnet-4-6
  system_prompt: |
    You are a content reviewer. Read the content and provide specific,
    actionable feedback on clarity, accuracy, and completeness.
```

Run the agent with a content creation task and observe how it orchestrates across the three subagents.

- **Exercise 4: Iterating on subagents via config** — demonstrate the power of config-driven changes. Have students:
  1. Change the researcher's model from Haiku to Sonnet and re-run — observe quality difference
  2. Change the writer's description to be more specific about tone — observe behavior change
  3. Add a constraint to the reviewer's system prompt — observe stricter reviews

  All changes are YAML-only, no Python code changes. This is the key benefit.

- **Exercise 5: Structuring larger projects** — discuss patterns:
  - Single YAML file works for up to ~5-7 subagents
  - For larger teams, consider a directory of YAML files (one per subagent or per team)
  - Add config validation with Pydantic V2:

```python
from pydantic import BaseModel, Field, RootModel

class SubAgentConfig(BaseModel):
    description: str = Field(min_length=10)
    system_prompt: str = Field(min_length=20)
    model: str | None = None
    tools: list[str] = Field(default_factory=list)

class SubAgentsConfig(RootModel[dict[str, SubAgentConfig]]):
    pass
```

  Show how validation catches misconfigurations early.

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/08-yaml-subagents.adoc
git commit -m "content: add Module 6 — YAML Subagents & the Loader Pattern"
```

---

## Task 12: Module 7 — Skills & Progressive Disclosure (`09-skills.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/09-skills.adoc`

- [ ] **Step 1: Write `09-skills.adoc`**

Content requirements:
- Title: "Skills & Progressive Disclosure"
- Intro: skills solve a token efficiency problem — instead of loading every capability into the system prompt upfront, skills are discovered on demand

- **Exercise 1: What progressive disclosure solves** — contrast two approaches:
  1. Stuffing everything into the system prompt (expensive, dilutes attention)
  2. Progressive disclosure: only load skill name + description into a catalog, read full instructions when needed

  Use a simple comparison showing token counts.

- **Exercise 2: Your first SKILL.md** — create a skill:

```
[source,role="execute"]
----
mkdir -p skills/code-review
cat > skills/code-review/SKILL.md << 'EOF'
---
name: code-review
description: Reviews Python code for bugs, security issues, and style problems. Use when asked to review, audit, or check code quality.
---

# Code Review Skill

## Process
1. Read the code file(s) to review
2. Check for these categories of issues:
   - **Bugs**: logic errors, off-by-one, null/None handling
   - **Security**: injection, hardcoded secrets, unsafe eval/exec
   - **Style**: naming conventions, function length, complexity
   - **Performance**: unnecessary loops, missing caching opportunities
3. Write findings to a review file with severity ratings (critical/warning/info)

## Output Format
Create a file called `review-{filename}.md` with:
- Summary (1-2 sentences)
- Issues table (severity, line, description, suggestion)
- Overall assessment (approve / request changes)
EOF
----
```

Then register and use:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    skills=["./skills/"],
)

result = agent.invoke({"messages": [("user",
    "Review the file workspace/myproject/main.py for code quality issues."
)]})
```

Explain the SKILL.md format: YAML frontmatter with `name` and `description` (required), then markdown body with the full instructions. The name must match the directory name. The description goes into the skill catalog that's always visible; the body is only loaded when the agent decides the skill is relevant.

- **Exercise 3: Skill invocation** — observe progressive disclosure in action. Have the student ask the agent something that should trigger the skill, then something unrelated. In the first case, the agent reads the full SKILL.md; in the second, it doesn't. Show how to observe this in the tool call trace.

- **Exercise 4: Skills on subagents** — equip a subagent with its own skills:

```python
reviewer_subagent = {
    "name": "code-reviewer",
    "description": "Reviews code for quality, security, and style issues.",
    "system_prompt": "You are a code review specialist.",
    "skills": ["./skills/"],
}

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[reviewer_subagent],
)
```

Explain that skills on subagents are isolated — the main agent doesn't see the subagent's skills, and vice versa. This keeps each agent focused.

- **Exercise 5: Skill layering** — create a second skill source:

```
[source,role="execute"]
----
mkdir -p skills-override/code-review
cat > skills-override/code-review/SKILL.md << 'EOF'
---
name: code-review
description: Reviews Python code with emphasis on security. Use when asked to review, audit, or check code.
---

# Security-Focused Code Review

## Process
1. Read the code
2. Focus primarily on security vulnerabilities (OWASP Top 10)
3. Flag any hardcoded credentials, injection vectors, or unsafe operations
4. Write findings to a security review file
EOF
----
```

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    skills=["./skills/", "./skills-override/"],
)
```

The `skills-override` version replaces the base `code-review` skill because it comes later in the list (last-one-wins). This is useful for customizing skills per project or environment.

- **Exercise 6: Skills that delegate** — create a skill whose instructions tell the agent to use a subagent:

```
[source,role="execute"]
----
mkdir -p skills/research-and-write
cat > skills/research-and-write/SKILL.md << 'EOF'
---
name: research-and-write
description: Researches a topic and produces a written summary. Use when asked to write about a topic that requires current information.
---

# Research and Write Skill

## Process
1. Use the `task` tool with `subagent_type: "researcher"` to gather information
2. Review the research results
3. Use the `task` tool with `subagent_type: "writer"` to produce polished content
4. Review the final output and make any necessary edits
EOF
----
```

This combines the skills and subagents patterns — the skill provides the procedure, the subagents provide the execution.

- **CLI callout**: `deepagents skills list` to see installed skills, copying skills to `~/.deepagents/agent/skills/` for global availability

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/09-skills.adoc
git commit -m "content: add Module 7 — Skills & Progressive Disclosure"
```

---

## Task 13: Module 8 — Memory & AGENTS.md (`10-memory.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/10-memory.adoc`

- [ ] **Step 1: Write `10-memory.adoc`**

Content requirements:
- Title: "Memory & AGENTS.md"
- Intro: skills give agents on-demand capabilities, but memory gives them persistent context that shapes every conversation

- **Exercise 1: The AGENTS.md spec** — create an AGENTS.md file:

```
[source,role="execute"]
----
cat > AGENTS.md << 'EOF'
# Project Context

This is a Python REST API project using FastAPI and SQLAlchemy.

## Coding Standards
- Use type hints on all functions
- Write docstrings for public functions
- Use async/await for database operations
- Follow PEP 8 naming conventions

## Architecture
- `src/` contains application code
- `tests/` contains pytest test files
- `alembic/` contains database migrations

## Known Issues
- The user authentication module needs rate limiting (TODO)
- Database connection pooling is not yet configured
EOF
----
```

Explain the AGENTS.md spec (https://agents.md/) — it's a convention for giving agents persistent project context.

- **Exercise 2: MemoryMiddleware** — configure and observe:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    memory=["./AGENTS.md"],
)

result = agent.invoke({"messages": [("user",
    "What coding standards should I follow in this project?"
)]})

print(result["messages"][-1].content)
```

The agent should reference the standards from AGENTS.md. Explain that `MemoryMiddleware` loads the file contents and injects them into the system prompt wrapped in `<agent_memory>` tags. Unlike skills (loaded on demand), memory is always present.

- **Exercise 3: Self-updating memory** — observe the agent modifying its own AGENTS.md:

```python
result = agent.invoke({"messages": [("user",
    "I just decided we should also use Pydantic V2 for all data validation. "
    "Update the project's AGENTS.md to include this coding standard."
)]})
```

Check that AGENTS.md was actually modified: `cat AGENTS.md`. The agent uses `edit_file` to update its own memory file. This is how agents learn and persist knowledge across conversations.

- **Exercise 4: Memory layering** — configure multiple memory sources:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    memory=["./AGENTS.md", "~/.deepagents/AGENTS.md"],
)
```

Create a user-level AGENTS.md with personal preferences:

```
[source,role="execute"]
----
mkdir -p ~/.deepagents
cat > ~/.deepagents/AGENTS.md << 'EOF'
# User Preferences
- I prefer concise responses
- Show code examples rather than lengthy explanations
- Always use uv, never pip
EOF
----
```

Both files are loaded — project context + user preferences.

- **Exercise 5: Memory + skills + subagents** — the full stack:

```python
from deepagents import create_deep_agent

subagents = [
    {
        "name": "researcher",
        "description": "Research topics and gather information.",
        "system_prompt": "You are a research assistant.",
        "model": "anthropic:claude-haiku-4-5-20251001",
    }
]

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    memory=["./AGENTS.md"],
    skills=["./skills/"],
    subagents=subagents,
)
```

Give it a task that exercises all three: "Research best practices for FastAPI rate limiting, then review our current auth module code." The agent should use memory (knows the project context), delegate research (subagent), and apply the code-review skill.

Explain the full middleware stack order: TodoList -> Skills -> Filesystem -> SubAgent -> Summarization -> PatchToolCalls -> AnthropicPromptCaching -> Memory -> HumanInTheLoop.

- **Exercise 6: Introducing a second model provider** — multi-provider support:

```python
subagents = [
    {
        "name": "researcher",
        "description": "Research topics using web search.",
        "system_prompt": "You are a research assistant.",
        "model": "openai:gpt-4o",  # Uses OpenAI for this subagent
    },
    {
        "name": "analyst",
        "description": "Deep analysis requiring careful reasoning.",
        "system_prompt": "You are an analytical expert.",
        "model": "anthropic:claude-sonnet-4-6",  # Anthropic for this one
    },
]

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=subagents,
)
```

Requires `export OPENAI_API_KEY=...`. Mark this exercise as optional. Explain the `"provider:model"` format works with any LiteLLM-supported provider.

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/10-memory.adoc
git commit -m "content: add Module 8 — Memory & AGENTS.md"
```

---

## Task 14: Module 9 — The Deep Agents CLI (`11-cli.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/11-cli.adoc`

- [ ] **Step 1: Write `11-cli.adoc`**

Content requirements:
- Title: "The Deep Agents CLI"
- Intro: you've seen CLI callouts throughout the workshop. Now let's explore the CLI as a full-featured agent environment, not just a quick demo tool.

- **Exercise 1: TUI deep dive** — guided exploration of the Textual-based interface:

```
[source,role="execute"]
----
deepagents
----
```

Walk through:
  - The input area at the bottom
  - Streaming output display
  - Tool call visualization (how tool calls and results are rendered)
  - Conversation history (scroll up)
  - Keyboard shortcuts
  - Exit with Ctrl+C

Have students give the CLI a multi-step task and observe the TUI rendering of planning (todos), tool calls (file operations), and subagent delegation.

- **Exercise 2: Configuration** — explore `~/.deepagents/`:

```
[source,role="execute"]
----
ls -la ~/.deepagents/ 2>/dev/null || echo "No config directory yet"
----
```

Explain the directory structure:
  - `~/.deepagents/agent/skills/` — global skills directory
  - `~/.deepagents/AGENTS.md` — user-level memory
  - Configuration for default model, API keys, etc.

Show how to set the default model so you don't need to specify it every time.

- **Exercise 3: Custom skills in CLI** — install the code-review skill globally:

```
[source,role="execute"]
----
mkdir -p ~/.deepagents/agent/skills/
cp -r skills/code-review ~/.deepagents/agent/skills/
deepagents skills list
----
```

The skill should appear in the list. Launch the CLI and ask it to review a file — it should use the installed skill.

- **Exercise 4: Headless mode** — non-interactive execution for scripting:

```
[source,role="execute"]
----
deepagents --headless "List all Python files in the current directory and count the total lines of code" 2>/dev/null
----
```

Explain headless mode:
  - No TUI — runs and exits
  - Useful for CI/CD pipelines, shell scripts, automation
  - Output can be captured and parsed
  - Show piping output: `deepagents --headless "..." > output.txt`

- **Exercise 5: CLI + project context** — demonstrate working-directory awareness:

```
[source,role="execute"]
----
cd deep-agents-workshop
ls AGENTS.md skills/
----
```

Launch the CLI from this directory — it automatically discovers:
  - `./AGENTS.md` for project memory
  - `./skills/` for project skills

This mirrors the programmatic `memory=["./AGENTS.md"]` and `skills=["./skills/"]` — same discovery, different interface.

- **Exercise 6: Practical workflow** — use the CLI as a development companion. Walk through a realistic scenario:
  1. Start the CLI in a project directory
  2. Ask it to scaffold a new feature module
  3. Ask it to write tests for the module
  4. Ask it to review the code it just wrote
  5. Ask it to update AGENTS.md with what it learned

This ties together skills (code-review), memory (AGENTS.md), and the agent's built-in capabilities in the CLI's interactive TUI.

- **Module summary**

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/11-cli.adoc
git commit -m "content: add Module 9 — The Deep Agents CLI"
```

---

## Task 15: Module 10 — Capstone: AIOps Team (`12-capstone-aiops.adoc`)

**Files:**
- Create: `content/modules/ROOT/pages/12-capstone-aiops.adoc`

- [ ] **Step 1: Write `12-capstone-aiops.adoc`**

Content requirements:
- Title: "Capstone: AIOps Team"
- Intro: everything you've learned comes together. You'll build an AIOps multi-agent system with an `ops_manager` orchestrator and a team of specialized SRE subagents. This is a realistic pattern for production agent systems.

- Start with an architecture diagram:

```
[mermaid]
....
graph TD
    I[Incident Alert] --> OM[ops_manager<br/>Orchestrator]
    OM -->|task| LA[sre_log_analyst<br/>Log Parsing & Patterns]
    OM -->|task| DG[sre_diagnostician<br/>Root Cause Analysis]
    OM -->|task| RM[sre_remediator<br/>Fixes & Rollbacks]
    LA -->|findings| OM
    DG -->|diagnosis| OM
    RM -->|remediation plan| OM
    OM --> R[Incident Report]

    LA -.->|skill| S1[log-analysis]
    DG -.->|skill| S2[diagnostics]
    RM -.->|skill| S3[remediation]
....
```

- **Exercise 1: Design the team** — create `aiops/subagents.yaml`:

```yaml
sre_log_analyst:
  description: >
    Use to analyze application logs for error patterns, anomalies,
    and correlations. Always delegate log analysis tasks here first.
  model: anthropic:claude-haiku-4-5-20251001
  system_prompt: |
    You are an SRE log analysis specialist. When given logs:
    1. Identify error patterns and their frequency
    2. Look for correlations between different log sources
    3. Flag anomalies that deviate from normal patterns
    4. Summarize findings with timestamps and severity ratings
    5. Save your analysis to a file for the ops_manager

sre_diagnostician:
  description: >
    Use after log analysis to correlate findings with system state
    and determine root cause. Reads log analysis results and
    applies diagnostic procedures.
  model: anthropic:claude-sonnet-4-6
  system_prompt: |
    You are an SRE diagnostics expert. You receive log analysis
    results and system metrics. Your job:
    1. Read the log analysis findings
    2. Correlate with known failure modes from your diagnostic skills
    3. Form hypotheses about root cause
    4. Rank hypotheses by likelihood
    5. Recommend specific remediation actions

sre_remediator:
  description: >
    Use after diagnosis to propose and execute remediation actions.
    CRITICAL: All execute actions require human approval.
  model: anthropic:claude-sonnet-4-6
  system_prompt: |
    You are an SRE remediation specialist. You receive a diagnosis
    and must propose fixes. For each proposed fix:
    1. Describe what the fix does
    2. Assess risk (low/medium/high)
    3. Describe the rollback procedure
    4. Execute only after explicit approval
  tools:
    - execute_remediation
```

- **Exercise 2: Build the skills** — create three SKILL.md files:

`aiops/skills/log-analysis/SKILL.md`:
```markdown
---
name: log-analysis
description: Procedures for analyzing application and system logs to identify error patterns, anomalies, and correlations.
---

# Log Analysis Procedures

## Error Pattern Detection
1. Parse log entries by severity (ERROR, WARN, INFO)
2. Group errors by error code or exception type
3. Calculate frequency and identify spikes
4. Look for cascading failures (error A followed by error B)

## Anomaly Detection
1. Establish baseline from recent history
2. Flag entries that deviate >2 standard deviations
3. Check for unusual request patterns
4. Identify new error types not seen before

## Correlation Analysis
1. Align timestamps across log sources
2. Look for patterns: request → processing → error
3. Check for resource exhaustion preceding errors
4. Map error clusters to deployment events
```

`aiops/skills/diagnostics/SKILL.md`:
```markdown
---
name: diagnostics
description: Root cause analysis procedures for common infrastructure and application failures.
---

# Diagnostic Procedures

## Common Failure Modes
- **OOM Kill**: Check for memory spikes, container limits, memory leaks
- **Connection Pool Exhaustion**: Check active connections, wait times, pool size
- **Disk Full**: Check disk usage, log rotation, temp file cleanup
- **DNS Resolution Failure**: Check resolver config, upstream DNS, cache TTL
- **Certificate Expiry**: Check cert dates, renewal automation, chain validity

## Diagnostic Decision Tree
1. Is the service responding? → Check health endpoints
2. Are errors intermittent or constant? → Intermittent suggests resource contention
3. Did anything change recently? → Check deployment history
4. Is it affecting all users or a subset? → Subset suggests routing/partition issue
```

`aiops/skills/remediation/SKILL.md`:
```markdown
---
name: remediation
description: Runbooks for common remediation actions including rollbacks, restarts, and scaling operations.
---

# Remediation Runbooks

## Service Restart
- Risk: LOW
- Procedure: Graceful restart via orchestrator
- Rollback: N/A (restart is non-destructive)

## Rollback Deployment
- Risk: MEDIUM
- Procedure: Revert to previous known-good version
- Rollback: Re-deploy the current version

## Scale Up
- Risk: LOW
- Procedure: Increase replica count or resource limits
- Rollback: Scale back down after incident resolves

## Connection Pool Reset
- Risk: MEDIUM
- Procedure: Drain and reinitialize connection pool
- Rollback: Restart service if pool fails to reinitialize
```

Each skill should be created with `mkdir -p` and `cat > ... << 'EOF'` execute blocks.

- **Exercise 3: Write the loader** — extend `load_subagents()` with custom tools:

```python
import yaml
from pathlib import Path
from langchain_core.tools import tool
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

@tool
def execute_remediation(action: str, target: str) -> str:
    """Execute a remediation action on a target system.
    REQUIRES HUMAN APPROVAL before execution.

    Args:
        action: The remediation action (restart, rollback, scale_up, reset_pool)
        target: The target service or component
    """
    # In production, this would call your infrastructure APIs
    return f"[SIMULATED] Executed '{action}' on '{target}' — success"

@tool
def fetch_logs(service: str, minutes: int = 30) -> str:
    """Fetch recent logs from a service.

    Args:
        service: The service name to fetch logs from
        minutes: How many minutes of logs to retrieve
    """
    # Simulated log output for the workshop
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

def load_subagents(config_path: Path) -> list:
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
            "system_prompt": spec["system_prompt"],
        }
        if "model" in spec:
            subagent["model"] = spec["model"]
        if "tools" in spec:
            subagent["tools"] = [available_tools[t] for t in spec["tools"]]
        if "skills" in spec:
            subagent["skills"] = spec["skills"]
        subagents.append(subagent)

    return subagents
```

Note the addition of `skills` support in the loader — this lets subagents.yaml reference skill directories per subagent. Update `subagents.yaml` to add tool and skill references:

```yaml
sre_log_analyst:
  # ... (same as before, add:)
  tools:
    - fetch_logs
    - query_metrics
  skills:
    - ./aiops/skills/log-analysis/

sre_diagnostician:
  # ... (same as before, add:)
  tools:
    - query_metrics
  skills:
    - ./aiops/skills/diagnostics/

sre_remediator:
  # ... (same as before, add:)
  tools:
    - execute_remediation
  skills:
    - ./aiops/skills/remediation/
```

- **Exercise 4: Wire up memory** — create `aiops/AGENTS.md`:

```
[source,role="execute"]
----
cat > aiops/AGENTS.md << 'EOF'
# AIOps Operations Context

## Environment
- Production cluster: 3 app servers, 1 database (PostgreSQL), 1 Redis cache
- Container orchestrator: Kubernetes
- Monitoring: Prometheus + Grafana

## Known Failure Modes
- Connection pool exhaustion under load spikes (>500 req/s)
- OOM kills when batch processing coincides with peak traffic
- DNS resolution failures during cloud provider maintenance windows

## Escalation Procedures
- Severity 1 (service down): Page on-call, 15-minute response SLA
- Severity 2 (degraded): Notify team channel, 1-hour response SLA
- Severity 3 (warning): Log ticket, next business day

## Recent Incidents
- 2026-03-15: Connection pool exhaustion caused 20-minute outage, fixed by increasing pool size to 200
- 2026-03-22: OOM kill during batch job, fixed by adding memory limits to batch containers
EOF
----
```

- **Exercise 5: Human-in-the-loop** — wire up `interrupt_on` for the remediator:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="""You are an AIOps operations manager. When an incident is reported:
1. Delegate log analysis to sre_log_analyst
2. Send findings to sre_diagnostician for root cause analysis
3. If remediation is needed, delegate to sre_remediator
4. Compile a final incident report""",
    memory=["./aiops/AGENTS.md"],
    skills=["./aiops/skills/"],
    subagents=load_subagents(Path("aiops/subagents.yaml")),
    tools=[fetch_logs, query_metrics, execute_remediation],
    interrupt_on={"execute_remediation": True},
    backend=FilesystemBackend(root_dir="./aiops"),
)
```

Walk through the approval flow when `execute_remediation` is called.

- **Exercise 6: End-to-end scenario** — feed the system an incident:

```python
result = agent.invoke({"messages": [("user",
    "INCIDENT ALERT: Service 'payment-api' is returning 503 errors. "
    "Error rate spiked from <1% to 23% in the last 10 minutes. "
    "Multiple customers reporting failed transactions. "
    "Investigate and propose remediation."
)]})
```

Walk through the expected flow:
1. `ops_manager` receives the alert
2. Delegates to `sre_log_analyst` (fetches logs, uses log-analysis skill)
3. Sends findings to `sre_diagnostician` (correlates with known failure modes, uses diagnostics skill)
4. Delegates to `sre_remediator` (proposes fix, human approval gate on execute)
5. Compiles incident report

- **Exercise 7: Iterate via config** — demonstrate config-driven changes:
  1. Add a new subagent (`sre_communicator` for drafting stakeholder updates) — YAML only
  2. Swap the log analyst to a different model — YAML only
  3. Add a new skill (escalation procedures) — create SKILL.md only
  4. No Python code changes needed for any of this

- **Module summary**: what you built (production-style multi-agent AIOps system), all concepts exercised (subagents, YAML config, skills, memory, tools, human-in-the-loop, backends), key pattern (config-driven agent teams)

- [ ] **Step 2: Verify build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/12-capstone-aiops.adoc
git commit -m "content: add Module 10 — Capstone: AIOps Team"
```

---

## Task 16: Conclusion Page — `99-conclusion.adoc`

**Files:**
- Create: `content/modules/ROOT/pages/99-conclusion.adoc`

- [ ] **Step 1: Write `99-conclusion.adoc`**

Content requirements:
- Title: "Conclusion & Next Steps"
- **"What you built"** section: recap each module's output in 1 line each
- **"Key patterns to take away"** section:
  - The four pillars (system prompt, planning, subagents, filesystem)
  - YAML-driven subagent configuration for maintainable agent teams
  - Skills + subagents composition for scalable capability management
  - Memory (AGENTS.md) for persistent context
  - Config-driven iteration (change behavior without code changes)
- **"Next steps"** section:
  - LangGraph Studio integration for visual debugging
  - Deployment patterns (LangGraph Cloud, self-hosted)
  - `AsyncSubAgent` for remote agent deployment
  - `CompositeBackend` for production storage patterns
  - Community resources
- **"Resources"** section:
  - Deep Agents repo: https://github.com/langchain-ai/deepagents
  - Agent Skills spec: https://agentskills.io
  - AGENTS.md spec: https://agents.md
  - Blog posts (all four)
  - LangGraph documentation

- [ ] **Step 2: Verify full build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1 | tail -20
```

Expected: `Site generation complete!` with no errors. All pages should resolve, no broken xrefs.

- [ ] **Step 3: Commit**

```bash
git add content/modules/ROOT/pages/99-conclusion.adoc
git commit -m "content: add conclusion and next steps page"
```

---

## Task 17: Final verification and cleanup

- [ ] **Step 1: Full Antora build**

```bash
podman run --rm --entrypoint antora -v "$PWD:/antora:Z" ghcr.io/juliaaano/antora-viewer site.yml 2>&1
```

Verify: `Site generation complete!` with no errors. Warnings about missing images are acceptable.

- [ ] **Step 2: Check all nav links resolve**

```bash
# Count pages in nav vs pages directory
grep -c "xref:" content/modules/ROOT/nav.adoc
ls content/modules/ROOT/pages/*.adoc | wc -l
```

The xref count should match the number of `.adoc` files.

- [ ] **Step 3: Verify no template files remain**

```bash
# These Showroom template files should not exist
for f in agnosticv-config.adoc architecture.adoc attribute-example.adoc content-repo.adoc contributing.adoc deployer.adoc images.adoc nookbag.adoc ocp-integration.adoc ocp4-role-reference.adoc quick-start.adoc ui-config.adoc user-data.adoc vm-role-reference.adoc; do
    [ -f "content/modules/ROOT/pages/$f" ] && echo "LEFTOVER: $f"
done
```

Expected: no output (all template files were deleted in Task 1).

- [ ] **Step 4: Commit any cleanup**

Only if changes were needed. Otherwise skip.
