# CLI Bonus Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create two bonus workshop modules covering CLI skill development workflows and project-aware agent configuration, culminating in a clone-and-go starter repo.

**Architecture:** Two AsciiDoc modules (`22-bonus-cli-skills.adoc`, `23-bonus-cli-projects.adoc`) following existing Showroom conventions. A starter repo directory (`starter-repo/`) provides the clone-and-go artifact. Module 11 gets a closing TIP linking to the new modules. Nav.adoc updated.

**Tech Stack:** AsciiDoc (Antora/Showroom format), Deep Agents CLI, SKILL.md files, AGENTS.md files, Python (for programmatic bridge exercises)

**Key references:**
- Spec: `docs/superpowers/specs/2026-04-12-cli-bonus-modules-design.md`
- Existing conventions: `CLAUDE.md` (project root)
- Module 9 (`09-skills.adoc`) — SKILL.md format, discovery, programmatic usage
- Module 11 (`11-cli.adoc`) — CLI basics being extended
- Module 7-8 — subagent fundamentals, YAML loader pattern
- CLI docs: `https://docs.langchain.com/oss/python/deepagents/cli/overview`

**Content conventions (from CLAUDE.md):**
- Second-person narrative ("You" not "participants")
- Numbered steps with AsciiDoc `. Step:` syntax
- `[source,role="execute"]` for click-to-run commands
- `cat > file << 'EOF'` for file creation, `uv run script.py` for execution
- Run/Code Preview tabs for Python scripts
- `.Sample output (your results may vary)` blocks after commands
- `MODEL` env var pattern: `os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")`
- Cross-references use `xref:` links

---

### Task 1: Create Part 1 — CLI as a Skill Development Tool (Exercises 1-3)

**Files:**
- Create: `content/modules/ROOT/pages/22-bonus-cli-skills.adoc`

This task covers the first half of Part 1: skill anatomy, interactive testing/iteration, and building the code-explainer skill.

- [ ] **Step 1: Create the file with header and Exercise 1 (Skill Anatomy)**

Create `content/modules/ROOT/pages/22-bonus-cli-skills.adoc` with:

```asciidoc
= Bonus: CLI Skills Development
:source-highlighter: rouge

In xref:11-cli.adoc[Module 11] you learned the CLI basics — TUI, configuration, headless mode. Now you'll use the CLI as a *skill development tool*: the fastest way to write, test, and iterate on agent capabilities that work in both the CLI and your Python code.

This module builds on xref:09-skills.adoc[Module 9]'s SKILL.md format. You'll create real skills, test them interactively, iterate without restarting, prove they work headlessly, and then use the exact same files programmatically.

== Exercise 1: Skill Anatomy Refresher

A skill is a directory containing a `SKILL.md` file. The file has YAML frontmatter (name, description) and a markdown body with instructions. Here's the minimal structure:

[source]
----
skills/
  hello-skill/
    SKILL.md
----

The CLI discovers skills from several directories, checked in this order (later entries override earlier ones on name collision):

[cols="1,2",options="header"]
|===
|Location |Scope

|`~/.deepagents/<agent>/skills/`
|User-level — available in all CLI sessions

|`~/.agents/skills/`
|User-level (alternative path)

|`.deepagents/skills/`
|Project-level — available when you're in this directory

|`.agents/skills/`
|Project-level (alternative path)
|===

. Create a minimal skill that formats greetings in different styles:
+
[source,role="execute"]
----
mkdir -p skills/hello-skill
cat > skills/hello-skill/SKILL.md << 'EOF'
---
name: hello-skill
description: Format greetings in different styles — formal, casual, or pirate
---

When asked to greet someone, format the greeting based on the requested style:

- **formal**: "Dear [Name], I hope this message finds you well."
- **casual**: "Hey [Name]! What's up?"
- **pirate**: "Ahoy, [Name]! Ye scurvy dog!"

Always include the person's name. If no style is specified, default to casual.
EOF
----

. Verify the CLI discovers it:
+
[source,role="execute"]
----
deepagents skills list
----
+
.Sample output (your results may vary)
----
Available skills:
  hello-skill - Format greetings in different styles — formal, casual, or pirate
...
----
+
The `description` from the frontmatter is what the agent sees in its skill catalog. It uses this to decide when to auto-select the skill.
```

- [ ] **Step 2: Add Exercise 2 (Interactive Testing & Iteration)**

Append Exercise 2 to the file:

