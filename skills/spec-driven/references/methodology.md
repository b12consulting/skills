# Spec-Driven Methodology Reference

Detailed operational guidance for the spec-driven skill family.

## Modeling Layers

When a project has non-trivial entities, cross-module payloads, APIs, events, signals, or persisted read models, keep these layers explicit and separate:

- **Domain model** — the conceptual model: entities, identity rules, relationships, state transitions, and invariants
- **Boundary contracts** — the boundary model: signals, events, API payloads, public structs, renderer inputs, tool outputs, and read-model shapes shared across module or package boundaries
- **Serialization & persistence** — how a canonical shape is stored or transported; this is not the same thing as the canonical in-memory or conceptual model

Rules:

- Document stable domain concepts in `Architecture/data-model.md` when the project has meaningful identity, lifecycle, or invariant rules.
- Document stable boundary contracts in the relevant architecture docs that own them when producers and consumers must stay aligned across modules, packages, services, or persistence boundaries.
- Do not treat a wire format or persistence encoding as the canonical model unless the project explicitly decides that it is.
- Do not leave long-lived contract definitions only in a ticket if they matter across more than one implementation pass.

## Folder Structure

```text
specs/
├── README.md                    # Project dashboard and navigation
├── Vision.md                    # WHY + success frame
├── PRD.md                       # WHAT — functional and non-functional requirements
├── Glossary.md                  # Domain vocabulary
├── Changelog.md                 # What shipped and when
├── Architecture/                # Architecture documentation (always a folder)
│   ├── README.md                # Architecture overview (entry point)
│   ├── data-model.md            # Optional: canonical entities, identity, invariants
│   └── <topic>.md               # Sub-documents split by concern
├── decisions/                   # Architecture Decision Records
│   ├── ADR-001-<title>.md
│   └── ...
└── tickets/                     # Work items
    └── <NNN>-<slug>/
        ├── Research.md          # Investigation findings (optional)
        ├── Spec.md              # Ticket metadata, summary, requirements, status
        ├── Plan.md              # Required approach, sequencing, and checklist
        ├── Decisions.md         # Open questions and resolved decisions (optional)
        └── Findings.md          # Curated durable discoveries (optional)
```

## Project-Level Documents

| Document                 | Purpose                                                                                                        | Required     |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- | ------------ |
| `README.md`              | Project dashboard. Status, active tickets, recent ADRs, navigation. **Read this first in every conversation.** | Always     |
| `Vision.md`              | Vision statement, problem statement, target audience, success metrics, and milestones.                        | Always       |
| `PRD.md`                 | Functional requirements, non-functional requirements, scope, assumptions, and constraints.                    | Always       |
| `Architecture/README.md` | System overview, components, tech stack, constraints. Links to sub-documents.                                | Always       |
| `Glossary.md`            | Domain terms and definitions. Keeps language consistent across all documents.                                 | Always       |
| `Changelog.md`           | Shipped changes in reverse chronological order.                                                               | Always       |
| `ADR-NNN-<title>.md`     | Records a decision that changed Vision, PRD, or Architecture.                                                | Per decision |

## Ticket-Level Documents

| Document       | Purpose                                                                                                                        | Required                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| `Research.md`  | Investigation findings, options considered, feasibility.                                                                      | When research was done           |
| `Spec.md`      | The canonical ticket record: frontmatter, summary, user stories, acceptance criteria, scope boundaries, and status.          | Per ticket                       |
| `Plan.md`      | The required execution document: implementation approach, sequencing, checklist, verification, and risks.                    | Per ticket                       |
| `Decisions.md` | Questions raised and decisions made. Open questions at the top, resolved decisions at the bottom.                             | When decisions arise             |
| `Findings.md`  | Curated implementation discoveries: assumptions, spec clarifications, frictions, workarounds, follow-up candidates, residual risks, and test gaps. | When non-trivial findings emerge |

For complete document templates, see [templates.md](./templates.md).

## Architecture Folder Guidelines

The `Architecture/` folder starts with a single `README.md` as the entry point. Keep architecture documentation high-level and navigable:

- **Start with README.md.** It alone is sufficient for most projects.
- **Split when a section exceeds ~200 lines** or covers a distinct concern such as data model, boundary ownership, or infrastructure.
- **New files go alongside README.md** and are linked from it.
- **Never nest deeper than one level** within `Architecture/`. If you need sub-folders, the architecture docs are too detailed — summarize and elevate.
- **Keep each file focused** on one architectural concern.

