# Workflows

Workflows are human-readable runbooks that explain how skills, hooks, MCP, and repository rules fit
together. Keep reusable execution instructions in `skills/<name>/SKILL.md`; use this directory for
multi-step scenarios and review checklists.

The default lifecycle is:

`bootstrap → plan → build → verify → review → ship`

Each workflow should state its inputs, expected artifacts, validation command, and handoff point.
