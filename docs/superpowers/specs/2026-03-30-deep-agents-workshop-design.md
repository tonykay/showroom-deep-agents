# Deep Agents Workshop Design Spec

**Date:** 2026-03-30
**Title:** Deep Agents: From First Agent to Production Multi-Agent Systems
**Format:** Antora/Showroom multi-module workshop (10 learning modules + supporting pages)

---

## 1. Workshop Identity

**Tagline:** A hands-on workshop building real AI agent systems with LangChain's Deep Agents framework.

**Audience:** Python developers familiar with LLM APIs (OpenAI/Anthropic SDK experience), new to the Deep Agents framework. LangChain/LangGraph concepts referenced lightly where they surface naturally -- no prerequisite knowledge required.

**Environment:**
- Local laptop (macOS/Linux)
- Python 3.13+
- `uv` as package manager (not pip)
- Anthropic API key required from the start
- OpenAI API key introduced in Module 10 for multi-provider demonstration
- Local Showroom experience via `./localroom.sh start` (split-pane: docs + terminal + code editor)

**Approach:**
- **Top-down:** Start with a working `create_deep_agent()` call in Module 03, then progressively peel back layers
- **Self-contained modules with capstone:** Each module has its own focused exercises; the final module synthesizes everything into a full AIOps multi-agent system
- **CLI woven early, deep dive late:** Light CLI callouts from Module 03 onward; dedicated CLI module (11) for TUI, headless mode, and CLI-specific features

---

## 2. File Structure

```
content/
  antora.yml
  modules/ROOT/
    nav.adoc
    pages/
      index.adoc                    # Welcome, how to use the workshop
      01-overview.adoc              # Workshop overview, audience, learning path
      02-details.adoc               # Setup: uv, Python 3.13, API keys, localroom
      03-first-agent.adoc           # Module 1: Your First Deep Agent
      04-system-prompts-planning.adoc  # Module 2: System Prompts & Planning
      05-filesystem-backends.adoc   # Module 3: Filesystem Tools & Backends
      06-custom-tools.adoc          # Module 4: Custom Tools
      07-subagent-fundamentals.adoc # Module 5: Subagent Fundamentals
      08-yaml-subagents.adoc        # Module 6: YAML Subagents & Loader Pattern
      09-skills.adoc                # Module 7: Skills & Progressive Disclosure
      10-memory.adoc                # Module 8: Memory & AGENTS.md
      11-cli.adoc                   # Module 9: The Deep Agents CLI
      12-capstone-aiops.adoc        # Module 10: Capstone: AIOps Team
      99-conclusion.adoc            # Wrap-up, next steps, resources
    assets/images/                  # Screenshots, diagrams
    examples/                       # Downloadable code samples
    partials/                       # Reusable content fragments
```

---

## 3. Module Specifications

### index.adoc -- Welcome

- What this workshop covers
- How to navigate the modules (progressive, but modules are mostly self-contained)
- Estimated total time (~8 hours)
- Prerequisites summary

### 01-overview.adoc -- Workshop Overview

- What Deep Agents are and why they exist (beyond simple tool-calling loops)
- The four pillars at a glance (detailed exploration in modules 03-07)
- Where Deep Agents fits in the LangChain ecosystem (`deepagents` = harness, `langchain` = framework, `langgraph` = runtime)
- Learning path visualization
- Target audience and what you'll build

### 02-details.adoc -- Environment Setup