Recommended sub-documents when the project warrants them:

- `Architecture/data-model.md` — use when domain entities, identity, lifecycle, or invariants span multiple modules or tickets
- other topic-specific architecture docs — use when signals, events, APIs, shared structs, renderer inputs, or persisted boundary shapes must stay aligned across producers and consumers

## Ticket Naming

Tickets use sequential numbering with a descriptive slug:

```text
<NNN>-<slug>/
```

- `NNN`: Three-digit sequential number, zero-padded (`001`, `002`, ...)
- `slug`: Lowercase, hyphen-separated description such as `user-auth` or `search-api`
- The Jira issue key is stored in the ticket's `Spec.md` frontmatter, **not** in the folder name
- To determine the next number, scan existing ticket folders and increment the highest by one

## Ticket Spec Frontmatter

Every ticket has a `Spec.md` with this frontmatter:

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

| Status           | Meaning                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `research`       | Investigating the problem space                                                                                                 |
| `specifying`     | Writing or refining the spec                                                                                                    |
| `open-questions` | Blocked on decisions the user must make                                                                                         |
| `planned`        | `Plan.md` exists, includes the checklist, and is ready for implementation                                                       |
| `in-progress`    | Implementation underway or ready for independent finish review                                                                  |
| `done`           | All acceptance criteria met, finish review completed, and work accepted                                                         |
| `archived`       | Ticket closed without completion. **The reason for archival must be documented clearly in the `Spec.md` body.**                |

## Ticket Lifecycle

```text
Research → Specify → Plan → Implement → Finish Review → Done
```

| Phase         | Files Produced / Updated                                   | Requires User Validation                 |
| ------------- | ---------------------------------------------------------- | ---------------------------------------- |
| Research      | `Research.md`                                              | No (user may review)                     |
| Specify       | `Spec.md`, `Decisions.md`                                  | **Yes — user must validate `Spec.md`**   |
| Plan          | `Plan.md`                                                  | **Yes — user must confirm `Plan.md`**    |
| Implement     | Code, tests, `Plan.md`, `Findings.md`                      | Per task as appropriate                  |
| Finish Review | Review notes, `Findings.md`, any factual spec drift corrections | **Yes — user confirms closeout direction** |
| Done          | Ticket `Spec.md` status, project `README.md`, `Changelog.md` | **Yes — user confirms completion**       |

**Any participant (human or agent) can execute any phase.** The lifecycle defines the order, not who does what.

`Finish Review` is usually performed with the `specs-finish-ticket` skill in a fresh conversation. There is no dedicated status for it; tickets usually remain `in-progress` until the review passes.

## Findings Guidance

`Findings.md` is not a scratchpad and not a second plan.

Use it for durable discoveries that matter after the implementation session ends, such as:

- assumptions the ticket relied on
- underspecified behavior that had to be clarified during implementation
- frictions encountered and temporary workarounds used to stay in scope
- follow-up improvements that deserve a new ticket
- residual risks or meaningful test gaps

Rules:

- Update `Findings.md` progressively during implementation, not only at the end.
- Revisit it during finish review.
- Keep entries curated and durable rather than chronological.
- Every finding must end with a clear disposition such as `Addressed here`, `Follow-up needed`, or `Accepted for now`.
- If a follow-up is required but out of scope for the current ticket, record it in `Findings.md` and ask the user whether to create a new ticket.

## ADR Trigger Rules

Create an Architecture Decision Record when:

- a project-level requirement or success measure in `Vision.md` or `PRD.md` changes
- the architecture is modified in a way that future contributors need to understand
- a ticket implementation reveals that stable specs must change
- canonical entity identity, lifecycle, or invariant rules change
- a public boundary contract changes, such as an API payload, event or signal shape, public struct, renderer input, or persisted read-model contract
- the project changes how a canonical shape is serialized, persisted, versioned, migrated, or intentionally cut over

## ADR Format

```markdown
# ADR-NNN: <Title>

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Date**: YYYY-MM-DD
**Ticket**: <link to related ticket, if any>

## Affected Documents

- Vision / PRD / Architecture files changed by this decision

## Context

What situation or problem prompted this decision?

## Decision

What did we decide?

## Compatibility / Migration

What changes at the boundary? Is there a cutover, compatibility window, migration, or intentional break?

## Consequences

What are the trade-offs? What becomes easier? What becomes harder?
```