```asciidoc
== Exercise 2: Interactive Testing & Iteration

The CLI's edit → reload → test loop is the fastest way to develop skills. You don't need to restart the CLI to pick up changes.

. Launch the CLI:
+
[source,role="execute"]
----
deepagents
----

. Invoke the skill explicitly:
+
----
/skill:hello-skill Greet Alice in pirate style
----
+
.Sample output (your results may vary)
----
Ahoy, Alice! Ye scurvy dog!
----

. Now try without specifying a style:
+
----
/skill:hello-skill Greet Bob
----
+
The agent should default to casual. If the output isn't what you expect — maybe it's too verbose or ignores the default — you can fix the skill without leaving the CLI.

. In a separate terminal, edit the SKILL.md to improve it. For example, add an output constraint:
+
[source,role="execute"]
----
cat > skills/hello-skill/SKILL.md << 'EOF'
---
name: hello-skill
description: Format greetings in different styles — formal, casual, or pirate
---

When asked to greet someone, format the greeting based on the requested style:

- **formal**: "Dear [Name], I hope this message finds you well."
- **casual**: "Hey [Name]! What's up?"
- **pirate**: "Ahoy, [Name]! Ye scurvy dog!"

Always include the person's name. If no style is specified, default to casual.

IMPORTANT: Output ONLY the greeting line. No preamble, no explanation, no extra text.
EOF
----

. Back in the CLI, reload and re-test:
+
----
/reload
/skill:hello-skill Greet Charlie
----
+
The skill now produces tighter output. This is the dev loop: edit the SKILL.md → `/reload` → test → repeat. No restarts, no redeployment.

. Exit the CLI when you're satisfied:
+
----
/exit
----
```

- [ ] **Step 3: Add Exercise 3 (code-explainer skill)**

Append Exercise 3:

```asciidoc
== Exercise 3: A Real Skill — code-explainer

Let's build something useful: a skill that explains code at a chosen level of detail.

. Create the code-explainer skill:
+
[source,role="execute"]
----
mkdir -p skills/code-explainer
cat > skills/code-explainer/SKILL.md << 'EOF'
---
name: code-explainer
description: Explain code at a chosen level — beginner, intermediate, or expert
---

When given code to explain, adapt your explanation to the requested level:

## Beginner
- Explain what every line does in plain English
- Define technical terms when you use them
- Use analogies to everyday concepts
- Assume no programming background

## Intermediate
- Focus on the logic flow and design patterns
- Explain why things are done this way, not just what they do
- Mention relevant standard library or framework concepts
- Assume familiarity with the language basics

## Expert
- Focus on performance characteristics, edge cases, and trade-offs
- Discuss algorithmic complexity where relevant
- Note any subtle bugs or improvements
- Assume deep language and ecosystem knowledge

If no level is specified, default to intermediate.

Format: Start with a one-sentence summary, then the detailed explanation.
EOF
----

. Launch the CLI and test with a code sample:
+
[source,role="execute"]
----
deepagents
----
+
Try: "Explain this code for a beginner:" followed by a small Python snippet, or pipe a file:
+
----
/skill:code-explainer Explain this for a beginner:

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
----

. Now ask for the same code at expert level:
+
----
/skill:code-explainer Explain this for an expert:

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
----
+
Notice how the same skill adapts its output based on the level. The SKILL.md body defines the behavior; the agent follows it.

. Try auto-selection — don't invoke the skill explicitly:
+
----
Can you explain what this Python function does?

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
----
+
The agent reads all skill descriptions and decides whether `code-explainer` is the right fit. If the description is specific enough, it will auto-select. If not, you'd refine the description.

. Exit the CLI:
+
----
/exit
----
```

- [ ] **Step 4: Verify the file renders correctly**

Run the Antora preview to verify formatting:

```bash
podman run --rm --name antora -v $PWD:/antora -p 8080:8080 -i -t ghcr.io/juliaaano/antora-viewer
```

Check `http://localhost:8080` for the new module page. Verify: heading hierarchy, execute blocks render with copy buttons, sample outputs look clean.

- [ ] **Step 5: Commit**

```bash
git add content/modules/ROOT/pages/22-bonus-cli-skills.adoc
git commit -m "Add CLI skills development bonus module (Exercises 1-3)"
```

---

### Task 2: Complete Part 1 — Exercises 4-7 (Headless, Second Skill, Programmatic Bridge, Recap)

**Files:**
- Modify: `content/modules/ROOT/pages/22-bonus-cli-skills.adoc`

- [ ] **Step 1: Add Exercise 4 (Headless Mode)**

Append to `22-bonus-cli-skills.adoc`:

```asciidoc
== Exercise 4: Headless Mode

The same skills work in non-interactive mode — pipe input, get output, no TUI. This is the same skill, same behavior, different interface.

. Run the code-explainer headlessly on a file:
+
[source,role="execute"]
----
cat > sample_code.py << 'EOF'
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_lookup(key: str) -> dict:
    # Simulate a slow database query
    import time
    time.sleep(0.1)
    return {"key": key, "value": f"result_{key}"}
EOF
----
+
[source,role="execute"]
----
cat sample_code.py | deepagents --skill code-explainer -n "explain for a beginner" -q
----
+
.Sample output (your results may vary)
----
This code creates a function that remembers its answers to avoid doing slow work twice.

The `@lru_cache(maxsize=128)` line is a decorator that tells Python: "If someone
asks for the same key again, just return what you calculated last time instead of
waiting." It keeps up to 128 previous answers in memory...
----

. Pipe the output to a file:
+
[source,role="execute"]
----
cat sample_code.py | deepagents --skill code-explainer -n "explain for an expert" -q > explanation.txt
cat explanation.txt
----
+
The `-q` flag gives clean output suitable for piping — no TUI chrome, no progress indicators, just the response.

. Combine with shell tools:
+
[source,role="execute"]
----
git diff HEAD~1 | deepagents --skill code-explainer -n "summarize what changed" -q
----
+
This is the power of headless mode: your skills become composable shell commands. Anything that produces text can be piped in; the output can be piped to files, other commands, or CI/CD pipelines.

NOTE: In non-interactive mode, shell execution is disabled by default. Use `-S recommended` to allow common commands, or `-S "pytest,git,make"` for specific ones.
```

