# TodayBite System Build Rules

## 1. Purpose

This document defines the upstream rules for all future UI and code generation work in TodayBite.

The goal is not to optimize single outputs one by one. The goal is to create a stable environment that continuously generates correct code through explicit rules, reusable structures, and feedback loops.

These rules are the source of truth for:

- UI optimization
- component design
- page reconstruction
- AI-assisted implementation
- prompt construction for future coding tasks

## 2. Four Non-Negotiable Principles

### 2.1 Make tacit experience explicit

Anything that repeatedly relies on intuition, memory, taste, or verbal reminders must be converted into explicit artifacts.

Explicit artifacts include:

- design tokens
- component rules
- page information hierarchy
- state matrices
- prompt templates
- acceptance checklists
- naming rules
- implementation boundaries

Rule:

If a decision must be repeated twice, it should no longer live only in conversation.

It must be written into a rule, template, or workflow.

### 2.2 Mechanize textual constraints

Natural-language constraints are not enough.

Whenever possible, constraints must be transformed into structures that force or strongly bias correct output.

Mechanization examples:

- replace vague style instructions with tokenized color, spacing, radius, shadow, and typography rules
- replace “keep consistency” with a defined component API and variant set
- replace “follow the same layout” with fixed page sections and ordering
- replace “make it better” with measurable acceptance criteria
- replace freeform prompts with fixed prompt slots

Rule:

If a human can interpret a sentence in multiple ways, the sentence is not yet a usable build rule.

### 2.3 Replace one-shot delivery with a continuous feedback loop

Every UI or code task must be designed as a loop, not a one-time handoff.

Required loop:

1. Define objective
2. Define constraints
3. Produce structured output
4. Check against checklist
5. Identify mismatch
6. Revise
7. Lock reusable rule if the revision teaches something stable

Rule:

No implementation task is complete until its reusable lessons are either:

- absorbed into existing rules
- or added as a new rule

### 2.4 Shift humans from writing code to designing systems

The human role is to define the environment that makes good code the default outcome.

That environment includes:

- rules
- workflows
- design systems
- prompt structures
- review checklists
- file responsibilities
- acceptance criteria

Rule:

Humans should spend less effort specifying line-by-line code and more effort specifying:

- what is allowed
- what is forbidden
- how output is reviewed
- how lessons become reusable

## 3. Source of Truth Hierarchy

When rules conflict, apply the following priority:

1. product requirements and confirmed business logic
2. system build rules in this document
3. page-level UX rules
4. component-level rules
5. implementation convenience

Rule:

Convenience never overrides consistency.

## 4. Build Pipeline for Every Future Task

Every future UI or frontend coding task must follow this pipeline.

### Step 1: Define the target

The task must first state:

- target page or component
- user goal
- primary action
- secondary actions
- success criteria

No coding begins before these are written down.

### Step 2: Define information hierarchy

Before designing visuals, define:

- what users must notice first
- what users may notice second
- what is supporting information
- what can be hidden or collapsed

Rule:

Information hierarchy is decided before color, spacing, or motion.

### Step 3: Bind the task to system rules

Before implementation, map the task to existing rules:

- design tokens
- component variants
- page sections
- state rules
- copy rules

Rule:

If a new design pattern is needed, first check whether an existing pattern can be extended.

Do not create a one-off pattern without documenting why.

### Step 4: Implement the minimum complete structure

Implementation must prioritize:

- correct structure
- clear hierarchy
- predictable variants
- complete states

Do not start with polish.

### Step 5: Run the review checklist

The output must be checked for:

- hierarchy clarity
- action clarity
- token consistency
- component reuse
- state completeness
- mobile usability
- copy precision

### Step 6: Capture the reusable lesson

If the task revealed a new stable pattern, update the rules.

That is mandatory.

## 5. UI System Rules

## 5.1 Design tokens first

No page or component should invent its own visual language.

All UI work must be derived from a shared token layer.

