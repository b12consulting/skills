---
name: specs-tickets
description: "Create new spec-driven tickets and resume existing ones through the full lifecycle: research, specification, planning, task definition, and implementation. Use when: the user describes new work to be done; continuing a previously started ticket; a feature, bug fix, or task needs planning and implementation; starting or resuming planned work on a project with specs/. Triggers on: 'new ticket', 'new feature', 'fix bug', 'implement', 'create ticket', 'I want to build', 'let us work on', 'new task', 'add feature', 'continue ticket', 'resume work', 'pick up where we left off', 'work on ticket', 'existing ticket', 'check ticket status', 'what is the state of ticket'."
---

# Specs Tickets

Create and execute tickets through the spec-driven lifecycle, or resume work on existing ones.

## Skill Dependencies

This skill is part of a set of three skills designed to work together:

- **spec-driven** — Methodology reference (structure, formats, rules)
- **specs-setup** — Initialize `specs/` for a new project
- **specs-tickets** (this skill) — Create and execute tickets through their lifecycle
- **specs-review** — Audit specs health, consistency, and drift

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the full methodology reference. Load [templates](../spec-driven/references/templates.md) when creating documents.

## Prerequisites

1. Verify `specs/` folder exists with `Vision.md`, `PRD.md`, `Goals.md`, and `Architecture/README.md`. If missing, prompt the user to run the [specs-setup](../specs-setup/SKILL.md) skill first.
2. Read `specs/README.md`, then `specs/Vision.md`, `specs/PRD.md`, `specs/Goals.md`, and `specs/Architecture/README.md` to understand the project context.
3. Check for coding standards (`.instructions.md`, `CLAUDE.md`, etc.). If missing, prompt the user to create them before implementation begins.

---

## Entry Point: New Ticket or Existing?

Determine whether the user wants to **create a new ticket** or **continue an existing one**.