- Install Python 3.13+ (verify with `python3 --version`)
- Install `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Create project: `uv init deep-agents-workshop && cd deep-agents-workshop`
- Add dependency: `uv add deepagents`
- Set Anthropic API key: `export ANTHROPIC_API_KEY=...`
- Validate setup: run a minimal Python script that imports `deepagents` and prints version
- Install `deepagents-cli`: `curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash`
- Validate CLI: `deepagents --help`
- Start localroom: `./localroom.sh start` (optional but recommended for full Showroom experience)

---

### Module 03: Your First Deep Agent (`03-first-agent.adoc`)

**Duration:** ~30 minutes

**Goal:** Working agent in under 5 minutes, both programmatically and via CLI.

**Concepts introduced:**
- `create_deep_agent()` returns a compiled LangGraph `CompiledStateGraph`
- Message format (list of tuples or HumanMessage objects)
- The `"provider:model"` string pattern (e.g., `"anthropic:claude-sonnet-4-6"`)
- What you get out of the box: built-in tools, default system prompt, `general-purpose` subagent

**Exercises:**
1. **Hello Deep Agent** -- minimal `create_deep_agent()` call with default model, invoke with a simple message, inspect the response structure
2. **Streaming responses** -- switch to `agent.stream()`, observe token-by-token output, understand the LangGraph event stream format
3. **Exploring defaults** -- ask the agent to list its tools, observe the built-in filesystem tools and `write_todos`
4. **CLI first look** -- run the same prompt in the `deepagents` TUI, compare the interactive experience to the programmatic one

---

### Module 04: System Prompts & Planning (`04-system-prompts-planning.adoc`)

**Duration:** ~35 minutes

**Goal:** Understand how Deep Agents' system prompt and planning tool shape agent behavior.

**Concepts introduced:**
- `BASE_AGENT_PROMPT` -- the comprehensive default system prompt
- System prompt prepending (custom + base)
- `TodoListMiddleware` and the `write_todos` tool
- Planning as context engineering

**Exercises:**
1. **Custom system prompts** -- add a `system_prompt` parameter, observe how it prepends to the base prompt, experiment with persona and constraints
2. **The base prompt** -- examine what `BASE_AGENT_PROMPT` contains (tool usage instructions, behavioral guidelines), understand why it's comprehensive
3. **Planning with todos** -- give the agent a multi-step task, observe `write_todos` tool usage, inspect the todo list state
4. **Guiding planning behavior** -- use system prompt instructions to influence how the agent plans and decomposes work

**CLI callout:** `deepagents --system-prompt "..."` flag for custom prompts

---

### Module 05: Filesystem Tools & Backends (`05-filesystem-backends.adoc`)

**Duration:** ~40 minutes

**Goal:** Understand the agent's filesystem capabilities and the pluggable backend system.

**Concepts introduced:**
- Built-in file tools: `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`
- The `execute` tool for shell commands
- `BackendProtocol` -- the pluggable interface
- `FilesystemBackend` and `StateBackend`
- Preview of `CompositeBackend` (detailed in capstone)

**Exercises:**
1. **Built-in file tools** -- give the agent tasks that exercise each file tool, observe how it navigates and modifies files
2. **The `execute` tool** -- run shell commands through the agent, understand sandboxing considerations
3. **FilesystemBackend** -- configure `root_dir`, understand path scoping, observe how the agent is contained to its workspace
4. **StateBackend** -- switch to in-memory state backend, observe ephemeral file storage, understand when this is useful (testing, sandboxed environments)
5. **Brief intro to CompositeBackend** -- preview layering backends (deep dive deferred to capstone)

**CLI callout:** How the CLI's file operations use the same backend system

---

### Module 06: Custom Tools (`06-custom-tools.adoc`)

**Duration:** ~40 minutes

**Goal:** Extend your agent with custom tools.

**Concepts introduced:**
- `@tool` decorator pattern
- Pydantic V2 for tool input schemas
- Tool description quality as routing signal
- `interrupt_on` for human-in-the-loop

**Exercises:**
1. **Simple tool** -- write a `@tool` decorated function (e.g., a timestamp or word-count tool), pass via `tools=[...]`, invoke it
2. **Tool with structured input** -- use Pydantic V2 models for tool input schemas, demonstrate validation
3. **Tool design patterns** -- when to use tools vs. system prompt instructions, keeping tool descriptions clear for routing
4. **Multiple tools** -- add 2-3 tools, observe how the agent selects between them based on descriptions
5. **Interrupt on tool call** -- introduce `interrupt_on` for human-in-the-loop approval on sensitive tools

---

### Module 07: Subagent Fundamentals (`07-subagent-fundamentals.adoc`)

**Duration:** ~45 minutes

**Goal:** Understand why subagents exist and how to define them declaratively.

**Concepts introduced:**
- Context bloat and the "dumb zone"
- `SubAgent` TypedDict structure (name, description, system_prompt, tools, model)
- The `task` tool and `subagent_type` parameter
- Subagent descriptions as routing mechanism
- Model routing for cost/speed optimization
- The default `general-purpose` subagent

**Exercises:**
1. **The context bloat problem** -- demonstrate how a long conversation degrades agent performance, motivate the need for context isolation
2. **Your first subagent** -- define a `SubAgent` dict with name, description, system_prompt; pass via `subagents=[...]`
3. **The `task` tool** -- observe how the main agent delegates via `task(description=..., subagent_type=...)`, inspect subagent responses
4. **Subagent descriptions as routing** -- experiment with description wording, see how it affects when the agent chooses each subagent
5. **Model routing** -- assign a cheaper/faster model to a research subagent (`"anthropic:claude-haiku-4-5-20251001"`), observe cost/speed trade-offs
6. **The default `general-purpose` subagent** -- understand that it always exists, useful purely for context isolation even without specialization

**CLI callout:** The CLI's built-in `task` tool dispatches to subagents the same way

---

### Module 08: YAML Subagents & the Loader Pattern (`08-yaml-subagents.adoc`)

**Duration:** ~45 minutes

**Goal:** Externalize subagent configuration into YAML for maintainable multi-agent systems.

**Concepts introduced:**
- YAML-based subagent configuration (the content-builder-agent pattern)
- `load_subagents()` helper: mapping tool name strings to objects
- Configuration-driven agent behavior
- Separation of agent logic from agent configuration

**Exercises:**
1. **The content-builder-agent pattern** -- walk through the canonical example's `subagents.yaml`, understand the structure (name as key, description, model, system_prompt, tools list)
2. **Build a `load_subagents()` helper** -- write the YAML loader that maps tool name strings to actual tool objects, handle optional fields (model, tools)
3. **Multi-subagent YAML** -- define 3+ subagents in a single YAML file (e.g., `researcher`, `writer`, `reviewer`), observe orchestration
4. **Iterating on subagents via config** -- change subagent behavior by editing YAML only (swap models, adjust descriptions, modify system prompts) without touching Python code
5. **Structuring larger projects** -- patterns for organizing subagent configs as teams grow (single file vs. directory of YAML files, config validation with Pydantic V2)

---

### Module 09: Skills & Progressive Disclosure (`09-skills.adoc`)

**Duration:** ~45 minutes

**Goal:** Create and use skills that give agents on-demand capabilities without bloating context.

**Concepts introduced:**
- The Agent Skills specification (agentskills.io)
- Progressive disclosure: frontmatter loaded into catalog, full body read on demand
- SKILL.md format: YAML frontmatter + markdown instructions
- Skill layering with multiple source paths (last-one-wins)
- Skills on subagents via the `skills` key

**Exercises:**
1. **What progressive disclosure solves** -- demonstrate token cost of loading everything into the system prompt vs. loading on demand
2. **Your first SKILL.md** -- create a skill directory with frontmatter (name, description) and markdown body, register via `skills=["./skills/"]`
3. **Skill invocation** -- observe how the agent discovers available skills from the catalog, reads the full SKILL.md only when relevant
4. **Skills on subagents** -- equip a subagent with its own skills via the `skills` key in the SubAgent dict, demonstrate skill isolation per subagent
5. **Skill layering** -- configure multiple skill source paths, understand last-one-wins override semantics
6. **Skills that delegate** -- write a skill whose instructions tell the agent to use the `task` tool with a specific subagent, combining both patterns

**CLI callout:** `deepagents skills list`, installing skills into `~/.deepagents/agent/skills/`, CLI skill management

---

### Module 10: Memory & AGENTS.md (`10-memory.adoc`)

**Duration:** ~40 minutes

**Goal:** Give agents persistent, self-updating memory across conversations.

**Concepts introduced:**
- The AGENTS.md specification (agents.md)
- `MemoryMiddleware` and `<agent_memory>` tags
- Self-updating memory via `edit_file` on AGENTS.md
- Memory layering (project + user level)
- Multi-provider model support

**Exercises:**
1. **The AGENTS.md spec** -- create an AGENTS.md file with project context, coding standards, user preferences
2. **MemoryMiddleware** -- configure `memory=["./AGENTS.md"]`, observe injection into system prompt wrapped in `<agent_memory>` tags
3. **Self-updating memory** -- give the agent a task that produces learnings, observe it `edit_file` its own AGENTS.md to store what it learned
4. **Memory layering** -- configure multiple memory paths (project-level + user-level), understand load order
5. **Memory + skills + subagents** -- combine all three: agent with memory for context, skills for procedures, subagents for delegation. Full middleware stack in action.
6. **Introducing a second model provider** -- swap one subagent to `"openai:gpt-4o"` to demonstrate multi-provider support (requires OpenAI API key)

---

### Module 11: The Deep Agents CLI (`11-cli.adoc`)

**Duration:** ~40 minutes

**Goal:** Master the CLI as a standalone agent environment and CI/automation tool.

**Concepts introduced:**
- Textual-based TUI architecture
- `~/.deepagents/` directory structure and configuration
- Headless mode for scripting and CI
- CLI skill and memory discovery from working directory

**Exercises:**
1. **TUI deep dive** -- explore the Textual-based interface: input, streaming output, tool call visualization, conversation history
2. **Configuration** -- `~/.deepagents/` directory structure, default model, custom settings
3. **Custom skills in CLI** -- install skills into `~/.deepagents/agent/skills/`, verify with `deepagents skills list`, use them in conversation
4. **Headless mode** -- run `deepagents` non-interactively for scripting and CI pipelines, capture structured output
5. **CLI + project context** -- how the CLI discovers AGENTS.md and skills from the working directory, mirroring the programmatic experience
6. **Practical workflow** -- use the CLI as a development companion: code generation, refactoring, debugging with custom skills and memory

---

### Module 12: Capstone -- AIOps Team (`12-capstone-aiops.adoc`)

**Duration:** ~60 minutes

**Goal:** Build a production-style multi-agent AIOps system that synthesizes every concept from the workshop.

**Architecture:**
- `ops_manager` -- orchestrator Deep Agent that triages incoming incidents and delegates to specialist subagents
- `sre_log_analyst` -- subagent specialized in log parsing and pattern detection, equipped with log-analysis skills
- `sre_diagnostician` -- subagent that correlates symptoms to root causes, has access to runbook/diagnostic skills
- `sre_remediator` -- subagent that proposes and (with human approval) executes remediation actions

**Configuration:**
- `subagents.yaml` -- all subagent definitions with descriptions, models, tool assignments
- `skills/log-analysis/SKILL.md` -- log pattern recognition procedures
- `skills/diagnostics/SKILL.md` -- root cause analysis procedures
- `skills/remediation/SKILL.md` -- fix/rollback runbooks
- `AGENTS.md` -- operational context (known failure modes, escalation procedures, environment topology)

**Exercises:**
1. **Design the team** -- define the YAML configuration for all subagents with appropriate descriptions, models, and tool assignments
2. **Build the skills** -- create SKILL.md files for log analysis patterns, diagnostic procedures, and remediation runbooks
3. **Write the loader** -- extend `load_subagents()` with custom tools (log fetcher, metrics query, alert API)
4. **Wire up memory** -- create AGENTS.md with operational context
5. **Human-in-the-loop** -- configure `interrupt_on` for the remediator's execute actions, practice the approval flow
6. **End-to-end scenario** -- feed the system a simulated incident (error logs + metrics spike), watch `ops_manager` triage, delegate to specialists, and propose remediation
7. **Iterate via config** -- adjust subagent descriptions, swap models, add a new skill -- all without changing Python code

---

### 99-conclusion.adoc -- Wrap-up

- What you built across the workshop
- Key patterns to take away (four pillars, YAML subagents, skills + subagents composition)
- Next steps: LangGraph Studio integration, deployment patterns, community resources
- Links to Deep Agents repo, documentation, and blog posts

---

## 4. Content Conventions

- **Narrative style:** Second-person ("You"), direct and practical
- **Code blocks:** `[source,role="execute"]` for terminal commands, `[source,python]` for code to read/understand, `[source,yaml]` for configuration
- **File creation:** `cat > filename << 'EOF'` pattern inside execute blocks
- **Module structure:** Brief intro -> learning objectives -> exercises (numbered, with verification steps) -> module summary (accomplished, takeaways, next steps)
- **CLI callouts:** Brief "Try this in the CLI" sidebars in modules 03-10 where natural; not forced into every module
- **Images:** `image::name.png[align="center",link=self,window=blank,width=700]`
- **Pydantic V2:** Always use V2 for structured outputs and tool input schemas

## 5. Key Dependencies

- `deepagents` (pip/uv package)
- `deepagents-cli` (installed via shell script)
- Anthropic API key (modules 03-12)
- OpenAI API key (module 10 exercise 6 only, clearly marked optional)
- `uv` package manager
- Python 3.13+
- Podman or Docker (for `localroom.sh` / Antora builds)

## 6. Reference Material

- Deep Agents repo: https://github.com/langchain-ai/deepagents.git
  - `examples/content-builder-agent/` -- canonical subagents + skills + memory example
  - `libs/deepagents/deepagents/graph.py` -- `create_deep_agent()` source
  - `libs/deepagents/deepagents/backends/` -- backend implementations
- Blog posts:
  - https://blog.langchain.com/deep-agents/ (introductory)
  - https://blog.langchain.com/doubling-down-on-deepagents/ (v0.2, backends)
  - https://blog.langchain.com/using-skills-with-deep-agents/ (skills system)
  - https://blog.langchain.com/building-multi-agent-applications-with-deep-agents/ (subagents + skills)
- Showroom template: https://github.com/rhpds/showroom_template_nookbag.git
- Agent Skills spec: https://agentskills.io/specification
- AGENTS.md spec: https://agents.md/
