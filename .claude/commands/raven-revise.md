---
description: Modify an existing raven question or its tests (re-validates)
---

You are modifying an existing problem in the raven repo.

**Read `AGENTS.md`** if not in context. It's the contract for shape, schema, and validation.

The user invoked: `/raven-revise $ARGUMENTS`

Parse as `<slug> <change description>`:
- First whitespace-separated token is the slug.
- Everything after is the free-form change request.

If parsing fails, stop and tell the user the expected shape.

## Steps

1. **Confirm the pair exists.** If `questions/<slug>.py` or `tests/<slug>.json` is missing, abort with a clear message — they should run `/raven-new` instead, or check the slug.

2. **Read both files and remember their original contents.** You will need to restore them on rollback.

3. **Apply the requested change.** Common shapes:
   - "add a case for X" — append cases to `tests/<slug>.json`.
   - "tighten the docstring" / "rename the function arg" — edit `questions/<slug>.py`.
   - "make this medium instead of easy" — edit `meta.difficulty`.
   - "swap the tricky case" — replace cases.

   Stay conservative: don't change more than the user asked for. Don't rewrite the whole problem unless they asked.

4. **Generate a reference solution in your own context** for the (possibly updated) question. Do NOT write it to disk.

5. **Validate**: schema still matches `AGENTS.md`, `solve` still imports cleanly, reference passes every case.

6. **On validation pass**: report what changed in one or two lines.

7. **On validation failure**: **roll back** by overwriting `questions/<slug>.py` and `tests/<slug>.json` with the original contents you saved in step 2. Then tell the user what failed and propose a next step. Do not leave the pair in a half-revised state.

## Don'ts

- Don't widen scope. If the user says "add a case for empty input", don't also reword the docstring.
- Don't skip validation just because the change "looks safe".
- Don't write the reference solution to disk.
