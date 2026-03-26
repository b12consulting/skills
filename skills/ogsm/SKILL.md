---
name: ogsm
description: "Create, review, or refine an OGSM strategic plan (Objective, Goals, Strategies, Measures). Use when: building a one-page strategy, translating workshop insights into strategic plans, reviewing strategic alignment, cascading company objectives to team level, converting vision into measurable action plans."
argument-hint: "Describe the context: source material (workshop transcript, notes, vision doc), scope (company/department/team), and time horizon"
---

# OGSM Strategic Planning

Build rigorous one-page strategic plans using the OGSM framework (Objective, Goals, Strategies, Measures). Originated at Procter & Gamble from Japanese strategic planning in the 1950s, OGSM is used by Fortune 500 companies to align entire organizations on a single page.

## When to Use

- Translating workshop insights, interviews, or vision documents into a structured strategic plan
- Creating a new OGSM from scratch for an organization, department, or team
- Reviewing or refining an existing OGSM for quality and coherence
- Cascading a company-level OGSM down to department or team level
- Comparing before/after versions of a strategic plan

## Core Concepts

OGSM answers four questions on a single page:

| Component | Question | Nature |
|-----------|----------|--------|
| **Objective** | Where do we want to go? | Qualitative — the ambition |
| **Goals** | How do we know we arrived? | Quantitative — SMART targets |
| **Strategies** | What choices will get us there? | Directional — 3-5 key levers |
| **Measures** | How do we track progress? | Operational — KPIs + actions |

The first two (O + G) define **WHAT**. The last two (S + M) define **HOW**.

## Procedure

### Step 0 — Gather Context

