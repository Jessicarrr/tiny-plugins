---
name: to-tickets
description: Create small, complete tickets from a plan, spec, or conversation. Each ticket states its blockers.
---

# To Tickets

Turn a plan, spec, or conversation into small, complete tickets.

Each ticket must deliver one working path through the system. It must state which other tickets block it.

## Process

### 1. Get context

Use the current conversation.

If the user gives a spec path, issue number, or URL, read its full content and comments.

### 2. Check the codebase

If needed, inspect the codebase to understand its current state.

Look for small refactoring work that makes the change easier. Create this work first.

### 3. Create tickets

Make tickets as vertical slices.

- Each ticket covers a complete path through the required layers, such as data, API, UI, and tests.
- Use code snippet examples if there are any in the original plan.
- Do not make tickets for only one layer unless that work is complete and useful on its own.
- Each completed ticket must be easy to demo or verify.
- Each ticket must fit in one fresh context window for a person who does not know the change.
- Put refactoring tickets before the work that needs them.
- Make sure the tickets don't lose detail from the overall plan. Implementers will read
  the tickets, not the plan itself, so the tickets should contain complete information
  on their own.
- Use short, clear ASD-STE100 language.

Do not omit any detail. Include code blocks if the original plan had any. This is not optional.
For writing tickets, you don't need to be concise. Ignore any previous instructions about being
concise.
For every ticket, list its blockers. A ticket with no blockers can start now.

### 4. Get approval

Show the proposed tickets as a numbered list. Include:

- **Title:** A short name.
- **Blocked by:** The tickets that must finish first, if any.
- **Description:** Plain English description of the ticket itself.
- **Detail:** What to do to achieve the ticket's goal. Include full detail, including any code snippets.
- **What it delivers:** The working user behaviour.

Don't miss any detail from the original plan. You don't need to be concise here.
Feel free to write tickets with a lot of text in them to express the full detail.
No detail should be compressed or missed from the plan.
Include code snippets if the original plan has any.
Revise the list until the user approves it.

### 5. Publish tickets

Publish approved tickets where the destination is clear from the conversation or repository.

If the destination is not clear, ask the user where to publish them.

Use native blocking links when the destination supports them. Otherwise, write blockers as text.

Use this template:

## Parent

Reference the parent issue when the source is an existing issue. Otherwise, omit this section.

## What to build

Describe the working behaviour from the user's view.

## Implementation detail

Give a guide for the implementation. Include code snippets if relevant.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- Reference each blocking ticket.
- Or write: `None (can start immediately)`.

Write tickets so a new person can understand and complete them.
