# skills

A collection of reusable AI agent skills for Yuma projects. Skills follow the [skills.sh](https://skills.sh/) open format and can be installed into any compatible AI coding agent (Claude, Cursor, Copilot, etc.).

## Installation

Install all skills from this repository:

```bash
npx skills add b12consulting/skills
```

Install a specific skill:

```bash
npx skills add b12consulting/skills --skill python-best-practices
```

Preview available skills before installing:

```bash
npx skills add b12consulting/skills --list
```

## Available Skills

See the `skills/` directory for a full list of available skills, each with its own `SKILL.md` documentation.

## Skill Structure

Each skill is a folder under `skills/` containing:

- `SKILL.md` — Instructions and guidelines for the agent (required)
- `scripts/` — Helper scripts (optional)
- `references/` — Supporting documentation (optional)

## Contributing

To add a new skill:

1. Create a new folder under `skills/` using kebab-case (e.g. `skills/my-new-skill/`)
2. Add a `SKILL.md` file with the following frontmatter:

```markdown
---
name: my-new-skill
description: A clear description of what this skill does and when to use it.
---

# My New Skill

...
```

3. The `name` field must match the directory name exactly.

## License

MIT
