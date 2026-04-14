---
name: specs-finish-ticket
description: "Review an implemented ticket in a fresh conversation before marking it done. Use when implementation is believed complete and the ticket needs an independent closeout review against specs, architecture, code, and tests. Triggers on: 'finish ticket', 'close ticket', 'final ticket review', 'ready to close', 'review completed ticket', 'verify ticket implementation', 'ticket closeout'."
---

# Specs Finish Ticket

Review an implemented ticket in a fresh conversation before marking it `done`.

This skill verifies that the implementation matches the spec, the plan was meaningfully executed, the tests meaningfully cover the promised behavior, any important drift is corrected in `specs/`, and durable implementation discoveries are captured in `Findings.md`.

## Skill Dependencies

This skill is part of a set of skills designed to work together:

- **spec-driven** — Core rules and high-level document map
- **specs-setup** — Initialize `specs/` for a new project
- **specs-tickets** — Create and execute tickets through their lifecycle
- **specs-review** — Audit specs health, consistency, and drift
- **specs-finish-ticket** (this skill) — Review implemented tickets before closure

If any of these skills are missing from the project, **instruct the user to install them** before proceeding:

```bash
npx skills add b12consulting/skills --skill <missing_skill>
```

**Always load the [spec-driven](../spec-driven/SKILL.md) skill first** for the core rules. Load the [methodology reference](../spec-driven/references/methodology.md) for detailed lifecycle, drift, ADR, and Findings guidance. Load [templates](../spec-driven/references/templates.md) only if you need to update ticket docs.

## Fresh Review Requirement

This skill is intended for a **fresh conversation** so the reviewing agent is not biased by the implementation path.

- If the current conversation already contains the implementation work for this ticket, **tell the user to restart in a fresh conversation before proceeding**.
- If the user explicitly wants to continue anyway, note that reviewer independence is reduced and proceed only with that caveat.

## Procedure

### 1. Identify The Ticket

Ask the user which ticket to finish, or identify it from conversation context:

- ticket number such as `003`
- title or description

If ambiguous, list likely matches and ask the user to choose.

### 2. Load The Ground Truth

Read the project-level docs needed to judge the ticket correctly:

1. `specs/README.md`
2. `specs/Vision.md`
3. `specs/PRD.md`
4. `specs/Architecture/README.md`
5. Relevant architecture sub-documents such as `data-model.md` or other topic-specific architecture docs when the ticket touches stable entities, public contracts, or persisted shapes

If these documents contradict each other, flag that before reviewing the ticket implementation.

### 3. Read The Full Ticket Record

Read the ticket `Spec.md` and every document present in the ticket folder, especially:

- `Spec.md`
- `Plan.md`
- `Research.md`
- `Decisions.md`
- `Findings.md`

Build a simple mental model of:

- what the ticket promised
- what approach was chosen
- what code and tests should exist
- what risks, assumptions, or follow-ups were already recorded

### 4. Gather Implementation Evidence

Inspect the actual implementation and tests.

- Use `Plan.md` and the codebase to find the touched files.
- Inspect the current code, not just the ticket narrative.
- If work is uncommitted, inspect the current git changes as part of the evidence.
- If needed, read file history or recent commits to understand whether the code reflects the completed ticket or unrelated drift.

### 5. Review The Ticket Across These Dimensions

#### A. Spec Compliance

- Does the implementation satisfy every acceptance criterion in `Spec.md`?
- Does every user story have corresponding code and observable behavior?
- Was any out-of-scope behavior added without being documented or approved?
- Were assumptions made during implementation captured when they matter long-term?

#### B. Architecture And Design Quality

- Does the implementation align with `Architecture/README.md` and relevant sub-documents?
- Are there obvious anti-patterns, boundary violations, hidden coupling, or temporary shims that should not remain?
- If the ticket changed stable system behavior, were the relevant `specs/` documents updated?

#### C. Code Quality

- Does the implementation solve the root problem rather than patching symptoms?
- Is the scope tight and coherent?
- Are naming, ownership, and structure consistent with the surrounding codebase?
- Is there dead compatibility code, abandoned scaffolding, or undocumented workaround logic?

#### D. Test Quality

- Do tests cover the promised behavior rather than only implementation details?
- Do tests meaningfully cover the acceptance criteria?
- Are important negative, edge, or regression cases covered when the spec warrants them?
- Are the tests useful enough that a future regression would be caught?

#### E. Ticket Documentation Hygiene

- Does `Plan.md` still reflect what was actually done, or did the implementation drift without documentation?
- Does `Findings.md` capture durable discoveries with clear dispositions?

### 6. Update Docs During Review

You may update documentation during finish review, but use this boundary carefully.

Allowed without extra confirmation:

- create or update `Findings.md` when the review uncovers durable context worth preserving
- correct **factual drift** in `Spec.md`, `Plan.md`, or project-level `specs/` docs when the completed ticket already established the shipped reality and the change does not introduce a new product or architecture decision
- if the ticket is ready to close, update the ticket `Spec.md`, `specs/README.md`, and `specs/Changelog.md` to reflect the shipped outcome of the current ticket when appropriate

Stop and ask the user before making any other changes, including:

- creating new tickets
- creating ADRs
- changing product scope or architectural intent rather than documenting factual reality
- making speculative cleanup changes outside the ticket closeout work

### 7. Determine The Outcome

Use one of these outcomes:

#### Ready To Close

Use this when:

- the spec is implemented
- the plan was executed coherently
- tests are good enough for the promised behavior
- relevant drift has been corrected
- remaining concerns are minor and do not require follow-up work

Actions:

1. Update `Findings.md` if needed.
2. Mark the ticket `done` in `Spec.md` and update the `updated` date.
3. Update `specs/README.md` to move the ticket into the completed section.
4. Update `specs/Changelog.md` based on the shipped outcome of the current ticket when appropriate.

#### Close With Follow-Up

Use this when the current ticket satisfies its spec, but the review discovered worthwhile follow-up improvements that should not block closure.

Actions:

1. Update `Findings.md` with the follow-up candidate and a `Follow-up needed` disposition.
2. Mark the current ticket `done` in `Spec.md` and update the project dashboard.
3. Update `specs/Changelog.md` based on the shipped outcome of the current ticket when appropriate.
4. Report the suggested follow-up work to the user and ask for confirmation before creating any new ticket or broader docs.

#### Changes Required

Use this when the implementation does not actually satisfy the spec, has meaningful anti-patterns, or lacks sufficient test coverage.

Actions:

1. Do **not** mark the ticket `done`.
2. Update `Findings.md` with the concrete gaps discovered during review.
3. Report the required changes to the user with findings first, ordered by severity.

### 8. Report Findings Clearly

When the review finds issues, report them like a code review:

- findings first, ordered by severity
- reference the affected files and, when useful, the relevant ticket or spec file
- keep the summary brief after the findings

If no meaningful findings are discovered, say so explicitly and note any residual risk that still exists.