- [ ] **Step 2: Add Exercise 5 (code-reviewer skill)**

```asciidoc
== Exercise 5: A Second Skill — code-reviewer

Let's add a second skill so the agent has a choice of capabilities.

. Create the code-reviewer skill:
+
[source,role="execute"]
----
mkdir -p skills/code-reviewer
cat > skills/code-reviewer/SKILL.md << 'EOF'
---
name: code-reviewer
description: Review code for bugs, security issues, and improvements
---

When asked to review code, provide structured feedback:

## Review Checklist
1. **Bugs** — logic errors, off-by-one, null/undefined risks
2. **Security** — injection, secrets in code, unsafe deserialization
3. **Performance** — unnecessary allocations, O(n^2) where O(n) exists
4. **Readability** — naming, complexity, missing context
5. **Testing** — what tests would you add?

## Output Format
For each finding:
- **Category**: [Bug/Security/Performance/Readability/Testing]
- **Location**: function or line reference
- **Issue**: what's wrong
- **Fix**: concrete suggestion

End with a summary: "X findings: N bugs, N security, N performance, N readability, N testing suggestions."

If no issues found in a category, skip it. Be specific — no vague advice.
EOF
----

. Test interactively:
+
[source,role="execute"]
----
deepagents
----
+
----
/skill:code-reviewer Review this code:

def process_user_input(data):
    query = f"SELECT * FROM users WHERE name = '{data}'"
    result = db.execute(query)
    password = "admin123"
    return result
----
+
.Sample output (your results may vary)
----
**Security**: SQL injection — `data` is interpolated directly into the query.
  Fix: Use parameterized queries: `db.execute("SELECT * FROM users WHERE name = ?", (data,))`

**Security**: Hardcoded password on line 4.
  Fix: Move to environment variable or secrets manager.

Summary: 2 findings: 0 bugs, 2 security, 0 performance, 0 readability, 0 testing suggestions.
----

. Exit and test headlessly with a real diff:
+
[source,role="execute"]
----
/exit
----
+
[source,role="execute"]
----
git diff | deepagents --skill code-reviewer -n "focus on security issues" -q
----
+
Two skills now coexist. When you ask without specifying a skill, the agent reads both descriptions and routes to the right one — "explain this code" goes to `code-explainer`, "review this for bugs" goes to `code-reviewer`.
```

- [ ] **Step 3: Add Exercise 6 (Programmatic Bridge)**

```asciidoc
== Exercise 6: Programmatic Bridge

The skills you developed in the CLI work identically with the Python SDK. Same SKILL.md files, same behavior, now embedded in your application.

. Create a script that uses both skills programmatically:
+
[tabs]
====
Run::
+
[source,role="execute"]
----
cat > skill_bridge.py << 'EOF'
import os
from deepagents import create_deep_agent
from utils import agent_response, delegation_trace

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")

# Point the SDK at the same skills directory the CLI uses
agent = create_deep_agent(
    model=MODEL,
    skills=["./skills/"],
)

result = agent.invoke({"messages": [("user",
    "Explain what a Python decorator does, for a beginner."
)]})

print(delegation_trace(result))
print(agent_response(result))
EOF
----

Code Preview::
+
[source,python]
----
import os
from deepagents import create_deep_agent
from utils import agent_response, delegation_trace

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")

# Point the SDK at the same skills directory the CLI uses
agent = create_deep_agent(
    model=MODEL,
    skills=["./skills/"],
)

result = agent.invoke({"messages": [("user",
    "Explain what a Python decorator does, for a beginner."
)]})

print(delegation_trace(result))
print(agent_response(result))
----
====

. Run it:
+
[source,role="execute"]
----
uv run skill_bridge.py
----
+
.Sample output (your results may vary)
----
=== Delegation Trace ===
  Step 1: general-purpose (inherited)
          Explain what a Python decorator does, at a beginner level...
  Total: 1 delegation(s)

A decorator is like a gift wrapper for functions...
----
+
The same `code-explainer` SKILL.md you tested in the CLI is now powering your Python application. Edit the skill in one place, both interfaces pick up the change.

This is the key insight: **develop skills in the CLI** where the feedback loop is fast, **deploy them in code** where you need programmatic control. One skill format serves both.
```

