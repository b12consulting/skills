---
name: spec-driven
description: "Spec-driven project methodology reference. Use when a project has a specs/ folder for managing product requirements, vision, goals, architecture, decision records (ADR), glossary, changelog, and ticket-based work tracking. Loaded when: working on a project with specs/; reading or updating PRD, vision, goals, architecture, or glossary; detecting drift between code and specs; reviewing project methodology or document formats. Triggers on: 'specs', 'PRD', 'vision', 'goals', 'architecture', 'ADR', 'decision record', 'glossary', 'changelog', 'ticket', 'project methodology', 'ground truth'."
---

# Spec-Driven Development

A methodology for collaborative human-agent project management where all requirements, decisions, and work are documented in a `specs/` folder that serves as the project's single source of truth.

## Skill Dependencies

This skill is part of a set of four skills designed to work together:

| Skill                        | Purpose                                            |
| ---------------------------- | -------------------------------------------------- |
| **spec-driven** (this skill) | Methodology reference — structure, formats, rules  |
| **specs-setup**              | Initialize `specs/` for a new project              |
| **specs-tickets**            | Create and execute tickets through their lifecycle |
| **specs-review**             | Audit specs health, consistency, and drift         |

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

## Core Principles

1. **Specs are the ground truth.** When code and specs disagree, the specs win. Either update the code or create an ADR to change the specs.
2. **Decisions are recorded.** Every change to Vision, PRD, Goals, or Architecture is documented with an Architecture Decision Record.
3. **Work is traceable.** Every ticket captures research, requirements, plans, and tasks so future contributors understand not just WHAT was built but WHY.
4. **Humans decide, agents execute and propose.** Agents can research, draft specs, plan, and implement — but key decisions (scope, architecture, trade-offs) require human confirmation.
5. **Progressive documentation.** Create documents when needed, not proactively. A small bug fix doesn't need Research.md.

## Truth Hierarchy

When documents conflict, the higher-level document takes precedence:

```
Vision.md > PRD.md / Goals.md > Architecture/ > Ticket Spec.md > Ticket Plan.md > Ticket Tasks.md
```

Conflicts must be resolved by either:

- Creating an ADR and updating the higher-level document
- Creating a ticket to fix the lower-level document or code

## Folder Structure

```
specs/
├── README.md                    # Project dashboard and navigation
├── Vision.md                    # WHY — vision, problem statement, target audience
├── PRD.md                       # WHAT — functional and non-functional requirements
├── Goals.md                     # HOW WE MEASURE — success metrics, KPIs, milestones
├── Glossary.md                  # Domain vocabulary
├── Changelog.md                 # What shipped and when
├── Architecture/                # Architecture documentation (always a folder)
│   ├── README.md                # Architecture overview (entry point)
│   └── <topic>.md               # Sub-documents split by concern
├── decisions/                   # Architecture Decision Records
│   ├── ADR-001-<title>.md
│   └── ...
└── tickets/                     # Work items
    └── <NNN>-<slug>/            # e.g., 001-user-auth/
        ├── README.md            # Ticket metadata and summary
        ├── Research.md          # Investigation findings (optional)
        ├── Spec.md              # Requirements and acceptance criteria
        ├── Plan.md              # Implementation approach (optional)
        ├── Tasks.md             # Task checklist
        ├── Dependencies.md      # Cross-ticket dependencies (optional)
        ├── Decisions.md         # Open questions and resolved decisions (optional)
        └── Journal.md           # Process record (optional)
```

## Project-Level Documents

| Document                 | Purpose                                                                                                                   | Required     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `README.md`              | Project dashboard. Status, active tickets, recent ADRs, navigation. **Read this first in every conversation.**            | Always       |
| `Vision.md`              | **WHY** — Vision statement, problem statement, target audience and personas. Rarely changes.                              | Always       |
| `PRD.md`                 | **WHAT** — Functional requirements, non-functional requirements, scope, assumptions & constraints. Traditional PRD scope. | Always       |
| `Goals.md`               | **HOW WE MEASURE** — Success metrics, KPIs, milestones. Reviewed periodically.                                            | Always       |
| `Architecture/README.md` | **HOW IT'S BUILT** — System overview, components, tech stack, constraints. Links to sub-documents.                        | Always       |
| `Glossary.md`            | Domain terms and definitions. Keeps language consistent across all documents.                                             | Always       |
| `Changelog.md`           | Shipped changes in reverse chronological order.                                                                           | Always       |
| `ADR-NNN-<title>.md`     | Records a decision that changed Vision, PRD, Goals, or Architecture.                                                      | Per decision |

## Ticket-Level Documents

