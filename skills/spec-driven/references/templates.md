# Document Templates

Complete templates for every document in the spec-driven methodology.

---

## specs/README.md

```markdown
# <Project Name>

> <One-line project description>

## Status

| Metric | Value |
|--------|-------|
| Active tickets | 0 |
| Last updated | YYYY-MM-DD |

## Active Tickets

| # | Title | Status | Owner |
|---|-------|--------|-------|

## Recently Completed

| # | Title | Completed |
|---|-------|-----------|

## Recent Decisions

| ADR | Title | Date |
|-----|-------|------|

## Navigation

- [Vision](Vision.md)
- [PRD](PRD.md)
- [Architecture](Architecture/README.md)
- [Glossary](Glossary.md)
- [Changelog](Changelog.md)
- [Decisions](decisions/)
- [Tickets](tickets/)
```

---

## specs/Vision.md

```markdown
# Vision

## Vision Statement

What is this project and why does it exist? What future are we building toward?

## Problem Statement

What problem are we solving? Who experiences this problem and what is the impact?

## Target Audience

Who are the primary users? Describe personas if applicable.

| Persona | Description | Key Needs |
|---------|-------------|-----------|
| | | |

## Success Metrics

How do we measure success? Define quantitative and qualitative indicators.

| Metric | Target | How Measured |
|--------|--------|--------------|
| | | |

## Milestones

| Milestone | Description | Target Date | Status |
|-----------|-------------|-------------|--------|
| | | | |
```

---

## specs/PRD.md

```markdown
# Product Requirements Document

## Functional Requirements

### FR-1: <Requirement title>

<Description>

### FR-2: <Requirement title>

<Description>

## Non-Functional Requirements

### Performance

### Security

### Scalability

### Accessibility

## Scope

### In Scope

### Out of Scope

## Assumptions & Constraints
```

---

## specs/Architecture/README.md

```markdown
# Architecture

## System Overview

High-level description of the system and its purpose.

## Architecture Diagram

Describe or include a diagram of the system architecture.

## Key Components

| Component | Responsibility |
|-----------|---------------|
| | |

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| | | |

## Key Constraints & Trade-offs

Document important architectural constraints and the trade-offs made.

## Sub-documents

Link to detailed architecture documents as they are created:

_(none yet)_
```

---

## specs/Architecture/data-model.md

```markdown
# Data Model

## Purpose

What part of the domain does this model describe, and why does it need its own document?

## Canonical Entities

| Entity | Purpose | Identity | Lifecycle / States |
|--------|---------|----------|--------------------|
| | | | |

## Relationships

| Source | Relationship | Target | Notes |
|--------|--------------|--------|-------|
| | | | |

## Invariants

- <Invariant 1>
- <Invariant 2>

## State Transitions

| Entity | From | Event / Condition | To | Notes |
|--------|------|-------------------|----|-------|
| | | | | |

## Derived / Read Models

Describe any projections or read models derived from the canonical domain entities.

## Related Boundary Docs

Link to other architecture docs that expose these entities at system boundaries.
```

---

## specs/Glossary.md

```markdown
# Glossary

| Term | Definition |
|------|-----------|
| | |
```

---

## specs/Changelog.md

```markdown
# Changelog

All notable changes to this project are documented here. Entries are in reverse chronological order.

## [Unreleased]

### Added

### Changed

### Fixed

### Removed
```

---

## specs/decisions/ADR-NNN-\<title\>.md

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

---

## tickets/\<NNN\>-\<slug\>/Research.md

```markdown
# Research: <Title>

## Objective

What are we trying to learn or decide?

## Findings

### <Topic 1>

### <Topic 2>

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| | | |

## Recommendation

Based on findings, what do we recommend?

## References

- <links to relevant docs, articles, code>
```

---

## tickets/\<NNN\>-\<slug\>/Spec.md

```markdown
---
id: "<NNN>"
title: "<Descriptive title>"
status: research
owner: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Spec: <Title>

<One-paragraph summary of what this ticket covers and why.>

## User Stories

### US-1: <Story title> (Priority: P1)

**As a** <persona>, **I want** <action>, **so that** <benefit>.

**Independent test**: <How this story can be verified on its own>

### US-2: <Story title> (Priority: P2)

**As a** <persona>, **I want** <action>, **so that** <benefit>.

**Independent test**: <How this story can be verified on its own>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] <Criterion 3>

## Scope

### In Scope

### Out of Scope
```

---

## tickets/\<NNN\>-\<slug\>/Plan.md

```markdown
# Plan: <Title>

## Approach

Describe the implementation strategy at a high level.

## Key Design Decisions

Document important choices made during planning and their rationale.

## Dependencies And Sequencing

Document only the blockers or ordering constraints that materially affect execution.

## Data Model & Contract Impact

- Canonical entities or value objects introduced or changed
- Boundary contracts introduced or changed
- Transport / persistence / serialization implications
- Compatibility, migration, or cutover policy

## Implementation Checklist

Format: `- [ ] T001 [P] Description with file path`

- **T001, T002, ...** — sequential checklist item ID
- **[P]** — present only when the work can run in parallel with other incomplete items
- Include the exact file path to create or modify in the description
- Group the checklist by user-story priority when that improves execution clarity

### P1 — <Story title>

- [ ] T001 <Description with file path>
- [ ] T002 [P] <Description with file path>
- [ ] T003 <Description with file path>

### P2 — <Story title>

- [ ] T004 <Description with file path>
- [ ] T005 [P] <Description with file path>

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| | | | |

## Verification

List the tests or checks that prove the plan satisfies the spec.
```

---

## tickets/\<NNN\>-\<slug\>/Decisions.md

```markdown
# Decisions: <Title>

## Open

Questions that need a decision before work can proceed.

### Q1: <Question>

**Context**: <Why this matters>
**Options**:
1. <Option A> — <trade-offs>
2. <Option B> — <trade-offs>

**Suggested**: <Agent's recommendation>
**Decision**: _Pending_

## Resolved

Decisions that have been made. Kept as a record.

### Q1: <Question>

**Decision**: <What was decided>
**Date**: YYYY-MM-DD
**Rationale**: <Why>
```

---

## tickets/\<NNN\>-\<slug\>/Findings.md

```markdown
# Findings: <Title>

Curated implementation findings discovered while executing or reviewing this ticket. Update progressively while work is in flight and revisit before closing the ticket. Do not use this as a chronological log.

## Findings

### F1: <Short title>

**Category**: Assumption | Spec clarification | Friction | Workaround | Follow-up | Risk | Test gap
**Finding**: <What was learned>
**Impact**: <Why it matters>
**Disposition**: Addressed here | Follow-up needed | Accepted for now
**Follow-up**: <Ticket / action / none>
```