- [ ] **Step 4: Add Exercise 7 (Workflow Recap) and Module Summary**

```asciidoc
== Exercise 7: The Skill Development Workflow

You've now experienced the full skill development loop. Here it is as a repeatable process:

. **Write** a SKILL.md with frontmatter (name, description) and a markdown body (instructions).

. **Test interactively** — launch the CLI, invoke with `/skill:name`, observe behavior.

. **Iterate** — edit the SKILL.md in your editor, run `/reload` in the CLI, re-test. No restart needed.

. **Test headlessly** — pipe input through `deepagents --skill name -n "task" -q` to verify non-interactive behavior.

. **Use programmatically** — pass `skills=["./skills/"]` to `create_deep_agent()` in your Python code. Same files, same behavior.

. **Share** — commit the `skills/` directory to git. Teammates get the skills by pulling.

This workflow works for teams: one person writes and refines skills in the CLI, another consumes them programmatically in a production pipeline. The SKILL.md is the shared contract.

TIP: For project-aware agents that auto-discover skills, subagents, and MCP tools from directory conventions — including a clone-and-go pattern — see xref:23-bonus-cli-projects.adoc[Bonus: CLI Project-Aware Agents].

== Module Summary

You've learned to use the CLI as a skill development tool:

* **Skill anatomy** — SKILL.md with YAML frontmatter and markdown instructions
* **Interactive testing** — `/skill:name` to invoke, `/reload` to pick up edits
* **Iteration** — edit → reload → test in seconds, not minutes
* **Headless mode** — same skills work with `-n` for scripting and piping
* **Programmatic bridge** — `create_deep_agent(skills=["./skills/"])` uses the same files
* **Dev workflow** — write in CLI, deploy in code, share via git

Next, in xref:23-bonus-cli-projects.adoc[Part 2], you'll assemble skills, subagents, and MCP into a self-contained project anyone can clone and use immediately.
```

- [ ] **Step 5: Commit**

```bash
git add content/modules/ROOT/pages/22-bonus-cli-skills.adoc
git commit -m "Complete CLI skills development bonus module (Exercises 4-7)"
```

---

### Task 3: Create Part 2 — Project-Aware Agents (Exercises 1-4)

**Files:**
- Create: `content/modules/ROOT/pages/23-bonus-cli-projects.adoc`

- [ ] **Step 1: Create the file with header and Exercise 1 (.deepagents/ directory)**

Create `content/modules/ROOT/pages/23-bonus-cli-projects.adoc`:

```asciidoc
= Bonus: CLI Project-Aware Agents
:source-highlighter: rouge

In xref:22-bonus-cli-skills.adoc[Part 1] you built skills and tested them in the CLI. Now you'll assemble skills, subagents, and MCP configuration into a self-contained project that anyone can clone and use immediately.

The Deep Agents CLI automatically discovers project configuration from directory conventions. No command-line flags, no environment variables — just the right files in the right places.

== Exercise 1: The `.deepagents/` Directory

The CLI looks for a `.deepagents/` directory in your project root. Everything inside it is loaded automatically when you launch the CLI from that directory.

. Create the project structure:
+
[source,role="execute"]
----
mkdir -p cli-project/.deepagents/agents/researcher
mkdir -p cli-project/.deepagents/agents/analyst
mkdir -p cli-project/.deepagents/skills
----

. Add project-level context:
+
[source,role="execute"]
----
cat > cli-project/.deepagents/AGENTS.md << 'EOF'
# Project Context

This is a code analysis project. When working in this project:

- Focus on Python code quality and best practices
- Use the researcher subagent for gathering information
- Use the analyst subagent for deep code analysis
- Apply code-explainer and code-reviewer skills when appropriate
EOF
----
+
This `AGENTS.md` is appended to the agent's system prompt every session. It gives the agent project-specific knowledge without you having to repeat it.

. Verify the structure:
+
[source,role="execute"]
----
find cli-project/.deepagents -type f
----
+
.Sample output (your results may vary)
----
cli-project/.deepagents/AGENTS.md
----
+
The CLI loads configuration in this order (later overrides earlier):

[cols="1,2",options="header"]
|===
|Source |What it provides

|`~/.deepagents/`
|User-level: global skills, memories, default config

|`.deepagents/`
|Project-level: project skills, subagents, context

|`.mcp.json`
|MCP servers (project root, Claude Code compatible)
|===

Project-level configuration overrides user-level when names collide. This means a project can customize behavior without affecting your global setup.
```

- [ ] **Step 2: Add Exercise 2 (Subagents via AGENTS.md)**

