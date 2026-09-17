---
name: example-workflow
description: Use when a user asks for the workflow this plugin is meant to automate. Replace this description with the user goal, trigger conditions, and expected result.
---

# Example workflow

Replace this file with the first workflow skill for `__PLUGIN_NAME__`.

## When to use

- State the user goal that should activate this skill.
- State the input files, tools, or MCP servers it needs.
- State when the skill must not be used.

## Workflow

1. Inspect the relevant project state before making changes.
2. Run deterministic scripts from `scripts/` when a check can be automated.
3. Use MCP tools only for the external capability described by the skill.
4. Produce a concise result with evidence and the next action.

## Completion contract

- Report what changed and what was verified.
- Quote command exit codes when commands were run.
- Do not write credentials or machine-local state into the plugin directory.
