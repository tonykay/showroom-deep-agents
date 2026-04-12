# YAML Subagent Model Override via Environment Variables

**Date:** 2026-04-12
**Module:** 08-yaml-subagents.adoc
**Status:** Approved

## Problem

The YAML subagent loader hardcodes model strings in YAML files. Students can change models by editing YAML, but there's no way to override models at runtime without modifying config files. This makes it awkward to test the same pipeline with different providers or switch models across environments (dev/staging/prod).

## Design

### Loader change

Add env var override logic to `load_subagents()` in `loader.py`. After reading the model from YAML, check for an environment variable named `{NAME}_MODEL` where NAME is the subagent name uppercased with hyphens replaced by underscores.

**Precedence (highest wins):**

1. Environment variable (`RESEARCHER_MODEL`, `WRITER_MODEL`, etc.)
2. YAML `model:` field
3. No model set — subagent inherits the main agent's model

**Convention:** subagent name `researcher` checks `RESEARCHER_MODEL`, `fact-checker` checks `FACT_CHECKER_MODEL`.

**Code addition (~3 lines in the existing loader):**

```python
# ENV var override: RESEARCHER_MODEL, WRITER_MODEL, etc.
env_key = f"{name.upper().replace('-', '_')}_MODEL"
model = os.environ.get(env_key, spec.get("model"))
if model:
    subagent["model"] = model
```

### Module content changes

1. **Exercise 2 loader code** — add the override with a clear comment
2. **New section after Exercise 4** — explain the env var override pattern:
   - Why it matters (same YAML across environments, no file edits to swap models)
   - Concrete usage: `RESEARCHER_MODEL=openai:llama-scout-17b uv run demo.py`
   - Precedence table

### What stays unchanged

- YAML files keep hardcoded model strings (they're the defaults)
- `demo.py` and `content_pipeline.py` unchanged
- No new files created