- If the user describes new work → go to [New Ticket](#new-ticket)
- If the user references an existing ticket → go to [Resume Ticket](#resume-ticket)
- If unclear, ask the user

---

## New Ticket

### Phase 0: Create Ticket

1. Ask the user to describe the work to be done.
2. Ask for the **Jira issue key** (optional — store in frontmatter if provided).
3. Determine the next ticket number: scan `specs/tickets/` for the highest existing number and increment by one. If no tickets exist, start at `001`.
4. Derive a short slug from the description (lowercase, hyphen-separated).
5. Create the ticket folder and `README.md`:

```
specs/tickets/<NNN>-<slug>/README.md
```

Use this frontmatter:

```yaml
---
id: "<NNN>"
title: "<Descriptive title>"
status: research
jira: "<JIRA-KEY>" # Omit if not provided
owner: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Follow with a one-paragraph summary of the ticket.

Then proceed to [Phase 1: Research](#phase-1-research).

---

## Resume Ticket

### 1. Identify the Ticket

Ask the user which ticket to continue, or identify it from conversation context:

- Ticket number (e.g., "ticket 003")
- Jira key (e.g., "YAI-042") — scan ticket README frontmatter to find the match
- Description (e.g., "the auth ticket") — scan ticket titles to find the best match

If ambiguous, list active tickets from `specs/README.md` and ask the user to pick one.

### 2. Read Ticket State

Read the ticket's `README.md` and note the **status** from frontmatter. Then read **all existing documents** in the ticket folder to understand the full context.

Summarize the current state for the user: what phase the ticket is in, what's been completed, and what comes next.

### 3. Check for Drift

Compare the ticket's documents against the current state of:

- **`specs/Vision.md`** and **`specs/PRD.md`** — Have requirements changed since this ticket was written?
- **`specs/Architecture/README.md`** — Has the architecture evolved?
- **The codebase** — Has relevant code changed since the ticket was last worked on?

If drift is detected:

- Report the specific inconsistencies to the user
- Discuss whether the ticket needs updating before continuing
- If specs changed, the ticket may need its Spec.md or Plan.md updated
- If code changed, completed tasks may need re-verification

### 4. Resolve Blockers

If the ticket status is `open-questions`:

- Present the unresolved questions from `Decisions.md` to the user
- Ask for decisions on each
- Record decisions in the Resolved section of Decisions.md
- Update ticket status once all questions are answered

If the ticket has `Dependencies.md` with unresolved blockers:

- Report the blocking tickets and their current status
- Discuss whether to wait, work around, or re-scope

### 5. Resume the Lifecycle

Based on the current status, pick up at the appropriate phase:

| Current Status   | Next Action                                                                                                                 |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `research`       | Review Research.md findings. Proceed to [Phase 2: Specify](#phase-2-specify).                                               |
| `specifying`     | Check if Spec.md has been validated. If yes, proceed to [Phase 3: Plan](#phase-3-plan). If no, present for validation.      |
| `open-questions` | Resolve questions (step 4), then return to previous phase.                                                                  |
| `planned`        | Check if Tasks.md exists. If yes, present for validation. If no, proceed to [Phase 4: Define Tasks](#phase-4-define-tasks). |
| `in-progress`    | Check Tasks.md for uncompleted tasks. Continue from [Phase 5: Implement](#phase-5-implement).                               |
| `done`           | Inform the user the ticket is complete. Ask if they want to reopen or create a follow-up.                                   |
| `archived`       | Inform the user the ticket was archived. Ask if they want to create a new ticket instead.                                   |

### 6. Update Journal

Add a `Journal.md` entry (create the file if it doesn't exist) noting when work resumed, any drift discovered, and decisions made during this session.

---

## Ticket Lifecycle

The lifecycle has six phases. Each produces specific documents. User validation is required at key checkpoints before proceeding.

```
┌──────────┐    ┌─────────┐    ┌──────┐    ┌─────────────┐    ┌───────────┐    ┌──────┐
│ Research  │───▶│ Specify │───▶│ Plan │───▶│ Define Tasks│───▶│ Implement │───▶│ Done │
└──────────┘    └─────────┘    └──────┘    └─────────────┘    └───────────┘    └──────┘
                     ▲              ▲             ▲
                  User           User          User
                validates      confirms      validates
```

**Any participant (human or agent) can execute any phase.** The lifecycle defines the order, not who does what.

---

### Phase 1: Research

**Goal**: Understand the problem space and gather information needed to write a good spec.

1. Investigate the codebase, existing documentation, and any external resources relevant to the ticket.
2. Identify technical constraints, existing patterns, and potential approaches.
3. Document findings in `Research.md`:
   - Objective: what we're trying to learn
   - Findings: organized by topic
   - Options considered with pros/cons
   - Recommendation
   - References
4. Update ticket status to `research`.

**Research.md is optional for straightforward tickets.** If the path is clear from the user's description, skip directly to Phase 2. A one-line bug fix doesn't need research, but a new feature with multiple possible approaches does.

---

### Phase 2: Specify

**Goal**: Define what "done" looks like.

1. Based on research findings (or the user's description), write `Spec.md`:
   - **User stories**: Who wants what and why
   - **Acceptance criteria**: Concrete, testable conditions that prove the work is done
   - **Scope boundaries**: What's in scope and explicitly out of scope

2. If the ticket has **cross-ticket dependencies**, create `Dependencies.md`:
   - What this ticket is blocked by
   - What this ticket blocks
   - External dependencies

3. If there are **unresolved questions** that block specification, create `Decisions.md`:
   - List each question with context in the **Open** section
   - Provide options with trade-offs for each
   - Include a suggested answer for each
   - **Ask the user to decide on ALL open questions before proceeding**
   - Move resolved questions to the **Resolved** section with the decision, date, and rationale

4. Update ticket status to `specifying` (or `open-questions` if questions exist).

5. **Present Spec.md to the user for validation.**

> **CHECKPOINT: Do not proceed to Phase 3 until the user has validated the spec.**

---

### Phase 3: Plan

**Goal**: Define the implementation strategy.

1. Based on the confirmed spec, write `Plan.md`:
   - **Approach**: High-level implementation strategy
   - **Key design decisions**: Important choices and their rationale
   - **Risks & mitigations**: What could go wrong and how to handle it

2. **Check alignment with Architecture/README.md.** If the plan requires architectural changes:
   - Flag this to the user explicitly
   - Propose an ADR in `specs/decisions/`
   - Update `specs/Architecture/README.md` only after user approval

3. Update ticket status to `planned`.

4. **Present Plan.md to the user for confirmation.**

> **CHECKPOINT: Do not proceed to Phase 4 until the user has confirmed the plan.**

---

### Phase 4: Define Tasks

**Goal**: Break the plan into executable steps.

1. Based on the confirmed plan, write `Tasks.md`:
   - Concrete, actionable tasks as a checklist
   - Each task should be small enough to complete and verify independently
   - Order tasks by dependency (what must be done first)
   - Include verification steps where appropriate (e.g., "run tests", "verify endpoint returns 200")

2. Update ticket status to `planned` (if not already).

3. **Present Tasks.md to the user for validation.**

> **CHECKPOINT: Do not proceed to Phase 5 until the user has validated the tasks.**

---

### Phase 5: Implement

**Goal**: Execute the tasks.

1. Work through `Tasks.md` sequentially:
   - Check off each task as it is completed
   - If a task reveals the spec or plan needs updating, **pause implementation**:
     - Update the relevant document
     - Log the change in `Journal.md`
     - Inform the user of the change
     - Get confirmation before continuing if the change is significant

2. **Drift detection during implementation**: If implementation reveals a conflict with Vision, PRD, Goals, or Architecture:
   - **Alert the user immediately**
   - Either create an ADR to update specs, or create a follow-up ticket to fix the code
   - Do not silently deviate from specs

3. Update ticket status to `in-progress`.

---

### Phase 6: Done

1. Verify **all acceptance criteria** from Spec.md are met.
2. Update ticket `README.md`:
   - Set status to `done`
   - Update the `updated` date
3. Update `specs/README.md`:
   - Move ticket from "Active Tickets" to "Recently Completed"
4. Add an entry to `specs/Changelog.md` describing what was shipped.
5. If any ground truth documents (Vision, PRD, Goals, Architecture) were updated during implementation, verify consistency across all references.

---

## Handling Changes Mid-Flight

Requirements often change during implementation. When they do:

1. Update `Spec.md` with the new or changed requirements.
2. Log the change and rationale in `Journal.md`.
3. If the change affects Vision, PRD, Goals, or Architecture, create an ADR.
4. If the change invalidates completed tasks, update `Tasks.md` accordingly.
5. Re-validate with the user if the change is significant.

The spec is always the source of truth for the ticket, not the code. Keep them in sync.

## Scaling Guidance

- **Small tickets** (bug fix, config change): Phase 0 → Phase 2 → Phase 4 → Phase 5 → Phase 6. Skip Research and Plan.
- **Medium tickets** (feature, refactor): All phases. Research may be brief.
- **Large tickets** (new system, major redesign): All phases. Consider breaking into multiple tickets during Phase 4 if the task list exceeds ~15 items.
