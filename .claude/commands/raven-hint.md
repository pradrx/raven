---
description: Tiered hint for a raven question (does NOT peek at tests)
---

You are giving the user a hint on a problem they're working on.

**Hard rule: you MUST NOT read `tests/<slug>.json`.** Reading it would let you tailor the hint to the specific test inputs, which defeats the practice. The hint must come from the docstring and your own knowledge of the problem domain.

The user invoked: `/raven-hint $ARGUMENTS`

Parse as `<slug>` (single token).

## Steps

1. **Read `questions/<slug>.py`** — only this file. The docstring tells you what the problem is.

2. **Look at the conversation history** to gauge how much help the user has already gotten:
   - First time asking for a hint on this slug → give the **nudge** tier.
   - Second time → give the **approach** tier.
   - Third time or beyond → give the **partial code** tier.

3. **Tier definitions**:
   - **Nudge**: a question or observation that points the user at the right concept without naming it. ("What invariant might let you avoid the nested loop?")
   - **Approach**: name the technique and sketch the high-level shape, without writing code. ("This is a classic two-pointer problem on a sorted array. Initialize one pointer at each end and move them inward based on the sum.")
   - **Partial code**: write a non-trivial scaffold with the core mechanic, leaving the body or edge handling for the user. Mark gaps with `# TODO: ...`.

4. **What to never do**:
   - Don't reveal specific test inputs or expected outputs (you don't know them — and you must not look).
   - Don't write a complete solution. The partial-code tier deliberately stops short.
   - Don't reference `tests/<slug>.json` in any way. Pretend it doesn't exist.

5. **Output one tier only.** Don't bundle nudge + approach + code in one message. Let the user re-invoke to escalate.
