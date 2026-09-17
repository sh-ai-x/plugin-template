# Skill authoring

- Use one lowercase kebab-case directory per skill: `skills/<name>/SKILL.md`.
- Keep the `name` frontmatter equal to the directory name.
- Make `description` specific enough to express when the skill should activate.
- Use the optional `alpha` field to classify the skill as `state`, `enforcement`, or `analysis`.
- Keep names host-neutral; the plugin name supplies the namespace at presentation time.
- Keep references and scripts beside the skill so installed copies remain portable.