```asciidoc
== Exercise 2: Subagents via AGENTS.md Files

In xref:07-subagent-fundamentals.adoc[Module 7] and xref:08-yaml-subagents.adoc[Module 8], you defined subagents as Python dicts and YAML files. The CLI uses a third format: markdown AGENTS.md files with YAML frontmatter.

Each subagent lives in its own directory under `.deepagents/agents/`. The directory name is the subagent's routing name.

. Create a researcher subagent using Haiku for fast, cheap lookups:
+
[source,role="execute"]
----
cat > cli-project/.deepagents/agents/researcher/AGENTS.md << 'EOF'
---
name: researcher
description: Research topics and gather factual information. Use for quick lookups, definitions, and background research.
model: anthropic:claude-haiku-4-5-20251001
---

You are a research assistant. Your job is to find and summarize information clearly.

## Your Process
1. Break down the question into searchable aspects
2. Provide factual, well-organized information
3. Keep responses concise — summaries, not essays
4. Cite your reasoning when making claims
EOF
----

. Create an analyst subagent using Sonnet for deep reasoning:
+
[source,role="execute"]
----
cat > cli-project/.deepagents/agents/analyst/AGENTS.md << 'EOF'
---
name: analyst
description: Perform deep analysis requiring critical thinking, trade-off evaluation, and nuanced reasoning. Use for complex questions.
model: anthropic:claude-sonnet-4-6
---

You are an analytical expert. Your job is to provide thorough, multi-perspective analysis.

## Your Process
1. Consider the question from multiple angles
2. Evaluate trade-offs explicitly
3. Support conclusions with reasoning
4. Acknowledge uncertainty where it exists
EOF
----
+
Notice how the frontmatter maps directly to the programmatic subagent dict:
+
[cols="1,1",options="header"]
|===
|AGENTS.md frontmatter |Python dict equivalent

|`name: researcher`
|`"name": "researcher"`

|`description: Research topics...`
|`"description": "Research topics..."`

|`model: anthropic:claude-haiku-4-5-20251001`
|`"model": "anthropic:claude-haiku-4-5-20251001"`

|Markdown body
|`"system_prompt": "You are a research assistant..."`
|===

. Launch the CLI from the project directory and test delegation:
+
[source,role="execute"]
----
cd cli-project
deepagents
----
+
----
What is the CAP theorem? Keep it brief.
----
+
The agent should delegate to the `researcher` (Haiku) for this factual lookup.
+
Now ask something that requires deeper analysis:
+
----
Should I use PostgreSQL or MongoDB for a new e-commerce platform? Consider scalability, team expertise, and data consistency.
----
+
This should route to `analyst` (Sonnet) for the complex trade-off evaluation.

. Exit the CLI:
+
----
/exit
----
```

- [ ] **Step 3: Add Exercise 3 (Model Cost Optimization)**

```asciidoc
== Exercise 3: Model Cost Optimization

Every delegation to the default `general-purpose` subagent uses your main agent's model. For routine tasks, that's wasteful. You can override it with a cheaper model.

. Create a cost-optimized general-purpose subagent:
+
[source,role="execute"]
----
mkdir -p .deepagents/agents/general-purpose
cat > .deepagents/agents/general-purpose/AGENTS.md << 'EOF'
---
name: general-purpose
description: General-purpose agent for research and multi-step tasks
model: anthropic:claude-haiku-4-5-20251001
---

You are a general-purpose assistant. Complete tasks efficiently and return concise summaries. Do not include raw data or intermediate results — focus on the final answer.
EOF
----
+
Now your agent team has three models in play:
+
[cols="1,1,1",options="header"]
|===
|Subagent |Model |Purpose

|Main agent
|Sonnet (orchestration)
|Decides what to delegate and integrates results

|researcher
|Haiku (fast/cheap)
|Quick factual lookups

|analyst
|Sonnet (capable)
|Deep reasoning and analysis

|general-purpose
|Haiku (fast/cheap)
|Routine delegation — context isolation without cost
|===
+
This is the same model routing pattern from xref:07-subagent-fundamentals.adoc#exercise-5-model-routing[Module 7 Exercise 5], but configured entirely in markdown — no Python code.

. Launch the CLI and test:
+
[source,role="execute"]
----
deepagents
----
+
----
Delegate to a subagent: calculate the factorial of 10 and explain it.
----
+
This routine task should route to `general-purpose` (Haiku) — fast and cheap. The analyst model is reserved for tasks that actually need it.

. Exit the CLI:
+
----
/exit
----
```

- [ ] **Step 4: Add Exercise 4 (Adding Project Skills)**

```asciidoc
== Exercise 4: Adding Project Skills

Skills and subagents work together. Let's add the skills you built in xref:22-bonus-cli-skills.adoc[Part 1] to this project.

. Copy the skills into the project's `.deepagents/skills/` directory:
+
[source,role="execute"]
----
cp -r ../skills/code-explainer .deepagents/skills/
cp -r ../skills/code-reviewer .deepagents/skills/
----

. Verify the project now has both subagents and skills:
+
[source,role="execute"]
----
find .deepagents -name "*.md" | sort
----
+
.Sample output (your results may vary)
----
.deepagents/AGENTS.md
.deepagents/agents/analyst/AGENTS.md
.deepagents/agents/general-purpose/AGENTS.md
.deepagents/agents/researcher/AGENTS.md
.deepagents/skills/code-explainer/SKILL.md
.deepagents/skills/code-reviewer/SKILL.md
----

. Launch the CLI and verify everything is discovered:
+
[source,role="execute"]
----
deepagents skills list
----
+
.Sample output (your results may vary)
----
Available skills:
  code-explainer - Explain code at a chosen level — beginner, intermediate, or expert
  code-reviewer  - Review code for bugs, security issues, and improvements
----

. Test the combined setup — subagents and skills working together:
+
[source,role="execute"]
----
deepagents
----
+
----
Research what Python decorators are, then explain the concept for a beginner.
----
+
Watch the orchestration: the main agent may delegate research to the `researcher` subagent, then use the `code-explainer` skill to format the explanation. Skills and subagents complement each other — subagents handle delegation, skills handle specialized formatting.

. Exit the CLI:
+
----
/exit
----
```

