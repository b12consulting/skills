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
- [Goals](Goals.md)
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

## specs/Goals.md

```markdown
# Goals

## Success Metrics

How do we measure success? Define quantitative and qualitative indicators.

| Metric | Target | How Measured |
|--------|--------|-------------|
| | | |

## Milestones

| Milestone | Description | Target Date | Status |
|-----------|-------------|-------------|--------|
| | | | |
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

## Context

What situation or problem prompted this decision?

## Decision

What did we decide?

## Consequences

What are the trade-offs? What becomes easier? What becomes harder?
```

---

## tickets/\<NNN\>-\<slug\>/README.md

```yaml
---
id: "<NNN>"
title: "<Descriptive title>"
status: research
jira: ""
owner: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

```markdown
# <NNN> — <Title>

<One-paragraph summary of what this ticket covers and why.>
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
# Spec: <Title>

## User Stories

### US-1: <Story title>

**As a** <persona>, **I want** <action>, **so that** <benefit>.

### US-2: <Story title>

**As a** <persona>, **I want** <action>, **so that** <benefit>.

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

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| | | | |
```

---

## tickets/\<NNN\>-\<slug\>/Tasks.md

```markdown
# Tasks: <Title>

## Task List

- [ ] **Task 1**: <Description>
- [ ] **Task 2**: <Description>
- [ ] **Task 3**: <Description>

## Completion Criteria

All tasks checked off and acceptance criteria from Spec.md verified.
```

---

## tickets/\<NNN\>-\<slug\>/Dependencies.md

```markdown
# Dependencies: <Title>

## Blocked By

| Ticket | Title | Status | Impact |
|--------|-------|--------|--------|
| | | | |

## Blocks

| Ticket | Title | Impact |
|--------|-------|--------|
| | | |

## External Dependencies

List any external systems, APIs, or third-party dependencies.
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

## tickets/\<NNN\>-\<slug\>/Journal.md

```markdown
# Journal: <Title>

Chronological record of how this ticket evolved. Not a chat transcript — a curated summary of key decisions, pivots, and process.

## YYYY-MM-DD

- <Event or decision>
```
