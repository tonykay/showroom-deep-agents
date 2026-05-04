# Bonus Modules: Deep Agents Memory — Working Memory, Persistence & Learning

**Date:** 2026-05-04
**Files:** `24-bonus-memory-working.adoc`, `25-bonus-memory-learning.adoc`
**Status:** Approved

## Overview

Two bonus modules that go beyond Module 10's AGENTS.md and MemoryMiddleware basics. Part 1 teaches working memory (filesystem as scratch space, cleanup patterns) and cross-session persistence (CompositeBackend + StoreBackend with SQLite). Part 2 builds the full learning loop — agents that accumulate knowledge and genuinely improve over time.

Module 10 gets a closing link pointing students to these bonus modules.

## Prerequisites

- Module 10 (Memory & AGENTS.md) — AGENTS.md basics, MemoryMiddleware, memory layering
- Module 5 (Filesystem Tools & Backends) — FilesystemBackend, LocalShellBackend
- Module 7 (Subagent Fundamentals) — for the lessons-writer subagent in Part 2

## Key References

- https://www.langchain.com/blog/your-harness-your-memory — memory is the harness, not a plugin
- https://docs.langchain.com/oss/python/deepagents/context-engineering — five context types, CompositeBackend, StoreBackend, SummarizationToolMiddleware
- Sarah Wooders on memory as a harness concern (MemGPT, Letta Code)
- Viv Trivedy on the anatomy of agent harnesses (filesystem as shared memory backbone)

## Part 1: Working Memory & Persistence

**File:** `24-bonus-memory-working.adoc`

**Narrative arc:** Agents need different kinds of memory for different lifespans. Working memory is scratch space that lives and dies with a task. Persistent memory survives across sessions. This module teaches both mechanics.

### Exercise 1: Working Memory as Filesystem

- Create an agent with `FilesystemBackend` that uses a `scratch/` directory as working memory
- Write intermediate results to files, read them back, produce a final output
- Observe how the scratch directory fills up with the agent's "thinking"
- System prompt instructs the agent to use `scratch/` for intermediate work

### Exercise 2: The ops_manager Cleanup Pattern

- Build an ops_manager agent that handles support tickets
- For each ticket: create a `scratch/ticket-NNN/` workspace, gather information, write notes, resolve
- After resolution, the agent clears its scratch directory
- Show two tickets back-to-back — the second starts clean, no leftover context from the first
- Key lesson: working memory is intentionally ephemeral

### Exercise 3: Why Cleanup Matters

- Demonstrate what happens *without* cleanup
- Run the same agent on a third ticket without clearing scratch
- The agent gets confused by stale files from the previous ticket
- This is context pollution at the filesystem level — the same problem subagents solve at the conversation level
- Reinforces the context engineering principles from Module 7

### Exercise 4: Capstone Connection

- Brief note (not a full exercise) showing how this pattern applies to the AIOps capstone
- The incident_commander could clear its working directory between incidents
- Code snippet showing the cleanup integration
- Links back to Module 12

### Exercise 5: Cross-Session Persistence with StoreBackend

- Introduce `CompositeBackend` routing `/memories/` to a `StoreBackend` backed by SQLite
- The agent writes to `/memories/preferences.md` during a conversation
- Those files survive across invocations
- Show the agent reading its own memories on startup
- SQLite chosen for zero-infrastructure persistence — real file on disk, no external database

### Exercise 6: Proving Persistence

- Run an agent, teach it a preference ("I prefer concise answers with code examples")
- Kill the process
- Run again — the agent remembers the preference and adjusts its behavior
- Inspect the SQLite file to see what was stored
- The filesystem metaphor makes persistence transparent — the agent doesn't know it's using a database

### Exercise 7: Thread-Scoped vs Shared Memory

- Show how `MemorySaver` (checkpointer) gives per-conversation memory
- While `StoreBackend` gives cross-conversation memory
- Different scopes for different needs
- Quick comparison: resume a conversation (MemorySaver) vs recall a preference from a different conversation (StoreBackend)

