---
description: Generate a new raven question + tests pair (validates inline)
---

You are generating a new practice problem for the raven repo.

**First, read `AGENTS.md` if you don't already have it in context this session.** That file is the canonical contract for slug rules, file layout, JSON schema, validation rules, and don'ts. Do not skip it.

The user invoked: `/raven-new $ARGUMENTS`

Parse the arguments:
- The first whitespace-separated token is the slug. (If `$ARGUMENTS` is empty, abort and explain the expected form.)
- Everything after the first whitespace, if any, is an inline free-form problem description.

## Steps

1. **Validate the slug.** Lowercase snake_case, ASCII letters/digits/underscore, starts with a letter. If it doesn't match, abort and explain.

2. **Check for collision.** If `questions/<slug>.py` or `tests/<slug>.json` already exists, abort with: "Slug `<slug>` is already used. Pick a different slug or run `/raven-revise <slug> ...` to modify the existing one." Do NOT overwrite.

3. **Resolve the problem description.** Three cases:
   - **Spec file present** (`specs/<slug>.md` exists): read the file. Use its contents as the canonical problem description for the rest of this command. If inline arguments after `<slug>` were also provided, print one warning line: `Spec file specs/<slug>.md detected — using it; inline description was ignored.` Then continue.
   - **No spec file, inline description present**: use the inline text as the description.
   - **Neither**: abort with: "No spec file at `specs/<slug>.md` and no inline description. Run `/raven-spec <slug>` to scaffold a spec, or pass an inline description: `/raven-new <slug> <description>`."

4. **Generate `questions/<slug>.py`** per the contract in `AGENTS.md` (Question file shape section):
   - Module docstring with the problem name as title, statement, and 1–2 illustrative examples that are NOT duplicates of any test case you'll write below. If a spec file is in use, prefer the examples from its `## Illustrative examples` section.
   - `def solve(...)` with body `pass`. Choose argument names that match the natural shape of the problem.
   - Helper data classes only if genuinely needed.

5. **Generate `tests/<slug>.json`** per the contract (Test file schema section):
   - `meta.difficulty`: pick `easy` / `medium` / `hard` based on the problem (honor the spec's `## Difficulty hint` if present).
   - `meta.topics`: pick from the preferred vocabulary in `AGENTS.md` (honor the spec's `## Topics hint` if present).
   - `cases`: at minimum a baseline + an edge case + a tricky case. Most problems benefit from 5–8. If the spec lists `## Edge cases to cover`, every item there must be represented as a case.
   - Each case has `args` (positional list) and `expected`. Add `name` for distinctive cases.

6. **Generate a reference solution in your own context** — do NOT write it to disk. Implement `solve` mentally or in a Python tool call.

7. **Validate**: run the reference solution against every case (use a Python execution tool if you have one, otherwise reason through each case carefully). Confirm `actual == expected` for all of them.

8. **On validation pass**: report success in one line. Example:
   `Created questions/two_sum.py and tests/two_sum.json — 5 cases, difficulty=easy, topics=[arrays, hash-map].`

9. **On validation failure (any case mismatches)**: this means either your reference solution is wrong or the test data is wrong. Either is a bug in what you'd ship. **Delete the partially-written `questions/<slug>.py` and `tests/<slug>.json`** so nothing broken lands on disk. Do NOT touch `specs/<slug>.md` — leave it as-is so the user can iterate on the spec. Then tell the user which case failed, what the reference returned vs. expected, and ask whether they want you to retry.

## Don'ts (from AGENTS.md, repeated for emphasis)

- Don't write the reference solution to disk.
- Don't fill `solve`'s body — it stays `pass`.
- Don't put real test inputs in the docstring's illustrative examples.
- Don't overwrite an existing slug.
- Don't modify, archive, or delete `specs/<slug>.md` — that file belongs to the user. Validation rollback affects only `questions/<slug>.py` and `tests/<slug>.json`.
