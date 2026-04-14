---
name: specs-tickets
description: "Create new spec-driven tickets and resume existing ones through the full lifecycle: research, specification, planning, and implementation. Use when: the user describes new work to be done; continuing a previously started ticket; a feature, bug fix, or task needs planning and implementation; starting or resuming planned work on a project with specs/. Triggers on: 'new ticket', 'new feature', 'fix bug', 'implement', 'create ticket', 'I want to build', 'let us work on', 'add feature', 'continue ticket', 'resume work', 'pick up where we left off', 'work on ticket', 'existing ticket', 'check ticket status', 'what is the state of ticket'."
---

# Specs Tickets

Create and execute tickets through the spec-driven lifecycle, or resume work on existing ones.

## Skill Dependencies

This skill is part of a set of skills designed to work together:

- **spec-driven** — Core rules and high-level document map
- **specs-setup** — Initialize `specs/` for a new project
- **specs-tickets** (this skill) — Create and execute tickets through their lifecycle
- **specs-review** — Audit specs health, consistency, and drift
- **specs-finish-ticket** — Review implemented tickets before closure

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the core rules. Load the [methodology reference](../spec-driven/references/methodology.md) for detailed lifecycle and Findings guidance. Load [templates](../spec-driven/references/templates.md) when creating documents.

## Prerequisites

1. Verify `specs/` folder exists with `Vision.md`, `PRD.md`, and `Architecture/README.md`. If missing, prompt the user to run the [specs-setup](../specs-setup/SKILL.md) skill first.
2. Read `specs/README.md`, then `specs/Vision.md`, `specs/PRD.md`, and `specs/Architecture/README.md` to understand the project context.
3. Read architecture sub-documents relevant to your ticket such as `specs/Architecture/data-model.md`.

---

## Entry Point: New Ticket or Existing?

Determine whether the user wants to **create a new ticket** or **continue an existing one**.

- If the user describes new work, go to the New Ticket section below.
- If the user references an existing ticket, go to the Resume Ticket section below.
- If unclear, ask the user.

---

## New Ticket

### Phase 0: Create Ticket

1. Ask the user to describe the work to be done.
2. Determine the next ticket number: scan `specs/tickets/` for the highest existing number and increment by one. If no tickets exist, start at `001`.
3. Derive a short slug from the description using lowercase hyphen-separated words.
4. Create the ticket folder and `Spec.md`:

```text
specs/tickets/<NNN>-<slug>/Spec.md
```

Use this frontmatter:

