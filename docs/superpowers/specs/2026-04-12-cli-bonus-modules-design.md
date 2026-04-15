# Bonus Modules: Deep Agents CLI — Skills Development & Project-Aware Agents

**Date:** 2026-04-12
**Files:** `22-bonus-cli-skills.adoc`, `23-bonus-cli-projects.adoc`
**Status:** Approved

## Overview

Two bonus modules that take the CLI beyond the basics covered in Module 11. Part 1 treats the CLI as a skill development tool — write, test, iterate, and bridge to programmatic usage. Part 2 assembles skills, subagents, and MCP config into a project-aware agent that anyone can clone and use immediately.

Module 11 gets a closing link pointing students to these bonus modules for advanced CLI usage.

## Prerequisites

- Module 11 (CLI basics: TUI, config, headless mode, project context)
- Module 7-8 (subagent fundamentals, YAML loader pattern) — for programmatic equivalence exercises
- Module 9 (skills) — for SKILL.md format understanding

## Part 1: CLI as a Skill Development Tool

**File:** `22-bonus-cli-skills.adoc`

**Narrative arc:** The CLI is the fastest way to develop agent capabilities. Write a SKILL.md, test it live, iterate without restarting, prove it works headlessly, then use the exact same file programmatically.

### Exercise 1: Skill Anatomy

- Examine a SKILL.md file: YAML frontmatter (`name`, `description`) + markdown body (instructions)
- Explain discovery directories and precedence order
- Create a minimal `hello-skill` that formats greetings in different styles
- Use `deepagents skills list` to verify discovery

### Exercise 2: Interactive Testing & Iteration

- Launch CLI, invoke via `/skill:hello-skill`
- Observe behavior, identify a prompt issue (e.g., too verbose)
- Edit SKILL.md, run `/reload`, re-test — no restart needed
- Key lesson: the edit → reload → test loop is seconds, not minutes

### Exercise 3: A Real Skill — code-explainer

- Write a skill that takes code and explains it at a chosen level (beginner/intermediate/expert)
- Test interactively with different inputs
- Iterate on the prompt until output quality is right
- Demonstrate that the skill description guides when the agent auto-selects it

### Exercise 4: Headless Mode

- Run the same skill non-interactively:
  ```bash
  cat some_file.py | deepagents --skill code-explainer -n "explain for a beginner" -q
  ```
- Show piping output to a file
- Same skill, same behavior, different interface
- Demonstrate `-S` flag for shell command allowlisting

### Exercise 5: A Second Skill — code-reviewer

- Write a review skill with specific review criteria in the prompt
- Test interactively, then headlessly:
  ```bash
  git diff | deepagents --skill code-reviewer -n "focus on security" -q
  ```
- Two skills now coexist — the agent can auto-select based on task

### Exercise 6: Programmatic Bridge

- Take both skills and use them with `create_deep_agent(skills=["./skills/"])` in a Python script
- Same SKILL.md files, same behavior, now in application code
- Print `delegation_trace()` to show skills being loaded
- Key lesson: CLI and SDK share the same skill format — develop in CLI, deploy in code

### Exercise 7: Skill Iteration Workflow Recap

- Recap the inner loop: write SKILL.md → test in CLI → `/reload` → iterate → test headlessly → use programmatically
- This is the dev workflow for agent capabilities
- Mention: this pattern works for teams — one person writes skills, another consumes them programmatically

## Part 2: Project-Aware Agents

**File:** `23-bonus-cli-projects.adoc`

**Narrative arc:** The CLI auto-discovers project configuration from directory conventions. Assemble subagents, skills, and MCP into a self-contained project that anyone can clone and immediately use.

### Exercise 1: The `.deepagents/` Directory

- Create the project structure:
  ```
  .deepagents/
    AGENTS.md           # project-level context
    skills/             # project skills
    agents/             # subagent definitions
      researcher/
        AGENTS.md
      analyst/
        AGENTS.md
  ```
- Explain what the CLI loads, from where, and in what order
- Precedence: project-level overrides user-level

