---
name: refactor
description: Plan refactors that make code easier for an unfamiliar developer to read and understand.
---

# Refactor

Use when the user wants a refactoring plan. Do not change code unless asked.

Inspect the relevant code and trace its main behavior. Propose behavior-preserving changes unless the user says otherwise.

Prioritize code whose purpose, flow, ownership, state changes, and side effects are obvious. Prefer clear names, direct control flow, local responsibilities, and fewer unnecessary abstractions.

Use this readability test while reviewing:

- Is the behavior's starting point easy to find?
- Do names describe what the code actually does?
- Can any part be expressed more directly or simply?
- Could an unfamiliar developer understand the implementation from the code itself?

Explain the recommended changes concretely, state the behavior to preserve, and describe how to verify it.
