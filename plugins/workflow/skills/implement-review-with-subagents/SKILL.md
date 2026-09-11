---
name: implement-review-with-subagents
description: Use Luna to implement a change and Terra to review it until no real issues remain. Use only when the user explicitly invokes this skill.
---

# Implement and Review with Subagents

Use this skill only when the user explicitly asks for it.

Read the relevant code, tests, documents, and requirements first.

1. Spawn `gpt-5.6-luna` with high reasoning effort.
   Ask it to use the workflow implement skill and make the smallest clear change.
   Say that it should prioritize making the code easy to understand for somebody with poor working memory.
2. When Luna finishes, spawn `gpt-5.6-terra` with medium reasoning effort.
   Ask it to use the workflow review skill and review the current diff.
3. If Terra finds no real issues, stop.
4. If Terra finds an issue, check that it is real and in scope.
5. Send real issues to Luna. Ask Luna to fix them and run the relevant checks.
6. Spawn Terra again after each fix.

Repeat steps 3–6 until Terra finds no real issues, or all findings are not real issues.

Ask Terra to report only actionable findings. Each finding must include its impact, location,
and a short recommendation.

Do not send non-issues to Luna. If a finding remains after a fix, ask Luna to explain why it
is not a real issue before you stop.

Keep the work within the user's request. Use clear code and existing repository patterns.
Report the changes, checks, and final review result.