- [ ] **Step 5: Commit**

```bash
git add content/modules/ROOT/pages/23-bonus-cli-projects.adoc
git commit -m "Add CLI project-aware agents bonus module (Exercises 1-4)"
```

---

### Task 4: Complete Part 2 — Exercises 5-8 (MCP, Headless, Starter Repo, Programmatic Equivalence)

**Files:**
- Modify: `content/modules/ROOT/pages/23-bonus-cli-projects.adoc`

- [ ] **Step 1: Add Exercise 5 (Project MCP Integration)**

Append to `23-bonus-cli-projects.adoc`:

```asciidoc
== Exercise 5: Project MCP Integration

The CLI picks up MCP server configuration from `.mcp.json` in your project root — the same file Claude Code uses.

. Add an MCP configuration:
+
[source,role="execute"]
----
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "docs-langchain": {
      "type": "http",
      "url": "https://docs.langchain.com/mcp"
    }
  }
}
EOF
----
+
This adds the LangChain documentation server. When the agent needs to look up Deep Agents API details, it can query the docs directly.

. Launch the CLI and verify MCP is loaded:
+
[source,role="execute"]
----
deepagents
----
+
----
/mcp
----
+
.Sample output (your results may vary)
----
Connected MCP servers:
  docs-langchain (http) - https://docs.langchain.com/mcp
----

. Test it with a docs query:
+
----
What parameters does create_deep_agent() accept? Check the docs.
----
+
The agent can now query live documentation through MCP, in addition to using its subagents and skills.

. Exit the CLI:
+
----
/exit
----
+
NOTE: The `.mcp.json` format is shared with Claude Code. If you already have one in your project for Claude Code, the Deep Agents CLI picks it up automatically — one config, two tools.
```

- [ ] **Step 2: Add Exercise 6 (Headless Project Workflows)**

```asciidoc
== Exercise 6: Headless Project Workflows

Everything you've assembled — subagents, skills, MCP — works in headless mode too. The project configuration is discovered automatically regardless of interactive or non-interactive mode.

. Run a task that exercises the full project config:
+
[source,role="execute"]
----
deepagents -n "Research what the Observer pattern is and explain it for a beginner" -q
----
+
The agent uses the project's researcher subagent and code-explainer skill — all discovered from `.deepagents/`, no flags needed.

. Chain commands in a shell pipeline:
+
[source,role="execute"]
----
cat sample_code.py | deepagents -n "Review this code, then explain the key issues for a beginner" -q > review_and_explain.txt
cat review_and_explain.txt
----

. Script a multi-step workflow:
+
[source,role="execute"]
----
cat > analyze.sh << 'SCRIPT'
#!/bin/bash
echo "=== Code Review ==="
cat "$1" | deepagents --skill code-reviewer -n "review this code" -q

echo ""
echo "=== Beginner Explanation ==="
cat "$1" | deepagents --skill code-explainer -n "explain for a beginner" -q
SCRIPT
chmod +x analyze.sh
----
+
[source,role="execute"]
----
./analyze.sh sample_code.py
----
+
No Python code, no SDK — just the CLI + project configuration + shell scripting. The project's `.deepagents/` directory makes the agent self-configuring.
```

- [ ] **Step 3: Add Exercise 7 (The Starter Repo)**