Required token categories:

- color
- spacing
- radius
- shadow
- typography
- border
- semantic state colors

Rule:

No hardcoded “special” visual style for a single business component unless explicitly approved as a system pattern.

## 5.2 Components before pages

Pages should be assembled from system components, not from one-off markup.

Required order:

1. token definition
2. base component rule
3. composed business component
4. page assembly

Rule:

If the same pattern appears twice, it must become a component or a variant.

## 5.3 States are mandatory, not optional

Every page and component must define at least these states when applicable:

- default
- hover
- active
- disabled
- loading
- empty
- error
- success

Rule:

A component is incomplete if its interaction and failure states are undefined.

## 5.4 Recommendation-first hierarchy

TodayBite is a decision-assistance product.

The interface must visually prioritize:

1. recommendation outcome
2. recommendation reasoning
3. price and calorie fit
4. controls and filters
5. supporting description

Rule:

If a screen looks beautiful but does not clearly answer “why this recommendation”, it fails.

## 5.5 Mobile-first density

The default layout should assume a mobile screen first.

Rule:

Any interaction that feels acceptable only on desktop is not finished.

## 6. Code Construction Rules

## 6.1 Do not encode design decisions ad hoc

Forbidden patterns:

- repeated literal spacing values without token meaning
- duplicated card styles across files
- page-specific button styles when a reusable variant is possible
- mixing visual semantics and business logic in uncontrolled ways

## 6.2 One component, one responsibility

A component should have one clear purpose.

Examples:

- present recommendation summary
- capture budget input
- display nutrient tags

Rule:

Do not create oversized components that both manage layout strategy and contain multiple unrelated interaction concerns.

## 6.3 Business components must explain their interface

Every business component should have a stable interface with explicit props.

Rule:

If a prop exists only to patch a one-off visual inconsistency, fix the system instead of adding the prop.

## 6.4 Prefer variants over branching styles

When a component needs multiple appearances, define variants.

Rule:

Do not scatter condition-heavy class construction across multiple pages if the variation belongs to the component API.

## 7. Review Checklist

Before considering any UI task complete, review all items below.

- Is the primary user goal visually obvious within 3 seconds?
- Is the main action singular and unambiguous?
- Does the page use existing tokens and components instead of ad hoc styles?
- Are recommendation reasons explicit rather than implied?
- Are loading, empty, error, and success states handled?
- Is the mobile layout still usable without precision clicking?
- Does the copy explain uncertainty where AI estimation exists?
- Did this task create a reusable rule that should be documented?

If any answer is no, the task is not complete.

## 8. Fixed Prompt Structure for Future AI Tasks

All future AI coding requests for TodayBite should follow this structure.

### 8.1 Task template

Use the following fixed sections:

```md
# Task
[What page/component/system is being changed]

# Objective
[What user outcome should improve]

# Scope
[What files or layers may be touched]

# Constraints
[Tokens, components, behaviors, business constraints, forbidden shortcuts]

# Existing System Reuse
[What existing components, tokens, or patterns must be reused first]

# Required States
[default/loading/empty/error/success/etc.]

# Acceptance Criteria
[Concrete pass/fail conditions]

# Feedback Loop
[How the output will be checked and what should be updated if a new rule emerges]
```

### 8.2 Mandatory prompt rules

Every prompt must explicitly answer:

- what problem is being solved
- what not to change
- what must be reused
- what the output will be judged against
- what lessons should be captured if the implementation reveals a stable pattern

## 9. What Changes After This Document

From this point onward:

- UI work starts from system rules, not local inspiration
- prompts must use a fixed structure
- reusable lessons must be documented
- page optimization must follow component and token constraints
- implementation is part of a loop, not a one-shot delivery

## 10. Current Next Step

The immediate next task after this document is:

1. define TodayBite visual tokens
2. define base component rules
3. redesign pages using the system rather than ad hoc styling
