---
name: refactor
description: Plan refactors that make code easier for an unfamiliar developer to read and understand.
---

# Refactor

Use when the user wants a refactoring plan. Do not change code unless asked.

Inspect the relevant code and trace its main behavior. Propose behavior-preserving changes unless the user says otherwise.

Use this readability test while reviewing:

- Is the behavior's starting point easy to find?
- Do names describe what the code actually does?
- Can any part be expressed more directly or simply?
- Is the control flow obvious, or is it indirect?
- Could an unfamiliar developer understand the implementation from the code itself?

Explain the recommended changes concretely, state the behavior to preserve, and describe how to verify it.

## Top Priority

The code should be easy to read and follow, and should be broken down into
manageable pieces.
We should leave it simpler and easier to understand than before.\
The main goal is to make the code easily understandable to somebody with poor working memory.

## Proposal

When done, write a refactor proposal. The user may specify a specific place for it to go, for example
a document, an issue or ticket, or anywhere else. If they didn't specify, write it in chat.

The proposal should:
- Write the purpose of the refactor, including that it's for making the code easily understandable.
- Use whitespace to break up large blocks of text or dot points.
- Be divided into easily digestible pieces.
- Use specific code examples. Just mentioning files and methods and what they do is not enough.
- Use mermaid diagrams to help build understanding.
- Be detailed, so that the implementation doesn't miss the purpose of the change.
- Use simple language, active voice, and asd-ste100 language.