```asciidoc
== Exercise 7: The Starter Repo

Everything you've built can be packaged into a git repository that anyone can clone and use immediately. Let's verify the project is self-contained.

. Review the complete project structure:
+
[source,role="execute"]
----
find . -not -path './.git/*' -not -name '.git' | sort
----
+
.Sample output (your results may vary)
----
.
./.deepagents
./.deepagents/AGENTS.md
./.deepagents/agents
./.deepagents/agents/analyst/AGENTS.md
./.deepagents/agents/general-purpose/AGENTS.md
./.deepagents/agents/researcher/AGENTS.md
./.deepagents/skills
./.deepagents/skills/code-explainer/SKILL.md
./.deepagents/skills/code-reviewer/SKILL.md
./.mcp.json
----

. Initialize it as a git repository:
+
[source,role="execute"]
----
git init
git add .
git commit -m "Initial commit: project-aware agent with skills and subagents"
----
+
This is now a shareable, clonable agent project. Anyone with the Deep Agents CLI installed can:
+
[source,bash]
----
git clone <your-repo-url>
cd <repo-name>
deepagents
----
+
And immediately have a working agent with:
+
* Three subagents (researcher/Haiku, analyst/Sonnet, general-purpose/Haiku)
* Two skills (code-explainer, code-reviewer)
* MCP documentation access
* Project context via AGENTS.md

. Make it your own — modify a subagent's model:
+
[source,role="execute"]
----
cat > .deepagents/agents/researcher/AGENTS.md << 'EOF'
---
name: researcher
description: Research topics and gather factual information. Use for quick lookups, definitions, and background research.
model: anthropic:claude-sonnet-4-6
---

You are a research assistant. Your job is to find and summarize information clearly.

## Your Process
1. Break down the question into searchable aspects
2. Provide factual, well-organized information
3. Keep responses concise — summaries, not essays
4. Cite your reasoning when making claims
EOF
----
+
The researcher now uses Sonnet instead of Haiku. Test it:
+
[source,role="execute"]
----
deepagents -n "What is the difference between concurrency and parallelism?" -q
----
+
One file edit, no code changes, no redeployment. This is the power of the project-aware pattern.
```

- [ ] **Step 4: Add Exercise 8 (Programmatic Equivalence) and Module Summary**

```asciidoc
== Exercise 8: Programmatic Equivalence

The CLI and SDK can share the same project configuration. Let's load the `.deepagents/` directory structure from Python.

. Create a loader for AGENTS.md subagent files:
+
[tabs]
====
Run::
+
[source,role="execute"]
----
cat > load_agents_md.py << 'EOF'
import os
import re
from pathlib import Path


def load_agents_md(agents_dir: Path) -> list:
    """Load subagent definitions from AGENTS.md files.

    Each subdirectory in agents_dir should contain an AGENTS.md
    with YAML frontmatter (name, description, model) and a
    markdown body (system_prompt).

    Same env var override as the YAML loader:
    {NAME}_MODEL overrides the frontmatter model.
    """
    subagents = []
    for agent_dir in sorted(agents_dir.iterdir()):
        agents_md = agent_dir / "AGENTS.md"
        if not agents_md.is_file():
            continue

        text = agents_md.read_text()

        # Parse YAML frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
        if not match:
            continue

        frontmatter, body = match.groups()

        # Simple YAML parsing for flat key: value pairs
        meta = {}
        for line in frontmatter.strip().splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                meta[key.strip()] = val.strip()

        name = meta.get("name", agent_dir.name)
        subagent = {
            "name": name,
            "description": meta.get("description", ""),
            "system_prompt": body.strip(),
        }

        # Model: env var override, then frontmatter, then inherit
        env_key = f"{name.upper().replace('-', '_')}_MODEL"
        model = os.environ.get(env_key, meta.get("model"))
        if model:
            subagent["model"] = model

        subagents.append(subagent)

    return subagents
EOF
----

Code Preview::
+
[source,python]
----
import os
import re
from pathlib import Path


def load_agents_md(agents_dir: Path) -> list:
    """Load subagent definitions from AGENTS.md files.

    Each subdirectory in agents_dir should contain an AGENTS.md
    with YAML frontmatter (name, description, model) and a
    markdown body (system_prompt).

    Same env var override as the YAML loader:
    {NAME}_MODEL overrides the frontmatter model.
    """
    subagents = []
    for agent_dir in sorted(agents_dir.iterdir()):
        agents_md = agent_dir / "AGENTS.md"
        if not agents_md.is_file():
            continue

        text = agents_md.read_text()

        # Parse YAML frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
        if not match:
            continue

        frontmatter, body = match.groups()

        # Simple YAML parsing for flat key: value pairs
        meta = {}
        for line in frontmatter.strip().splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                meta[key.strip()] = val.strip()

        name = meta.get("name", agent_dir.name)
        subagent = {
            "name": name,
            "description": meta.get("description", ""),
            "system_prompt": body.strip(),
        }

        # Model: env var override, then frontmatter, then inherit
        env_key = f"{name.upper().replace('-', '_')}_MODEL"
        model = os.environ.get(env_key, meta.get("model"))
        if model:
            subagent["model"] = model

        subagents.append(subagent)

    return subagents
----
====

. Create a script that loads the full project config programmatically:
+
[tabs]
====
Run::
+
[source,role="execute"]
----
cat > project_agent.py << 'EOF'
import os
from pathlib import Path
from deepagents import create_deep_agent
from load_agents_md import load_agents_md

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")

# Load subagents from .deepagents/agents/ AGENTS.md files
subagents = load_agents_md(Path(".deepagents/agents"))

# Load skills from .deepagents/skills/
agent = create_deep_agent(
    model=MODEL,
    subagents=subagents,
    skills=[".deepagents/skills/"],
)

print(f"Loaded {len(subagents)} subagents:")
for sa in subagents:
    print(f"  {sa['name']} ({sa.get('model', 'inherited')})")

result = agent.invoke({"messages": [("user",
    "Research the Observer design pattern, then explain it for a beginner."
)]})

from utils import agent_response, delegation_trace
print(delegation_trace(result, subagents=subagents))
print(agent_response(result))
EOF
----

Code Preview::
+
[source,python]
----
import os
from pathlib import Path
from deepagents import create_deep_agent
from load_agents_md import load_agents_md

MODEL = os.environ.get("DEEPAGENTS_MODEL", "anthropic:claude-sonnet-4-6")

# Load subagents from .deepagents/agents/ AGENTS.md files
subagents = load_agents_md(Path(".deepagents/agents"))

# Load skills from .deepagents/skills/
agent = create_deep_agent(
    model=MODEL,
    subagents=subagents,
    skills=[".deepagents/skills/"],
)

print(f"Loaded {len(subagents)} subagents:")
for sa in subagents:
    print(f"  {sa['name']} ({sa.get('model', 'inherited')})")

result = agent.invoke({"messages": [("user",
    "Research the Observer design pattern, then explain it for a beginner."
)]})

from utils import agent_response, delegation_trace
print(delegation_trace(result, subagents=subagents))
print(agent_response(result))
----
====

. Copy `utils.py` into the project and run:
+
[source,role="execute"]
----
cp ../utils.py .
uv run project_agent.py
----
+
.Sample output (your results may vary)
----
Loaded 3 subagents:
  analyst (anthropic:claude-sonnet-4-6)
  general-purpose (anthropic:claude-haiku-4-5-20251001)
  researcher (anthropic:claude-sonnet-4-6)

=== Delegation Trace ===
  Step 1: researcher (anthropic:claude-sonnet-4-6)
          Research the Observer design pattern: definition, use cases, examples...
  Total: 1 delegation(s)

The Observer pattern is like a newsletter subscription...
----
+
The CLI and SDK are two faces of the same system. The CLI auto-discovers `.deepagents/` — the SDK needs explicit paths. But the configuration files are identical. Develop interactively in the CLI, deploy programmatically with the SDK.

== Module Summary

You've built a complete project-aware agent system:

* **`.deepagents/` directory** — project-level configuration auto-discovered by the CLI
* **AGENTS.md subagents** — markdown-based subagent definitions with model routing
* **Cost optimization** — different models per subagent (Haiku for routine, Sonnet for analysis)
* **Skills + subagents** — complementary capabilities that work together
* **MCP integration** — `.mcp.json` shared with Claude Code
* **Headless workflows** — same project config works in scripts and pipelines
* **Clone-and-go** — share agent projects via git, onboard via `git clone && deepagents`
* **Programmatic equivalence** — `load_agents_md()` bridges CLI config to SDK code

The key takeaway: **agent projects are portable**. Package your skills, subagents, and configuration into a git repository. Anyone can clone it and have a working agent — whether they prefer the CLI or the SDK.
```

