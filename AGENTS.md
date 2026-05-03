# AGENTS.md — Raven Contract

This is the canonical contract for any agent (Claude Code, API call, future-you) generating problems for the `raven` practice harness. Read this in full before invoking any `/raven-*` slash command.

## Purpose

Raven is a local LeetCode-style practice tool. Coding agents generate **questions** and **test cases**; a human user solves the questions and runs them against the hidden test cases. The harness is a dumb runner — all authoring, validation, hinting, and grading happen via slash commands that adhere to this contract.

## File layout

```
raven/
├── raven                       # CLI runner (run | list | show)
├── AGENTS.md                   # this file
├── CLAUDE.md                   # thin pointer to this file for Claude Code
├── questions/<slug>.py         # vanilla problem statement + boilerplate solve
├── tests/<slug>.json           # hidden test cases + metadata
├── templates/
│   ├── question.py.tpl         # canonical shape for a question file
│   └── tests.json.tpl          # canonical shape for a tests file
└── .claude/commands/*.md       # slash command definitions
```

The pair `(questions/<slug>.py, tests/<slug>.json)` MUST share the same `<slug>`. Both files exist or neither does.

## Slug rules

- Lowercase `snake_case`.
- ASCII letters, digits, and underscores only.
- Must start with a letter.
- Short and descriptive (`two_sum`, `edit_distance_variants`, `valid_parens`).
- Must not collide with an existing question. `/raven-new` aborts on collision.

## Question file shape (`questions/<slug>.py`)

Required:
- A module-level docstring containing:
  - The problem name as a title (`Two Sum`).
  - The problem statement.
  - One or two illustrative input/output examples that **must not be exact duplicates of any test case in `tests/<slug>.json`**. They are for the human to grok the shape; they are not test data.
- A single function `def solve(...)` whose body is `pass`.

Allowed:
- Helper functions or simple data classes (e.g., `ListNode`, `TreeNode`) defined ABOVE `solve`, only when the problem genuinely requires custom structures or input parsing.
- Imports from the Python standard library.

Forbidden:
- Test data, expected outputs, hidden cases.
- A real implementation in `solve` — its body is always `pass`.
- Third-party imports.

See `questions/two_sum.py` for the canonical example. The minimal shape lives at `templates/question.py.tpl`.

## Test file schema (`tests/<slug>.json`)

```json
{
  "meta": {
    "difficulty": "easy" | "medium" | "hard",
    "topics": ["arrays", "hash-map"]
  },
  "cases": [
    {"name": "baseline",       "args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
    {"name": "edge: empty",    "args": [[], 0],             "expected": []},
    {                          "args": [[3, 3], 6],         "expected": [0, 1]}
  ]
}
```

### Required fields
- `meta.difficulty`: exactly one of `"easy"`, `"medium"`, `"hard"`.
- `meta.topics`: a non-empty list of strings.
- `cases`: a non-empty list. Each case requires:
  - `args`: list of positional arguments to `solve`. Must be JSON-serializable.
  - `expected`: the expected return value of `solve(*args)`. Must be JSON-serializable.

### Optional fields
- `cases[*].name`: a short human-readable identifier, shown in failure output. Encouraged for any case where the failure mode is distinctive.

### Topics vocabulary

Free-form, but prefer this preferred set so `raven list --topic …` stays useful:
`arrays`, `strings`, `hash-map`, `linked-list`, `tree`, `graph`, `dp`, `recursion`, `two-pointers`, `sliding-window`, `binary-search`, `sorting`, `heap`, `stack`, `queue`, `bit-manipulation`, `math`.

Add a new topic only if a problem genuinely calls for one.

The minimal shape lives at `templates/tests.json.tpl`.

## Case coverage rules

Every test file must include, at minimum:

1. **A baseline case** — the simplest representative input.
2. **An edge case** — empty input, single element, minimum/maximum bounds, or whatever degenerate shape is meaningful for the problem. Skip only if the problem genuinely has no such edge.
3. **A tricky case** — distinguishes a correct solution from a plausible naive heuristic (duplicates, negative numbers, off-by-one boundaries, ordering quirks, etc.).

Three cases is the floor, not a target. Most problems benefit from five to eight.

## Validation contract

Every slash command that writes or modifies a question/tests pair MUST validate before declaring done:

1. **Schema** — `tests/<slug>.json` parses as JSON and matches the schema above (required fields present, types correct, enums respected).
2. **Importability** — `questions/<slug>.py` imports cleanly and defines a callable `solve`.
3. **Reference solution agreement** — the agent generates a reference solution in its own context (in chat, in a Python tool call, in scratch memory), runs it against every case, and confirms `actual == expected` for all of them.

The reference solution is **never written to disk**. It exists only long enough to validate the cases.

If validation fails, the command MUST roll back: either delete the partially-written files or restore the previous file contents. Do not ship broken pairs. Report the failure to the user with enough context to fix it (which case failed, what the reference returned, what was expected).

## Slash command catalog

All slash commands live in `.claude/commands/*.md`. Each command MUST follow the validation contract above when it writes files.

| Command | Args | Behavior |
| --- | --- | --- |
| `/raven-new` | `<slug> <description>` | Generate a new question + tests pair. Validates inline. Atomic rollback on failure. Aborts on slug collision. |
| `/raven-revise` | `<slug> <change description>` | Modify an existing pair (docstring, tests, or both). Re-validates. Atomic rollback to previous contents on failure. |
| `/raven-check` | `<slug>` | Re-validate an existing pair without changing it. Useful after manual edits. |
| `/raven-hint` | `<slug>` | Read-only. Tiered hint (nudge → approach → partial code). MUST NOT read `tests/<slug>.json`. |
| `/raven-grade` | `<slug>` | Read-only. Critique the user's `solve` (style, complexity, edge cases). MUST NOT read `tests/<slug>.json`. |

## CLI catalog

The `raven` script is a runner only. It does not author or validate.

| Command | Behavior |
| --- | --- |
| `raven run <slug>` | Import `questions/<slug>.py`, call `solve(*case.args)` for each case, report PASS/FAIL + summary. Exits 0 on all-pass, 1 otherwise. |
| `raven list [--difficulty X] [--topic Y]` | Print a table of slug / difficulty / topics. Filters AND together. Flags rows with missing meta. |
| `raven show <slug>` | Print the question's module docstring and `meta` block. Deliberately omits `cases`. |

## Don'ts

- Don't write reference solutions to disk under any name (`solutions/`, `_ref/`, etc.).
- Don't fill `solve`'s body. The user solves; agents generate problems.
- Don't add or modify cases without re-validating the pair end-to-end.
- Don't leak test contents in `/raven-hint` or `/raven-grade` output. Both commands MUST NOT read `tests/<slug>.json`.
- Don't put third-party imports in question files.
- Don't commit broken pairs. If you can't get validation to pass, delete the files and explain why to the user.
- Don't reuse a slug. Slugs are unique forever within the repo.
