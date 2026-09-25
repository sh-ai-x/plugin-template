# Guidelines

- Prefer a small skill with clear triggers over a broad instruction file.
- Keep manifest metadata, README instructions, and validation checks in sync.
- Make examples runnable without credentials or external sibling repositories.
- Put policy in `rules/`, reusable behavior in `skills/` or `scripts/`, and lifecycle wiring in `hooks/`.
- Verify generated output from a clean temporary destination before publishing a template change.