- [ ] **Step 5: Commit**

```bash
git add content/modules/ROOT/pages/23-bonus-cli-projects.adoc
git commit -m "Complete CLI project-aware agents bonus module (Exercises 5-8)"
```

---

### Task 5: Update Module 11, nav.adoc, and final polish

**Files:**
- Modify: `content/modules/ROOT/pages/11-cli.adoc` (add closing TIP)
- Modify: `content/modules/ROOT/nav.adoc` (add new module entries)

- [ ] **Step 1: Add closing TIP to Module 11**

Add before the `== Module summary` section in `content/modules/ROOT/pages/11-cli.adoc`:

```asciidoc
TIP: For advanced CLI usage — skill development workflows, project-aware agents with model routing, and the clone-and-go pattern — see xref:22-bonus-cli-skills.adoc[Bonus: CLI Skills Development] and xref:23-bonus-cli-projects.adoc[Bonus: CLI Project-Aware Agents].
```

- [ ] **Step 2: Add entries to nav.adoc**

Add the two new modules to the Bonus Modules section in `content/modules/ROOT/nav.adoc`, after the MCP entry:

```asciidoc
* xref:22-bonus-cli-skills.adoc[CLI Skills Development]
* xref:23-bonus-cli-projects.adoc[CLI Project-Aware Agents]
```

- [ ] **Step 3: Verify Antora build**

```bash
podman run --rm --name antora -v $PWD:/antora -p 8080:8080 -i -t ghcr.io/juliaaano/antora-viewer
```

Check:
- Both new modules appear in the left nav under Bonus Modules
- All cross-references (`xref:`) resolve correctly
- Execute blocks have copy buttons
- Run/Code Preview tabs work on Python scripts
- Module 11 TIP links work

- [ ] **Step 4: Commit**

```bash
git add content/modules/ROOT/pages/11-cli.adoc content/modules/ROOT/nav.adoc
git commit -m "Link Module 11 to CLI bonus modules, add nav entries"
```

- [ ] **Step 5: Push all changes**

```bash
git push
```
