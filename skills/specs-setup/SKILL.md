---
name: specs-setup
description: "Initialize the spec-driven project methodology. Use when: no specs/ folder exists; critical files like PRD.md, Vision.md, or Architecture/ are missing; setting up a new project for structured requirements and ticket management. Triggers on: 'setup specs', 'initialize specs', 'create PRD', 'start project methodology', 'missing specs', 'init specs', 'no specs folder'."
---

# Specs Setup

Initialize the spec-driven methodology for a project. Run this when `specs/` doesn't exist or is missing critical files.

## Skill Dependencies

This skill is part of a set of skills designed to work together:

- **spec-driven** — Core rules and high-level document map
- **specs-setup** (this skill) — Initialize `specs/` for a new project
- **specs-tickets** — Create and execute tickets through their lifecycle
- **specs-review** — Audit specs health, consistency, and drift
- **specs-finish-ticket** — Review implemented tickets before closure

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the core rules. Load the [methodology reference](../spec-driven/references/methodology.md) for detailed document guidance and the [templates](../spec-driven/references/templates.md) when creating documents.

## Prerequisites

Before setting up specs, check if the project has **coding standards** defined:

- `.github/copilot-instructions.md` or `.github/instructions/*.instructions.md`
- `CLAUDE.md`
- or equivalent

If no coding standards exist, **prompt the user to create them before proceeding.** Specs define WHAT to build; coding standards define HOW to build it. Both are needed before any implementation work begins.

## Procedure

### 1. Assess Current State

Check which of these exist:

- [ ] `specs/` directory
- [ ] `specs/README.md`
- [ ] `specs/Vision.md`
- [ ] `specs/PRD.md`
- [ ] `specs/Architecture/` directory
- [ ] `specs/Architecture/README.md`
- [ ] `specs/Architecture/data-model.md` (optional)
- [ ] `specs/Glossary.md`
- [ ] `specs/Changelog.md`
- [ ] `specs/decisions/` directory
- [ ] `specs/tickets/` directory

Report what's missing and confirm with the user before creating anything.

### 2. Create Missing Structure

Create any missing directories and files using the templates from [templates.md](../spec-driven/references/templates.md).

Create in this order:

1. `specs/` directory
2. `specs/decisions/` directory (add a `.gitkeep` if empty)
3. `specs/tickets/` directory (add a `.gitkeep` if empty)
4. `specs/Architecture/` directory
5. `specs/Vision.md`
6. `specs/PRD.md`
7. `specs/Architecture/README.md`
8. `specs/Glossary.md`
9. `specs/Changelog.md`
10. `specs/README.md` (last, because it links to everything above)

Do **not** create optional architecture sub-documents by default. Decide whether `specs/Architecture/data-model.md` or other topic-specific docs are needed during architecture setup.

### 3. Populate Vision.md

Interview the user to fill in the vision. Ask about:

1. **Vision statement**: What is this project? Why does it exist? What future are we building toward?
2. **Problem statement**: What problem does it solve? Who feels this pain? What is the impact?
3. **Target audience**: Who are the primary users or personas?
4. **Success metrics**: How will we know the project is succeeding?
5. **Milestones**: What major milestones matter, and roughly when?

Write `Vision.md` based on the user's answers. **Present it for review and confirmation.**

If the project has existing documentation or a README, use it as input — but always confirm with the user rather than assuming.

### 4. Populate PRD.md

Interview the user to fill in the PRD. Ask about:

1. **Functional requirements**: What are the key things the system must do?
2. **Non-functional requirements**: Performance, security, scalability, accessibility needs?
3. **Scope**: What's explicitly in scope? What's explicitly out of scope?
4. **Assumptions & constraints**: What are we assuming? What limits us?

Write `PRD.md` based on the user's answers. **Present it for review and confirmation.**

### 5. Populate Architecture

If the project has **existing code**, analyze it and draft the architecture documentation:

1. **System overview**: What does the system do at a high level?
2. **Key components**: What are the major parts and their responsibilities?
3. **Technology stack**: What technologies are used and why?
4. **Key constraints**: What are the important architectural constraints and trade-offs?

If the project is **new** with no code yet, work with the user to define the target architecture.

**Present `Architecture/README.md` for review and confirmation.**

Remember: keep it high-level. The architecture entry point should give someone a clear mental model of the system in under 5 minutes of reading. Split into sub-documents only when a section exceeds ~200 lines.

If the project has any of the following, strongly consider creating optional architecture sub-documents now:

- non-trivial domain entities with identity or lifecycle rules
- signals, events, APIs, or shared structs crossing module or package boundaries
- persisted read models or storage formats that differ from canonical in-memory shapes
- compatibility, migration, or cutover concerns around data shape

Use them like this:

- `specs/Architecture/data-model.md` — canonical entities, identity, relationships, state transitions, invariants
- other topic-specific architecture docs — boundary payloads, owners, producers, consumers, canonical shape, transport or persistence format, and compatibility policy where those concerns need long-lived documentation

For boundary-oriented docs, explicitly distinguish:

- the canonical in-memory or conceptual shape
- the transport or wire format
- the persistence or stored representation

If those differ, document the difference rather than collapsing them into one vague "schema".

### 6. Populate Glossary

Scan `Vision.md`, `PRD.md`, and `Architecture/README.md` for domain-specific terms. Draft definitions and **ask the user to confirm them.** Even a small initial glossary (5-10 terms) is valuable — it can grow over time.

### 7. Create Instructions File

Create a `.github/instructions/specs.instructions.md` file to ensure agents automatically load the spec-driven methodology when working with specs:

```markdown
---
applyTo: "specs/**"
---

This project uses the spec-driven methodology. Load the `spec-driven` skill before making any changes to files in the specs/ folder.
```

If the `.github/instructions/` directory doesn't exist, create it.

### 8. Finalize README

Update `specs/README.md` with:

- the project name and one-line description
- current status such as "Setting up" or "No active tickets"
- working navigation links to all created documents
- links to `Architecture/data-model.md` and any other architecture sub-documents if they were created

### 9. Suggest Commit

Suggest the user commits the initial specs:

```text
docs: initialize spec-driven methodology
```

## Incremental Setup

If `specs/` already exists but is incomplete, only create the missing pieces. Do not overwrite existing documents — they may contain work that shouldn't be lost. Instead, flag any inconsistencies or gaps and let the user decide how to resolve them.
