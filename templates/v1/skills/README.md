# Skills and workflows

Create one directory per workflow under `skills/`. Each directory must contain a `SKILL.md` with
`name`, `description`, and the workflow instructions. Put supporting scripts, references, templates,
and assets next to that file.

Keep the skill name host-neutral. Claude Code exposes it with the plugin namespace (for example
`/__PLUGIN_NAME__:example-workflow`); Codex and agy discover the same `skills/<name>/SKILL.md`
without requiring a second copy of the instructions.
