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

### python-best-practices

Python coding best practices for data and consulting projects. Covers code style, type hints, error handling, project structure, data handling, testing, logging, and security.

**Use when:**
- Writing new Python scripts or modules
- Reviewing or refactoring existing Python code
- Building data pipelines or ETL workflows
- Developing APIs or CLI tools

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
