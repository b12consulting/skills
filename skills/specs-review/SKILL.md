---
name: specs-review
description: "Review the health of a spec-driven project. Use when: checking if specs are up to date; detecting drift between code and specs; finding stale or incomplete tickets; auditing consistency across Vision, PRD, Architecture, and tickets. Triggers on: 'specs review', 'spec health', 'check specs', 'audit specs', 'are specs up to date', 'drift check', 'stale tickets', 'spec consistency'."
---

# Specs Review

Audit the health and consistency of a project's spec-driven documentation.

## Skill Dependencies

This skill is part of a set of skills designed to work together:

- **spec-driven** — Core rules and high-level document map
- **specs-setup** — Initialize `specs/` for a new project
- **specs-tickets** — Create and execute tickets through their lifecycle
- **specs-finish-ticket** — Review implemented tickets before closure
- **specs-review** (this skill) — Audit specs health and consistency

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the core rules. Load the [methodology reference](../spec-driven/references/methodology.md) when you need detailed lifecycle, document, ADR, or Findings guidance.

## Procedure

### 1. Structural Completeness

Verify all required files exist:

- [ ] `specs/README.md`
- [ ] `specs/Vision.md`
- [ ] `specs/PRD.md`
- [ ] `specs/Architecture/README.md`
- [ ] `specs/Glossary.md`
- [ ] `specs/Changelog.md`
- [ ] `specs/decisions/` directory
- [ ] `specs/tickets/` directory

Report any missing files. Suggest running `specs-setup` if critical files are absent.

If the project is event-driven, API-heavy, multi-package, or persistence-heavy, also check whether optional architecture sub-documents such as `specs/Architecture/data-model.md` or other topic-specific architecture docs would improve clarity.

### 2. Document Quality

For each project-level document, check:

| Document                 | Check                                                                                                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `Vision.md`              | Has vision statement, problem statement, target audience, success metrics, and milestones?                            |
| `PRD.md`                 | Has functional requirements, non-functional requirements, and scope? Are requirements numbered (`FR-1`, `FR-2`, ...)? |
| `Architecture/README.md` | Has system overview, key components, and tech stack? Links to sub-documents if they exist?                            |
| `Glossary.md`            | Has at least a few terms? Are terms used consistently in other documents?                                             |
| `Changelog.md`           | Is it up to date with recent completed tickets?                                                                       |
| `README.md`              | Does the active tickets table match actual ticket statuses? Is the last-updated date recent?                          |

Flag documents that are empty templates or still contain placeholder content.

If these optional architecture documents exist, also check:

| Document                     | Check                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `Architecture/data-model.md` | Are canonical entities, identity rules, relationships, state transitions, and invariants documented clearly? |

### 3. Cross-Reference Consistency

Check that documents reference each other correctly:

- **README dashboard vs. reality**: Do the Active Tickets and Recently Completed tables match ticket statuses from `Spec.md` frontmatter?
- **Glossary usage**: Scan `Vision.md`, `PRD.md`, and architecture docs for domain terms. Are they defined in the Glossary?
- **Architecture sub-documents**: If `Architecture/README.md` links to sub-documents, do those files exist?

### 4. Drift Detection

Compare specs against the codebase:

- Does the tech stack in `Architecture/README.md` match the actual dependencies?
- Do the key components described in architecture docs match the actual project structure?
- Are there functional requirements in `PRD.md` that do not correspond to any ticket, planned or completed?
- Where architecture docs define long-lived boundary contracts, do those contracts still match the code?
- Where `data-model.md` exists, do documented identity rules and invariants still match the code and current architecture?

This step requires codebase analysis. Flag potential drift but note that **confirmation with the user is needed** — apparent drift may be intentional and just not yet documented.

### 5. Report

Summarize findings in three categories:

**Critical** — Blocks correct agent behavior:

- missing ground truth documents such as `Vision.md`, `PRD.md`, or `Architecture/README.md`
- tickets with invalid or missing frontmatter in `Spec.md`
- tickets missing required `Plan.md` for their lifecycle state
- conflicts between specs and code that could lead to wrong implementation

**Warning** — Should be addressed soon:

- stale tickets
- unresolved open questions
- README dashboard out of sync
- empty or placeholder documents

**Suggestion** — Improvements for completeness:

- missing Glossary terms
- tickets without `Findings.md` that clearly involved durable assumptions, frictions, or follow-up candidates
- architecture that could benefit from sub-documents
- missing `data-model.md` or other architecture docs for non-trivial boundary contracts or persistence shapes

### 6. Propose Actions

For each finding, propose a concrete action:

- "Create ADR to document the React-to-Vue migration that happened in ticket 005"
- "Update `specs/README.md` — tickets 003 and 004 are marked done but still in Active Tickets"
- "Ticket 007 has been in-progress for 3 weeks with no updates — ask the owner for status"
- "Add 'workspace' and 'campaign' to the Glossary — used in PRD but not defined"

Ask the user which actions to take. Execute approved actions immediately.
