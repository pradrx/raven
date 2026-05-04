---
description: Generate a new raven question + tests pair (validates inline)
---

You are generating a new practice problem for the raven repo.

**First, read `AGENTS.md` if you don't already have it in context this session.** That file is the canonical contract for slug rules, file layout, the path-style argument convention, JSON schema, validation rules, and don'ts. Do not skip it.

The user invoked: `/raven-new $ARGUMENTS`

Parse the arguments:
- The first whitespace-separated token is the path-style locator (`<folder>/<...>/<slug>` or just `<slug>`). If `$ARGUMENTS` is empty, abort and explain the expected form.
- Everything after the first whitespace, if any, is an inline free-form problem description.

The **last** segment of the locator is the slug; preceding segments form the folder. Call the joined relative path `<rel>` (e.g. for `leetcode/easy/two_sum`, `<rel>` is `leetcode/easy/two_sum` and the slug is `two_sum`).

## Steps

1. **Validate every segment.** Each segment must match `[a-z][a-z0-9_-]*`. Strip a leading `/` if present; reject trailing `/`, `..`, `.`, and empty segments. If anything fails, abort and explain.

2. **Check for slug collision.** Recursively walk `questions/` and `tests/`. If any file with stem == slug exists anywhere (even at a different folder), abort with the offending path and: "Slug `<slug>` is already used at `<offending-path>`." A spec at the **mirrored** path `specs/<rel>.md` is the expected case (see step 3) and not a collision; a spec at any *other* path with the same slug **is** a collision and aborts with: "Spec for slug `<slug>` lives at `<offending-path>`, not `specs/<rel>.md`. Either run `/raven-new <its-actual-folder>/<slug>` or move the spec to `specs/<rel>.md`."

3. **Resolve the problem description.** Three cases:
   - **Spec at the mirrored path** (`specs/<rel>.md` exists): read it. Use its contents as the canonical problem description. If inline arguments after the locator were also provided, print one warning line: `Spec file specs/<rel>.md detected — using it; inline description was ignored.` Then continue.
   - **No spec, inline description present**: use the inline text as the description.
   - **Neither**: abort with: "No spec file at `specs/<rel>.md` and no inline description. Run `/raven-spec <rel>` to scaffold a spec, or pass an inline description: `/raven-new <rel> <description>`."

4. **Create folders if needed.** `mkdir -p questions/<folder>` and `mkdir -p tests/<folder>` (no-op if folder is empty).

5. **Generate `questions/<rel>.py`** per the contract in `AGENTS.md` (Question file shape section):
   - Module docstring with the problem name as title, statement, and 1–2 illustrative examples that are NOT duplicates of any test case you'll write below. If a spec file is in use, prefer the examples from its `## Illustrative examples` section.
   - `def solve(...)` with body `pass`. Choose argument names that match the natural shape of the problem.
   - Helper data classes only if genuinely needed.

6. **Generate `tests/<rel>.json`** per the contract (Test file schema section):
   - `meta.difficulty`: pick `easy` / `medium` / `hard` (honor the spec's `## Difficulty hint` if present).
   - `meta.topics`: pick from the preferred vocabulary in `AGENTS.md` (honor the spec's `## Topics hint` if present).
   - `cases`: at minimum a baseline + an edge case + a tricky case. Most problems benefit from 5–8. If the spec lists `## Edge cases to cover`, every item there must be represented as a case.
   - Each case has `args` (positional list) and `expected`. Add `name` for distinctive cases.

7. **Generate a reference solution in your own context** — do NOT write it to disk. Implement `solve` mentally or in a Python tool call.

8. **Validate**: run the reference solution against every case (use a Python execution tool if you have one, otherwise reason through each case carefully). Confirm `actual == expected` for all of them.

9. **On validation pass**: report success in one line. Example:
   `Created questions/<rel>.py and tests/<rel>.json — 5 cases, difficulty=easy, topics=[arrays, hash-map].`

10. **On validation failure (any case mismatches)**: this means either your reference solution is wrong or the test data is wrong. Either is a bug in what you'd ship. **Delete the partially-written `questions/<rel>.py` and `tests/<rel>.json`**. Then `rmdir` any folder you created under `questions/` or `tests/` if it's now empty (walk upward until you hit a non-empty folder or the root). Do NOT touch `specs/<rel>.md` — leave it as-is so the user can iterate on the spec. Then tell the user which case failed, what the reference returned vs. expected, and ask whether they want you to retry.

## Don'ts (from AGENTS.md, repeated for emphasis)

- Don't write the reference solution to disk.
- Don't fill `solve`'s body — it stays `pass`.
- Don't put real test inputs in the docstring's illustrative examples.
- Don't overwrite an existing slug anywhere in the tree.
- Don't modify, archive, or delete `specs/<rel>.md` — that file belongs to the user. Validation rollback affects only `questions/` and `tests/` files (and any empty folders you created under those roots).
