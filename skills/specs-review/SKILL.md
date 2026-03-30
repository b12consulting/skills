---
name: specs-review
description: "Review the health of a spec-driven project. Use when: checking if specs are up to date; detecting drift between code and specs; finding stale or incomplete tickets; auditing consistency across Vision, PRD, Goals, Architecture, and tickets. Triggers on: 'specs review', 'spec health', 'check specs', 'audit specs', 'are specs up to date', 'drift check', 'stale tickets', 'spec consistency'."
---

# Specs Review

Audit the health and consistency of a project's spec-driven documentation.

## Skill Dependencies

This skill is part of a set of skills designed to work together:

- **spec-driven** — Methodology reference (structure, formats, rules)
- **specs-setup** — Initialize `specs/` for a new project
- **specs-tickets** — Create and execute tickets through their lifecycle
- **specs-review** (this skill) — Audit specs health and consistency

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the full methodology reference.

## Procedure

### 1. Structural Completeness

Verify all required files exist:

- [ ] `specs/README.md`
- [ ] `specs/Vision.md`
- [ ] `specs/PRD.md`
- [ ] `specs/Goals.md`
- [ ] `specs/Architecture/README.md`
- [ ] `specs/Glossary.md`
- [ ] `specs/Changelog.md`
- [ ] `specs/decisions/` directory
- [ ] `specs/tickets/` directory

Report any missing files. Suggest running `specs-setup` if critical files are absent.

### 2. Document Quality

For each project-level document, check:

| Document                 | Check                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `Vision.md`              | Has vision statement, problem statement, and target audience?                                                   |
| `PRD.md`                 | Has functional requirements, non-functional requirements, and scope? Are requirements numbered (FR-1, FR-2...)? |
| `Goals.md`               | Has measurable success metrics? Are milestones defined with target dates?                                       |
| `Architecture/README.md` | Has system overview, key components, and tech stack? Links to sub-documents if they exist?                      |
| `Glossary.md`            | Has at least a few terms? Are terms used consistently in other documents?                                       |
| `Changelog.md`           | Is up to date with recent completed tickets?                                                                    |
| `README.md`              | Does the active tickets table match actual ticket statuses? Is the "last updated" date recent?                  |

Flag documents that are empty templates (never filled in) or have placeholder content.

### 3. Ticket Health

Scan all ticket folders in `specs/tickets/` and check each one:

**Frontmatter integrity:**

- Does every ticket have a `README.md` with valid frontmatter (`id`, `title`, `status`, `created`, `updated`)?
- Are status values valid (`research`, `specifying`, `open-questions`, `planned`, `in-progress`, `done`, `archived`)?

**Lifecycle consistency:**

- Does a ticket marked `in-progress` have a `Tasks.md` with at least some unchecked items?
- Does a ticket marked `done` have all acceptance criteria in `Spec.md` checked off?
- Does a ticket marked `planned` have both `Spec.md` and `Plan.md`?
- Does a ticket marked `archived` have a documented reason in its README.md body?

**Stale tickets:**

- Any ticket with status `in-progress` or `research` whose `updated` date is more than 2 weeks old? Flag as potentially stale.
- Any ticket with status `open-questions` that has been waiting for decisions? Flag with the pending questions.

**Orphaned files:**

- Any ticket folder missing a `README.md`?
- Any `Decisions.md` with items still in the Open section for a ticket that has moved past `specifying`?

Report findings as a table:

| #   | Title | Status      | Issues                              |
| --- | ----- | ----------- | ----------------------------------- |
| 001 | ...   | in-progress | Stale (last updated 3 weeks ago)    |
| 002 | ...   | done        | Acceptance criteria not all checked |

### 4. Cross-Reference Consistency

Check that documents reference each other correctly:

- **README.md dashboard vs. reality**: Do the "Active Tickets" and "Recently Completed" tables match actual ticket statuses?
- **ADR references**: Are ADRs referenced in the tickets that triggered them? Are ADR-modified documents (Vision, PRD, Goals, Architecture) updated accordingly?
- **Glossary usage**: Scan Vision, PRD, and Architecture for domain terms. Are they defined in the Glossary? Are there Glossary terms that appear unused?
- **Architecture sub-documents**: If `Architecture/README.md` links to sub-documents, do those files exist?

### 5. Drift Detection

Compare specs against the codebase:

- Does the tech stack in `Architecture/README.md` match the actual dependencies (check `package.json`, `pyproject.toml`, `Cargo.toml`, etc.)?
- Do the key components described in Architecture match the actual project structure?
- Are there functional requirements in PRD.md that don't correspond to any ticket (planned or completed)?

This step requires codebase analysis. Flag potential drift but note that **confirmation with the user is needed** — apparent drift may be intentional and just not yet documented.

### 6. Report

Summarize findings in three categories:

**Critical** — Blocks correct agent behavior:

- Missing ground truth documents (Vision, PRD, Architecture)
- Tickets with invalid or missing frontmatter
- Conflicts between specs and code that could lead to wrong implementation

**Warning** — Should be addressed soon:

- Stale tickets
- Unresolved open questions
- README dashboard out of sync
- Empty or placeholder documents

**Suggestion** — Improvements for completeness:

- Missing Glossary terms
- Tickets without Journal.md that had complex processes
- Architecture that could benefit from sub-documents

### 7. Propose Actions

For each finding, propose a concrete action:

- "Create ADR to document the React-to-Vue migration that happened in ticket 005"
- "Update specs/README.md — tickets 003 and 004 are marked done but still in Active Tickets"
- "Ticket 007 has been in-progress for 3 weeks with no updates — ask the owner for status"
- "Add 'workspace' and 'campaign' to the Glossary — used in PRD but not defined"

Ask the user which actions to take. Execute approved actions immediately.
