---
name: implement
description: Implement a requested change after understanding the codebase and requirements.
---

# Implement

Use this skill when the user asks to implement a software change.

Read the relevant code, tests, documents, and requirements before you change files.
Trace the current behavior and identify the acceptance criteria, if any.

**Style rules**
- Make sure to add whitespace to code to divide up logical sections,
  and increase readability.
- Make sure control flow is explicit and written in if statements,
  rather than implied through other mechanisms like catch blocks or
  non-obvious behaviours.

**Implementation rules**
Make the smallest clear change that fulfills the requirements.

- Reuse existing code and patterns when they fit.
- Do not duplicate code without a clear reason.
- Name functions for what their bodies actually do.
- Use direct control flow, clear names, and small local responsibilities.
- Keep state changes and side effects easy to find.
- Write code that a reader with poor working memory can follow.

Verify the changed behavior with relevant tests or checks. State what you changed and how you verified it.
