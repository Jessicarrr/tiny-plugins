---
name: clarify
description: Remove unclear requirements from a feature, refactor, or other change before implementation.
---

# Clarify

Use this skill when a change request has unclear requirements.
The goal is a clear and unambiguous set of requirements.

## Process

1. Inspect the available files first. Review relevant code, documents, tests, and configuration.
2. Write down what is known. Separate facts, assumptions, and unknowns.
3. Ask 3 or 4 questions in each round. Group related questions together.
4. For each question, explain why the answer is needed. Give a recommended path forward.
5. Use the user's answers to update the facts and decisions. Inspect more files when needed.
6. Repeat until no important requirement is unclear.

## Context

When you write the work down, write it for a contextless reader.

Assume the reader has not seen the conversation. Start with a short description of the thing being changed. Explain the current state, the problem, and the desired result. Define key terms.

## Finish

Clarification is complete when these items are clear:

- the goal and user need
- the scope
- the required behavior
- constraints and non-goals
- acceptance checks

End with a short, standalone decision record. Include the final requirements, decisions, assumptions, open risks, and acceptance checks. If important ambiguity remains, continue asking questions.