Before writing, collect:
- Source material (transcripts, notes, existing strategy docs)
- Scope: company-wide, department, or team?
- Time horizon: typically 1-3 years (Objective) with annual cycles
- Any parent OGSM to cascade from (a parent Strategy becomes the child's Objective)
- Stakeholder quotes or raw data that ground the plan in reality

### Step 1 — Draft the Objective

Write ONE qualitative statement (2-4 sentences max) that captures the overarching ambition.

**Quality criteria for a good Objective:**
- [ ] Inspiring — people can rally behind it
- [ ] Directional — makes clear WHERE the organization is heading
- [ ] Qualitative — no numbers (those belong in Goals)
- [ ] Scoped — specifies the domain and context
- [ ] Grounded — reflects the real situation and constraints (not generic)
- [ ] Singular — ONE objective, not a list

**Pattern**: `[Verb of ambition] + [domain/scope] + [by/through] + [direction/how]`

**Example**: "Become the market leader in European automotive components by transforming into a fully customer-driven organization."

**Anti-patterns to avoid:**
- Too vague: "Be the best company" (no scope, no direction)
- Too operational: "Implement SAP across all sites" (that's a strategy)
- Multiple objectives crammed together
- Objective that is a restatement of current state

### Step 2 — Define Goals (3-5)

Goals make the Objective measurable. Each Goal must be SMART.

**Quality criteria for good Goals:**
- [ ] Specific — clearly defines what is measured
- [ ] Measurable — has a number or percentage
- [ ] Achievable — ambitious but realistic
- [ ] Relevant — directly tied to the Objective
- [ ] Time-bound — has a deadline or horizon
- [ ] Independent — Goals should not overlap significantly

**Format**: Use a table with columns: `#`, `Goal`, `KPI`, `Baseline`, `Target`, `Horizon`

**Example:**

| # | Goal | KPI | Baseline | Target | Horizon |
|---|------|-----|----------|--------|---------|
| G1 | Increase market share in Europe | Market share % | 8% | 12% | 2028 |
| G2 | Improve customer satisfaction | NPS score | 42 | 65 | 2027 |

**Anti-patterns to avoid:**
- Goals without numbers ("Improve quality")
- Goals that are actually strategies ("Launch a new product line")
- Too many goals (>5 dilutes focus)
- Missing baselines (you can't track progress without a starting point — mark as "TBD" if unknown)

### Step 3 — Choose Strategies (3-5)

Strategies are the key choices — the big levers you will pull. They are NOT a to-do list.

**Quality criteria for good Strategies:**
- [ ] Choice-making — each strategy implies what you will NOT do
- [ ] Lever-sized — big enough to move the needle on multiple Goals
- [ ] Distinct — no overlap between strategies
- [ ] Actionable — can be broken down into concrete measures
- [ ] Named clearly — use a short title + description structure

**Structure each strategy as:**
1. **Title** — short, memorable label (e.g., "Regulatory Mastery")
2. **Description** — 2-3 sentences explaining the strategic direction
3. **Contributes to Goals** — explicit mapping to G1, G2, etc.
4. **Key areas of intervention** — 3-5 bullet points on where action happens

**Anti-patterns to avoid:**
- Strategies that are tasks ("Hire 3 people in Q2" — that's a Measure/action)
- Strategies without clear connection to Goals
- More than 5 strategies (forces tough choices — that's the point)
- Generic strategies ("Improve operational excellence" — what does this mean concretely?)

### Step 4 — Define Measures (KPIs + Actions)

Each Strategy gets its own Measures: dashboard KPIs and concrete actions.

**Quality criteria for good Measures:**

For **KPIs (Dashboard metrics)**:
- [ ] Quantitative and trackable
- [ ] Leading indicators preferred over lagging where possible
- [ ] Tied to a specific Strategy
- [ ] Has a baseline (or "TBD") and a target

For **Actions**:
- [ ] Specific and concrete
- [ ] Has an owner and a deadline
- [ ] Directly supports the KPI it's under
- [ ] SMART-formulated

**Format**: Use a table per Strategy:

| Strategy | KPI | Baseline | Target | Action | Owner | Deadline |
|----------|-----|----------|--------|--------|-------|----------|
| S1 | Zero-touch invoice rate | 0% | 60% | Implement Basware auto-matching | Lev | Q3 2027 |

**Anti-patterns to avoid:**
- Measures without owners (nobody is accountable)
- KPIs that don't connect to any Strategy
- Actions without deadlines
- Too many measures per strategy (5-7 max — focus)

### Step 5 — Cross-check & Validate

Run these coherence checks on the completed OGSM:

1. **Vertical alignment**: Does every Goal connect to the Objective? Does every Strategy connect to at least one Goal? Does every Measure connect to a Strategy?
2. **Coverage**: Are all Goals addressed by at least one Strategy? Are all Strategies covered by at least one Measure?
3. **Strategy-Goal matrix**: Create a cross-reference table (Strategies × Goals) with markers showing which strategies contribute to which goals. Look for orphans.
4. **One-page test**: Can the entire OGSM be understood on a single page (or a concise document)? If not, simplify.
5. **"So what?" test**: Read each component aloud. If someone could say "any company could write this," it's too generic — make it specific to the context.
6. **Exclusion test**: Are there explicit things the organization chooses NOT to do? Good OGSM makes trade-offs visible.

### Step 6 — Format & Deliver

Output the OGSM as a Markdown document with this structure:

```markdown
# [Organization/Team] — OGSM [Year/Period]

> **Context**: [Brief description of source, date, participants]

---

## Objective (O)

[Single qualitative statement]

### Context
[2-5 bullet points grounding the objective in reality]

---

## Goals (G)

| # | Goal | KPI | Baseline | Target | Horizon |
|---|------|-----|----------|--------|---------|

---

## Strategies (S)

### S1 — [Title]
**Description**: ...
**Contributes to**: G1, G2
**Key areas**: ...

### S2 — [Title]
...

---

## Measures (M)

| Strategy | KPI | Baseline | Target | Action | Owner | Deadline |
|----------|-----|----------|--------|--------|-------|----------|

---

## Strategy × Goals Matrix

|  | G1 | G2 | G3 |
|--|:--:|:--:|:--:|
| S1 | ● |  | ● |
| S2 |  | ● | ● |

---

## Exclusions & Constraints
[What will NOT be done and why]

## Next Steps
[Immediate follow-up actions]
```

## Cascading OGSMs

When creating a department or team OGSM from a parent OGSM:

1. The **parent's Strategy** becomes the **child's Objective**
2. The child defines its own Goals, Strategies, and Measures within that scope
3. The child's Goals should roll up to (contribute to) the parent's Goals
4. Ensure alignment without duplication — each level adds specificity

```
Company OGSM
  └── Strategy S2: "Accelerate transactional processes"
        ↓ becomes ↓
Finance Department OGSM
  └── Objective: "Accelerate transactional processes in Finance..."
        └── Goals: specific Finance KPIs
        └── Strategies: Finance-specific levers
        └── Measures: Finance team actions
```

## Review Checklist

When reviewing an existing OGSM, assess each dimension:

| Dimension | Check |
|-----------|-------|
| Objective clarity | Is it inspiring, directional, and singular? |
| Goal completeness | Are Goals SMART with baselines and targets? |
| Strategy distinctness | Are Strategies choices (not tasks) with clear scope? |
| Measure accountability | Do all Measures have owners and deadlines? |
| Vertical alignment | O → G → S → M chain is unbroken? |
| Coverage | No orphan Goals or Strategies? |
| Specificity | Would this OGSM only make sense for THIS organization? |
| One-page fit | Could an executive grasp it in 5 minutes? |
| Trade-offs | Are exclusions explicit? |

## OGSM vs. Related Frameworks

| Framework | Key Difference |
|-----------|---------------|
| **OKR** (Objectives & Key Results) | Quarterly cycle, no explicit strategy layer, focused on stretch goals |
| **Balanced Scorecard** | Four predefined perspectives (financial, customer, process, learning); OGSM is perspective-agnostic |
| **SWOT** | Diagnostic tool (input to OGSM), not an action framework |
| **V2MOM** (Salesforce) | Similar structure but adds Vision and Values layers; OGSM is more concise |

OGSM is ideal when you need strategy + execution alignment on a single page, especially for cascading across organizational levels.
