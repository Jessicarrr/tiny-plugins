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

Keep the design simple. Prefer direct control flow, clear names, visible state changes, and local responsibilities.

If the repository does not contain enough information, state the gap and ask questions needed to continue.

## Plan format

Write a standalone plan. Include:

- **Goal:** the problem and desired result.
- **Current path:** where the behaviour starts and how it works now.
- **Changes:** files or components to update, in implementation order. Include code snippets, don't be afraid to use these liberally.
- **Decisions:** important choices and their reasons.
- **State and side effects:** what changes, where it changes, and what can be observed.
- **Verification:** tests, checks, or manual steps that prove the result.

Use plain, concise language. Use one sentence for one idea. Prefer active voice. Explain unfamiliar terms when first used. Do not hide key reasoning in vague phrases such as "update the system" or "handle the logic".

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
- Design the code so that it's easily understandable for somebody with poor working memory.

## Plan language

Make sure the plan is easy to follow for somebody with zero context, or somebody who
hasn't read the current conversation.

The plan should explain how and why the code is simple, and how the code is designed to be
easy to interpret and understand.

The final plan should be written for an audience with poor working memory. It should
be concise. It should also use asd-ste100 language.
