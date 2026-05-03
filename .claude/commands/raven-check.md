---
description: Re-validate a raven question + tests pair without modifying it
---

You are re-validating an existing pair. Useful after a hand edit, or when revisiting a question and wanting confidence the data is still consistent.

**Read `AGENTS.md`** if not in context.

The user invoked: `/raven-check $ARGUMENTS`

Parse as `<slug>` (single token). Strip surrounding whitespace.

## Steps

1. **Confirm the pair exists.** If either file is missing, abort with a clear message.

2. **Schema check on `tests/<slug>.json`** per `AGENTS.md`:
   - JSON parses.
   - `meta.difficulty` is `easy` | `medium` | `hard`.
   - `meta.topics` is a non-empty list of strings.
   - `cases` is a non-empty list; each case has `args` (list) and `expected`. `name` if present is a string. All values are JSON-serializable.

3. **Importability check on `questions/<slug>.py`**:
   - Module imports without error.
   - `solve` is defined and callable. (Its body may be `pass` — that's expected; this command does NOT verify the user's solution.)

4. **Reference solution agreement**:
   - Generate a reference solution for the question in your own context. Do NOT write it to disk.
   - Run it against every case.
   - Confirm `actual == expected` for every case.

5. **Report**:
   - On full pass: `OK — N/N cases agree with reference (difficulty=X, topics=[...])`.
   - On any failure: list each failing case (name or index, args summary, expected vs. actual from your reference), and say what kind of failure it is (schema, import, or reference-disagreement). Suggest `/raven-revise <slug> ...` to fix.

This command is read-only on disk. It MUST NOT modify any files.