## Part 2: Learning Through Memory

**File:** `25-bonus-memory-learning.adoc`

**Narrative arc:** Persistence is just storage — learning is what makes memory useful. An agent that accumulates knowledge and applies it to future tasks genuinely improves over time. This module builds the full learning loop.

### Exercise 1: The Learning Loop Concept

- Introduce the pattern: encounter → solve → remember → recall → apply
- Frame with the "memory is the harness" philosophy
- Reference LangChain blog and Sarah Wooders' argument
- Memory isn't a plugin you bolt on — it's fundamental to how the agent operates
- Set up the conceptual framework before the hands-on work

### Exercise 2: Baseline — Agent Without Memory

- Give an agent a coding task with a non-obvious gotcha
- Example: "Create a FastAPI endpoint that handles file uploads with size validation"
- The agent produces a working but naive solution — missing edge cases
- Save the output for later comparison
- Uses persistent StoreBackend from Part 1 (but empty — no prior knowledge)

### Exercise 3: Teaching the Agent

- Tell the agent about the gotcha it missed
- "File uploads over 10MB should return 413, and you need streaming UploadFile, not File"
- The agent writes this lesson to persistent memory (`/memories/lessons-learned.md`)
- Inspect the memory file — should contain the specific lesson in a reusable format
- The agent organizes the lesson by topic, not just appending raw text

### Exercise 4: The Payoff — Agent With Memory

- New session, same task, same agent
- This time it reads its memory on startup, finds the relevant lesson
- Produces a better solution that handles the edge case
- Show before/after comparison side-by-side
- Key moment: the agent learned from experience

### Exercise 5: Accumulating Knowledge

- Run three more related tasks, each teaching the agent something new
- After each, inspect the growing memory file
- The agent organizes its own knowledge — structured notes, not a flat list
- Observe how the agent starts referencing earlier lessons when solving new problems
- Memory becomes a growing knowledge base

### Exercise 6: Memory-Aware Subagents

- Create a main agent with a `lessons-writer` subagent
- After completing any task, the main agent delegates to `lessons-writer`
- The lessons-writer extracts key learnings and stores them in memory
- Separates "doing" from "learning" — main agent stays focused on the task
- The lessons-writer has its own system prompt optimized for knowledge extraction

### Exercise 7: The Self-Improving Agent

- Tie it all together: persistent memory + lessons-writer subagent + cleanup pattern from Part 1
- Run through a sequence of 3 related tasks
- By the third task, the agent is noticeably better — faster, more accurate, handles edge cases
- Print `delegation_trace()` to show the learning subagent at work
- This is the culmination: an agent that gets better with experience

### Exercise 8: References and Further Reading

- Link to the key resources with context on why they matter:
  - LangChain blog: "Your Harness, Your Memory" — the philosophical foundation
  - Sarah Wooders: memory as a harness concern, MemGPT origins
  - Viv Trivedy: anatomy of agent harnesses, filesystem as memory backbone
- Frame these as the theory behind what students just built hands-on
- Suggest next steps: production backends (Postgres, Redis), multi-tenant memory, memory compaction strategies

## Module 10 Update

Add a closing note to the existing Module 10:

```asciidoc
TIP: For advanced memory patterns — working memory with cleanup, cross-session persistence with SQLite, and agents that learn from experience — see xref:24-bonus-memory-working.adoc[Bonus: Working Memory & Persistence] and xref:25-bonus-memory-learning.adoc[Bonus: Learning Through Memory].
```

## Content Conventions

- Follow all existing workshop conventions (CLAUDE.md): second-person narrative, numbered steps, `[source,role="execute"]` blocks, Run/Code Preview tabs for Python scripts, sample outputs
- Use `MODEL` env var pattern where applicable
- `utils.py` with `agent_response()` and `delegation_trace()` for output
- Cross-reference Modules 5, 7, 10, and 12 where patterns connect
- The ops_manager scenario should feel like a realistic operations workflow
- Before/after comparisons should be concrete and visually clear