```yaml
---
id: "<NNN>"
title: "<Descriptive title>"
status: research
owner: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Follow with a one-paragraph summary of the ticket and the initial spec scaffold.

Then proceed to Phase 1: Research.

---

## Resume Ticket

### 1. Identify the Ticket

Ask the user which ticket to continue, or identify it from conversation context:

- ticket number such as `003`
- description such as `the auth ticket` by scanning ticket titles

If ambiguous, list active tickets from `specs/README.md` and ask the user to pick one.

### 2. Read Ticket State

Read the ticket's `Spec.md` and note the **status** from frontmatter. Then read **all existing documents** in the ticket folder to understand the full context.

Summarize the current state for the user: what phase the ticket is in, what is complete, and what comes next.

### 3. Check for Drift

Compare the ticket's documents against the current state of:

- **`specs/Vision.md`** and **`specs/PRD.md`** — have requirements or success expectations changed since this ticket was written?
- **`specs/Architecture/README.md`** — has the architecture evolved?
- **the codebase** — has relevant code changed since the ticket was last worked on?

If drift is detected:

- report the specific inconsistencies to the user
- discuss whether the ticket needs updating before continuing
- if specs changed, the ticket may need `Spec.md` or `Plan.md` updates
- if code changed, completed checklist items may need re-verification

### 4. Resolve Blockers

If the ticket status is `open-questions`:

- present the unresolved questions from `Decisions.md` to the user
- ask for decisions on each
- record decisions in the Resolved section of `Decisions.md`
- update the ticket status once all questions are answered

If the ticket's `Plan.md` already records unresolved blockers or sequencing constraints:

- report those blockers and their current status
- discuss whether to wait, work around, or re-scope

### 5. Resume the Lifecycle

Based on the current status, pick up at the appropriate phase:

| Current Status   | Next Action                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| `research`       | Review `Research.md` findings. Proceed to Phase 2: Specify.                                                     |
| `specifying`     | Check whether `Spec.md` has been validated. If yes, proceed to Phase 3: Plan. If no, present it for validation. |
| `open-questions` | Resolve questions, then return to the prior phase.                                                              |
| `planned`        | Review `Plan.md`, including its checklist, and proceed to implementation once it is confirmed.                  |
| `in-progress`    | Continue from the execution checklist in `Plan.md`.                                                             |
| `done`           | Inform the user the ticket is complete. Ask whether they want to reopen it or create a follow-up.               |
| `archived`       | Inform the user the ticket was archived. Ask whether they want to create a new ticket instead.                  |

### 6. Update Findings

If resuming work uncovers durable assumptions, frictions, workarounds, follow-up candidates, or residual risks, create or update `Findings.md`. Keep it curated and durable rather than chronological.

---

## Ticket Lifecycle

The lifecycle is: Research → Specify → Plan → Implement → Finish Review → Done.

User validation is required at the spec, plan, and closeout checkpoints.

**Any participant (human or agent) can execute any phase.** The lifecycle defines the order, not who does what.

---

### Phase 1: Research

**Goal**: Understand the problem space and gather information needed to write a good spec.

1. Investigate the codebase, existing documentation, and any external resources relevant to the ticket.
2. Identify technical constraints, existing patterns, and potential approaches.
3. If the ticket may affect domain entities or boundary payloads, identify:
   - the canonical domain concepts involved
   - the canonical boundary contract involved
   - the owner, producers, and consumers of that contract
   - whether serialization or persistence format differs from the canonical in-memory shape
4. Document findings in `Research.md`:
   - Objective: what we are trying to learn
   - Findings: organized by topic
   - Options considered with pros and cons
   - Recommendation
   - References
5. Update ticket status to `research` in `Spec.md`.

**`Research.md` is optional for straightforward tickets.** If the path is clear from the user's description, skip directly to Phase 2. A one-line bug fix does not need research, but a new feature with multiple possible approaches often does.

---

### Phase 2: Specify

**Goal**: Define what done looks like.

1. Based on research findings or the user's description, write `Spec.md`:
   - **User stories**: who wants what and why. Assign a **priority** (`P1`, `P2`, `P3`, ...) to each story. Each story should be **independently testable** and include a one-line verification note.
   - **Acceptance criteria**: concrete, testable conditions that prove the work is done
   - **Scope boundaries**: what is in scope and explicitly out of scope

2. **Clarification scan.** Before finalizing the spec, scan it for ambiguity across these categories:
   - functional scope and behavior
   - domain and data model
   - interaction and UX flow
   - non-functional quality attributes
   - integration and external dependencies
   - edge cases and failure handling
   - constraints and trade-offs
   - terminology consistency

   For each category that is partial or missing, decide whether clarification materially affects implementation. If it does, ask the user. Limit yourself to the most impactful questions. If a gap is better deferred to planning, note it internally and move on.

3. If there are unresolved questions that block specification, create `Decisions.md`:
   - list each question with context in the Open section
   - provide options with trade-offs for each
   - include a suggested answer for each
   - ask the user to decide on all open questions before proceeding
   - move resolved questions to the Resolved section with the decision, date, and rationale

4. **Self-validate the spec.** Before presenting it to the user, check:
   - no implementation details have leaked into the spec
   - every requirement is testable and unambiguous
   - acceptance criteria are measurable
   - scope is clearly bounded
   - no more than 3 items remain marked `[NEEDS CLARIFICATION]`
   - all user stories have a priority and an independent-test description
   - field-level schema details appear in the spec only when they are part of a user-visible or product-level contract; stable technical contract definitions live in architecture docs or the plan

   If any check fails, fix the spec before presenting it.

5. Update ticket status to `specifying`, or `open-questions` if questions exist, in `Spec.md`.

6. **Present `Spec.md` to the user for validation.**

> **CHECKPOINT: Do not proceed to Phase 3 until the user has validated the spec.**

---

### Phase 3: Plan

**Goal**: Define the implementation strategy and executable checklist.

1. Based on the confirmed spec, write `Plan.md`:
   - **Approach**: high-level implementation strategy
   - **Key design decisions**: important choices and their rationale
   - **Dependencies and sequencing**: only the blockers or ordering constraints that materially affect execution
   - **Data model and contract impact**: canonical entities, boundary contracts, serialization differences, and compatibility or cutover policy when relevant
   - **Implementation checklist**: the concrete execution checklist with file-scoped items
   - **Risks and mitigations**: what could go wrong and how to handle it
   - **Verification**: the checks that prove the plan satisfies the spec

2. **Check alignment with architecture docs.** If the plan requires architectural changes:
   - flag this to the user explicitly
   - propose an ADR in `specs/decisions/`
   - update `specs/Architecture/README.md` and any affected sub-documents only after user approval

3. **Coverage check.** Before presenting the plan, verify that `Spec.md` and `Plan.md` are consistent:
   - every requirement maps to at least one checklist item
   - every checklist item traces back to a requirement or design decision
   - terminology is consistent across the two files

   For tickets that affect data modeling or boundary contracts, also verify:
   - every changed canonical entity or contract is reflected in the relevant architecture doc
   - every contract change has explicit verification checklist items for producer and consumer alignment
   - compatibility or migration work is represented in `Plan.md` when needed

   If gaps are found, update `Plan.md` or `Spec.md` before proceeding. This check is lightweight — skip it for very small tickets with <= 5 checklist items.

4. Update ticket status to `planned` in `Spec.md`.

5. **Present `Plan.md` to the user for confirmation.**

> **CHECKPOINT: Do not proceed to implementation until the user has confirmed the plan.**

---

### Phase 4: Implement

**Goal**: Execute the plan.

1. Work through the execution checklist in `Plan.md` sequentially:
   - check off each item as it is completed
   - if an item reveals the spec or plan needs updating, pause implementation
   - update the relevant document, inform the user, and get confirmation if the change is significant

2. Update `Findings.md` progressively:
   - use it for durable discoveries that matter after the session ends
   - create it as soon as those discoveries appear; do not wait until the ticket is nearly done
   - every finding must end with a clear disposition such as `Addressed here`, `Follow-up needed`, or `Accepted for now`

3. **Drift detection during implementation**: If implementation reveals a conflict with `Vision.md`, `PRD.md`, or architecture docs:
   - alert the user immediately
   - either create an ADR to update specs, or create a follow-up ticket to fix the code
   - **do not silently deviate from specs**

4. Update ticket status to `in-progress` in `Spec.md`.

---

### Phase 5: Prepare Finish Review

**Goal**: Hand the ticket off for independent closeout review before it is marked done.

1. Verify all acceptance criteria from `Spec.md` appear to be met.
2. Make a final pass over `Plan.md` and `Findings.md`:
   - ensure completed checklist items are checked off or clearly superseded
   - ensure `Findings.md` captures durable assumptions, frictions, follow-up candidates, residual risks, and test gaps with clear dispositions
3. If the ticket affects data shape, update `specs/Architecture/data-model.md` to classify the change explicitly:
4. Do **not** mark the ticket `done` yet.
5. Ask the user to start a **fresh conversation** and run the [specs-finish-ticket](../specs-finish-ticket/SKILL.md) skill for independent review.

The ticket typically remains `in-progress` until the finish review passes and the user confirms closure.

---

## Handling Changes Mid-Flight

Requirements often change during implementation. When they do:

1. Update `Spec.md` with the new or changed requirements.
2. Update `Plan.md` so the approach, sequencing, and checklist still reflect reality.
3. Update `Findings.md` if the change revealed an assumption, workaround, follow-up candidate, or residual risk worth preserving.
4. If the change affects `Vision.md`, `PRD.md`, or architecture docs, create an ADR.
5. If the change alters canonical entities, boundary contracts, or serialization policy, update `specs/Architecture/data-model.md` and/or the relevant architecture docs when those definitions are part of the long-lived system design.
6. Re-validate with the user if the change is significant.

The spec is always the source of truth for the ticket, not the code. Keep it in sync.

## Scaling Guidance

- **Small tickets** such as a bug fix or config change: create the ticket, specify it, write a compact plan with checklist, implement it, then send it to finish review. Skip Research.
- **Medium tickets** such as a feature or refactor: use all phases. Research may be brief.
- **Large tickets** such as a new system or major redesign: use all phases. Consider breaking the work into multiple tickets if the `Plan.md` checklist exceeds ~15 items.
