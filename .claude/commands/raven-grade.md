---
description: Critique the user's solve for a raven question (does NOT peek at tests)
---

You are reviewing the user's solution to a problem after they've worked on it.

**Hard rule: you MUST NOT read `tests/<slug>.json`.** The grade should reflect general code quality and reasoning, not "did your code happen to pass these specific cases". The harness already tells the user pass/fail via `./raven run <slug>`; your job is the qualitative review.

The user invoked: `/raven-grade $ARGUMENTS`

Parse as `<slug>` (single token).

## Steps

1. **Read `questions/<slug>.py`** — including the docstring (so you know the problem) and the user's current `solve` implementation.

2. **If the conversation has recent `./raven run <slug>` output**, you may reference it. Otherwise, do not run the harness yourself; this is a code review, not a test runner.

3. **Critique along these axes**:
   - **Correctness reasoning**: walk through the algorithm. Does it handle the edge cases the docstring implies? Off-by-ones? Empty input? Negative numbers? Duplicates? Identify any cases that look unhandled, but **do so from the problem statement, not from peeking at tests**.
   - **Time/space complexity**: state Big-O for the user's solution. Is there a better-known asymptotic for this problem? If so, name it without writing the better solution unless asked.
   - **Style**: naming, structure, early returns, redundant work, idiomatic Python.
   - **Robustness**: input validation that's missing or unnecessary. Defensive checks that aren't earning their keep.

4. **Output shape**:
   - One short paragraph of overall assessment.
   - A bulleted list of specific observations, each with a file:line reference where possible (e.g., `questions/two_sum.py:23 — the inner loop runs even after a match is found`).
   - End with one concrete recommendation if there's an obvious next step.

5. **What to never do**:
   - Don't read `tests/<slug>.json`. Don't reference test cases by content.
   - Don't write a full corrected solution unprompted. Point at issues; let the user fix.
   - Don't grade as pass/fail — that's the harness's job.
