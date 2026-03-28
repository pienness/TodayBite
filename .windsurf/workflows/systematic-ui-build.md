---
description: TodayBite systematic UI and AI-assisted build workflow
---

# TodayBite Systematic UI Build Workflow

Use this workflow before any frontend, UI, component, or page reconstruction task.

## 1. Read the upstream system rules

Read `docs/SYSTEM_BUILD_RULES.md` first.

You must not begin implementation until the task is framed using that document.

## 2. Rewrite the task into the fixed structure

Restate the task using the following sections:

```md
# Task
# Objective
# Scope
# Constraints
# Existing System Reuse
# Required States
# Acceptance Criteria
# Feedback Loop
```

If any section is missing, the task is not ready for implementation.

## 3. Freeze the target before coding

Before touching code, explicitly decide:

- what screen or component is being changed
- what the primary user action is
- what information must be seen first
- what must remain unchanged
- what existing system parts must be reused

Do not code before these are written down.

## 4. Reuse before inventing

Check for existing:

- design tokens
- base components
- component variants
- page sections
- copy patterns

If an existing pattern can be extended, extend it.

Do not create a one-off pattern unless you can explain why the current system cannot support the need.

## 5. Build in the correct order

Always implement in this order:

1. token or rule change
2. base component change
3. business component change
4. page composition
5. state completion
6. polish

Do not jump directly to polish.

## 6. Complete all required states

For every affected component or page, verify applicable states:

- default
- hover
- active
- disabled
- loading
- empty
- error
- success

If states are undefined, the task is incomplete.

## 7. Run the review checklist

Before considering the task done, answer:

- Is the primary goal obvious within 3 seconds?
- Is the main action singular and clear?
- Are system tokens and components reused consistently?
- Are recommendation reasons explicit?
- Are mobile interactions still usable?
- Are AI uncertainties stated where needed?
- Did this task reveal a reusable lesson?

## 8. Close the feedback loop

After implementation, do one of the following:

- update `docs/SYSTEM_BUILD_RULES.md` if a new stable rule emerged
- document that no new stable rule was produced

No task is complete until the reusable lesson decision is made.
