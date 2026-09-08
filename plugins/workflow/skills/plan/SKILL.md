---
name: plan
description: Create a clear implementation plan for a software change before coding.
---

# Plan

Use this skill when the user asks for an implementation plan, design plan, or coding plan.

The plan must help a developer who does not know this change understand what to do and why.

## Process

1. Inspect the relevant code, tests, configuration, and documentation.
2. Find the current entry point and trace the main path.
3. Identify the data or component that owns each behaviour.
4. Record the decisions, state changes, side effects, and important constraints.
5. Reuse clear patterns that already exist in the repository.
6. Define how the change will be verified.

Keep the design simple. Prefer direct control flow, clear names, visible state changes, and local responsibilities. Avoid new layers, generic helpers, or abstractions unless they make the change easier to understand or maintain.

## Plan format

Write a standalone plan. Include:

- **Goal:** the problem and desired result.
- **Current path:** where the behaviour starts and how it works now.
- **Changes:** files or components to update, in implementation order.
- **Decisions:** important choices and their reasons.
- **State and side effects:** what changes, where it changes, and what can be observed.
- **Verification:** tests, checks, or manual steps that prove the result.
- **Open questions:** only questions that block a safe or correct plan.

Use plain, concise language. Use one sentence for one idea. Prefer active voice. Explain unfamiliar terms when first used. Do not hide key reasoning in vague phrases such as "update the system" or "handle the logic".
Make sure the plan is easy to follow for somebody with zero context, or somebody who hasn't read this conversation.

## Code design philosophy

When planning, make sure you consider the following questions:

- Can the reader see where the behaviour starts?
- Can the reader follow the main path without opening many files?
- Are side effects and state changes clear?
- Do names explain why each part exists?
- Does each responsibility stay near the data or component that owns it?
- Is any abstraction making the design harder to follow?
- Could any part be written more directly?
- Can the reader understand the plan without the original conversation?

If the repository does not contain enough information, state the gap and ask questions needed to continue.