### Exercise 2: Subagents via AGENTS.md Files

- Create `researcher` (Haiku) and `analyst` (Sonnet) as AGENTS.md files
- Show frontmatter format: `name`, `description`, `model` — maps directly to the programmatic `subagents=[...]` dicts from Modules 7-8
- Launch CLI, ask it to delegate — observe model routing
- Link back to Module 7 (subagent fundamentals) and Module 8 (YAML subagents)

### Exercise 3: Model Cost Optimization

- Override `general-purpose` subagent with cheaper model via `.deepagents/agents/general-purpose/AGENTS.md`
- Show how different models per subagent balance capability vs cost
- The researcher uses Haiku (fast, cheap lookups), analyst uses Sonnet (deep reasoning), general-purpose uses Haiku (routine delegation)
- Tie back to Module 7 Exercise 5 (model routing) and Module 8 Exercise 5 (env var overrides)

### Exercise 4: Adding Project Skills

- Move skills from Part 1 into `.deepagents/skills/`
- Launch CLI from project root — skills are auto-discovered
- Subagents + skills work together: main agent can delegate to a subagent AND invoke skills
- `deepagents skills list` shows both project and user-level skills

### Exercise 5: Project MCP Integration

- Add a `.mcp.json` to the project
- Show CLI picks it up automatically
- Note: same format as Claude Code — one config file, two tools can consume it
- `/mcp` command to inspect loaded servers

### Exercise 6: Headless Project Workflows

- Script a multi-step pipeline:
  ```bash
  deepagents -n "Research X, then review the findings" -S recommended -q
  ```
- Agent uses project subagents, skills, and MCP tools — all from directory structure
- Show chaining with shell: output of one invocation feeds the next
- No Python code involved — pure CLI + project config

### Exercise 7: The Starter Repo

- Students clone a purpose-built repo (e.g., `deep-agents-skills-starter` or hosted in workshop materials)
- Repo contains:
  ```
  .deepagents/
    AGENTS.md              # project context
    agents/
      researcher/AGENTS.md  # Haiku model
      analyst/AGENTS.md     # Sonnet model
    skills/
      code-explainer/SKILL.md
      code-reviewer/SKILL.md
  .mcp.json                # optional MCP server
  README.md
  ```
- Run `deepagents` from inside — immediately have a working multi-capability agent
- Modify a skill prompt and a subagent model to make it their own
- Key lesson: agent projects are portable — share via git, onboard via clone

### Exercise 8: Programmatic Equivalence

- Python script that loads the same `.deepagents/` config:
  - Skills from `.deepagents/skills/` via `create_deep_agent(skills=[".deepagents/skills/"])`
  - Subagents parsed from `.deepagents/agents/` AGENTS.md files using a `load_agents_md()` helper that reads frontmatter (name, description, model) + body (system_prompt) — same pattern as Module 8's `load_subagents()` but for markdown instead of YAML
- `delegation_trace()` shows the same subagents and skills working
- CLI is the interactive face, SDK is the programmatic one — same config, same behavior

## Module 11 Update

Add a closing note to the existing Module 11:

```asciidoc
TIP: For advanced CLI usage — skill development workflows, project-aware agents with model routing, and the clone-and-go pattern — see xref:22-bonus-cli-skills.adoc[Bonus: CLI Skills Development] and xref:23-bonus-cli-projects.adoc[Bonus: CLI Project-Aware Agents].
```

## Starter Repo

A minimal repo to be created (or hosted in workshop materials for `wget`/`git clone`). Contents defined in Exercise 7 above. Should be small enough to inspect fully — no more than 6-8 files. Each file should have clear comments explaining its purpose.

## Content Conventions

- Follow all existing workshop conventions (CLAUDE.md): second-person narrative, numbered steps, `[source,role="execute"]` blocks, Run/Code Preview tabs for Python scripts, sample outputs
- Use `MODEL` env var pattern where applicable
- Headless examples woven into exercises where natural, not a separate section
- Cross-reference Modules 7, 8, 9, and 11 where the CLI equivalents map to programmatic patterns
