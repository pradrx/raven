---
description: Generate a new raven question + tests pair (validates inline)
---

You are generating a new practice problem for the raven repo.

**First, read `AGENTS.md` if you don't already have it in context this session.** That file is the canonical contract for slug rules, file layout, JSON schema, validation rules, and don'ts. Do not skip it.

The user invoked: `/raven-new $ARGUMENTS`

Parse the arguments as `<slug> <free-form description>`:
- The first whitespace-separated token is the slug.
- Everything after the first whitespace is the free-form problem description.

If the arguments don't fit that shape (no whitespace, empty, etc.), stop and tell the user the expected form: `/raven-new <slug> <description>`.

## Steps

1. **Validate the slug.** Lowercase snake_case, ASCII letters/digits/underscore, starts with a letter. If it doesn't match, abort and explain.

2. **Check for collision.** If `questions/<slug>.py` or `tests/<slug>.json` already exists, abort with: "Slug `<slug>` is already used. Pick a different slug or run `/raven-revise <slug> ...` to modify the existing one." Do NOT overwrite.

3. **Generate `questions/<slug>.py`** per the contract in `AGENTS.md` (Question file shape section):
   - Module docstring with the problem name as title, statement, and 1–2 illustrative examples that are NOT duplicates of any test case you'll write below.
   - `def solve(...)` with body `pass`. Choose argument names that match the natural shape of the problem.
   - Helper data classes only if genuinely needed.

4. **Generate `tests/<slug>.json`** per the contract (Test file schema section):
   - `meta.difficulty`: pick `easy` / `medium` / `hard` based on the problem.
   - `meta.topics`: pick from the preferred vocabulary in `AGENTS.md` first; add new topics only if necessary.
   - `cases`: at minimum a baseline + an edge case + a tricky case. Most problems benefit from 5–8.
   - Each case has `args` (positional list) and `expected`. Add `name` for distinctive cases.

5. **Generate a reference solution in your own context** — do NOT write it to disk. Implement `solve` mentally or in a Python tool call.

6. **Validate**: run the reference solution against every case (use a Python execution tool if you have one, otherwise reason through each case carefully). Confirm `actual == expected` for all of them.

7. **On validation pass**: report success in one line. Example:
   `Created questions/two_sum.py and tests/two_sum.json — 5 cases, difficulty=easy, topics=[arrays, hash-map].`

8. **On validation failure (any case mismatches)**: this means either your reference solution is wrong or the test data is wrong. Either is a bug in what you'd ship. **Delete the partially-written `questions/<slug>.py` and `tests/<slug>.json`** so nothing broken lands on disk. Then tell the user which case failed, what the reference returned vs. expected, and ask whether they want you to retry.

## Don'ts (from AGENTS.md, repeated for emphasis)

- Don't write the reference solution to disk.
- Don't fill `solve`'s body — it stays `pass`.
- Don't put real test inputs in the docstring's illustrative examples.
- Don't overwrite an existing slug.