| Document          | Purpose                                                                                                                                                      | Required                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| `README.md`       | Ticket metadata (status, owner, dates, Jira link) and one-paragraph summary.                                                                                 | Per ticket               |
| `Research.md`     | Investigation findings, options considered, feasibility.                                                                                                     | When research was done   |
| `Spec.md`         | The contract: user stories, acceptance criteria, scope boundaries.                                                                                           | Per ticket               |
| `Plan.md`         | Implementation strategy — high-level approach, key design decisions, risks.                                                                                  | At planning phase        |
| `Tasks.md`        | Concrete task breakdown with checkboxes.                                                                                                                     | At task definition phase |
| `Dependencies.md` | What this ticket blocks or is blocked by.                                                                                                                    | When dependencies exist  |
| `Decisions.md`    | Questions raised and decisions made. Open questions at the top, resolved decisions at the bottom. Becomes a decision record once all questions are answered. | When decisions arise     |
| `Journal.md`      | Chronological record of key decisions, pivots, and process. Not a chat transcript.                                                                           | For non-trivial tickets  |

For complete document templates, see [templates.md](./references/templates.md).

## Architecture Folder Guidelines

The `Architecture/` folder starts with a single `README.md` as the entry point. Keep architecture documentation high-level and navigable:

- **Start with README.md.** It alone is sufficient for most projects.
- **Split when a section exceeds ~200 lines** or covers a distinct concern (data model, API contracts, infrastructure).
- **New files go alongside README.md** and are linked from it (e.g., `data-model.md`, `api-contracts.md`).
- **Never nest deeper than one level** within `Architecture/`. If you need sub-folders, the architecture docs are too detailed — summarize and elevate.
- **Keep each file focused** on one architectural concern.

## Ticket Naming

Tickets use sequential numbering with a descriptive slug:

```
<NNN>-<slug>/
```

- `NNN`: Three-digit sequential number, zero-padded (001, 002, ...).
- `slug`: Lowercase, hyphen-separated description (e.g., `user-auth`, `search-api`).
- The Jira issue key is stored in the ticket's `README.md` frontmatter, **not** in the folder name.
- To determine the next number, scan existing ticket folders and increment the highest by one.

## Ticket README Frontmatter

Every ticket has a `README.md` with this frontmatter:

```yaml
---
id: "<NNN>"
title: "<Descriptive title>"
status: research | specifying | open-questions | planned | in-progress | done | archived
jira: "" # Optional: Jira issue key (e.g., YAI-042)
owner: "" # Who is responsible
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Status values:**

| Status           | Meaning                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `research`       | Investigating the problem space                                                                                                                        |
| `specifying`     | Writing or refining the spec                                                                                                                           |
| `open-questions` | Blocked on decisions the user must make                                                                                                                |
| `planned`        | Plan and/or tasks defined, ready for implementation                                                                                                    |
| `in-progress`    | Implementation underway                                                                                                                                |
| `done`           | All acceptance criteria met, work complete                                                                                                             |
| `archived`       | Ticket closed without completion. **The reason for archival (superseded, cancelled, etc.) must be documented clearly in the ticket's README.md body.** |

## Ticket Lifecycle

```
Research → Specify → Plan → Define Tasks → Implement → Done
```

| Phase        | Files Produced                         | Requires User Validation              |
| ------------ | -------------------------------------- | ------------------------------------- |
| Research     | Research.md                            | No (user may review)                  |
| Specify      | Spec.md, Decisions.md, Dependencies.md | **Yes — user must validate Spec.md**  |
| Plan         | Plan.md                                | **Yes — user must confirm Plan.md**   |
| Define Tasks | Tasks.md                               | **Yes — user must validate Tasks.md** |
| Implement    | Code + tests                           | Per task as appropriate               |
| Done         | Update README.md status, Changelog.md  | **Yes — user confirms completion**    |

**Any participant (human or agent) can execute any phase.** The lifecycle defines the _order_, not who does what. The user may write the spec themselves, or the agent may do the research. Flexibility is expected.

## Drift Detection

At the start of every conversation on a project with `specs/`:

1. Read `specs/README.md`, then `Vision.md`, `PRD.md`, `Goals.md`, and `Architecture/README.md`.
2. If the current code or task contradicts these documents, **alert the user immediately**.
3. Resolution options:
   - Create an ADR to update the specs (if the code is right and specs are outdated)
   - Create a ticket to fix the code (if the specs are right and code has drifted)

## ADR Trigger Rules

Create an Architecture Decision Record when:

- A requirement in Vision.md, PRD.md, or Goals.md changes
- The architecture is modified (new component, technology change, pattern shift)
- A ticket implementation reveals that specs need updating
- A significant decision is made that future contributors should understand

## ADR Format

```markdown
# ADR-NNN: <Title>

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Date**: YYYY-MM-DD
**Ticket**: <link to related ticket, if any>

## Context

What situation or problem prompted this decision?

## Decision

What did we decide?

## Consequences

What are the trade-offs? What becomes easier? What becomes harder?
```

## Operational Standards Check

If the project lacks coding standards (e.g., `.instructions.md`, `CLAUDE.md`, `copilot-instructions.md`), **prompt the user to create them before starting any implementation work.** Coding standards define HOW to build; specs define WHAT to build. Both are required.

Coding standards live in their respective configuration files — not in `specs/`.
