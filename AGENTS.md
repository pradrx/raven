# AGENTS.md — Raven Contract

This is the canonical contract for any agent (Claude Code, API call, future-you) generating problems for the `raven` practice harness. Read this in full before invoking any `/raven-*` slash command.

## Purpose

Raven is a local LeetCode-style practice tool. Coding agents generate **questions** and **test cases**; a human user solves the questions and runs them against the hidden test cases. The harness is a dumb runner — all authoring, validation, hinting, and grading happen via slash commands that adhere to this contract.

## File layout

```
raven/
├── raven                          # CLI runner (run | list | show)
├── AGENTS.md                      # this file
├── CLAUDE.md                      # thin pointer to this file for Claude Code
├── questions/<rel>.py             # vanilla problem statement + boilerplate solve
├── tests/<rel>.json               # hidden test cases + metadata
├── specs/<rel>.md                 # OPTIONAL user-authored spec consumed by /raven-new
├── templates/
│   ├── question.py.template       # canonical shape for a question file
│   ├── tests.json.template        # canonical shape for a tests file
│   └── spec.md.template           # canonical shape for a spec file
└── .claude/commands/*.md          # slash command definitions
```

`<rel>` is the relative path under each of the three roots, **without extension**. It may be a bare slug at the root (e.g. `two_sum`) or include user-chosen folders (e.g. `leetcode/easy/two_sum` or `stripe/invoice_match_by_id`). Folders are organizational only — slugs (the file stem) are globally unique across the entire `questions/` tree.

`specs/<rel>.md` is optional. It exists when the user invoked `/raven-spec <rel>` to scaffold a richer description before generating. Once `/raven-new` runs, the spec file becomes inert — raven leaves it alone for the user to commit, gitignore, or delete.

### Mirror rule

The triple `(questions/<rel>.py, tests/<rel>.json, specs/<rel>.md)` MUST share the same `<rel>`.

- Question and test exist together at the mirrored path or neither does.
- Spec is optional, but if present it must live at the same `<rel>`.
- A question at `questions/leetcode/easy/two_sum.py` REQUIRES its test at `tests/leetcode/easy/two_sum.json` — a test under any other folder is a contract violation.

## Slug rules

- Lowercase. ASCII letters, digits, underscores, and hyphens only — pattern `[a-z][a-z0-9_-]*`.
- Must start with a letter.
- Short and descriptive (`two_sum`, `edit_distance_variants`, `contains-duplicate`).
- **Globally unique across the entire `questions/` tree.** Folder context does not disambiguate — `leetcode/two_sum` and `interview/two_sum` cannot coexist.
- Slugs are unique forever within the repo. Don't release a slug name back into the namespace by deleting and re-creating.

**Folder segments** (the parts of `<rel>` before the slug) follow the same character rules as slugs.

## Path-style argument convention

Slash commands and the runner accept locators in two equivalent forms:

- **Bare slug**: `two_sum`. The runner finds the file by walking `questions/` recursively.
- **Path-style**: `<folder>/<...>/<slug>`, e.g. `leetcode/easy/two_sum`. Last segment is the slug; preceding segments are the folder path.

Create-side commands (`/raven-spec`, `/raven-new`) **require** the path-style form when you want to place files in a subfolder; a bare slug means "create at the root of the appropriate directory".

Read-side commands (`raven run`, `raven show`, `/raven-revise`, `/raven-check`, `/raven-hint`, `/raven-grade`) accept either form. With path-style, the resolver verifies the slug actually lives at the requested folder and errors loudly otherwise — this is a typo guard.

## Question file shape (`questions/<rel>.py`)

Required:
- A module-level docstring containing:
  - The problem name as a title (`Two Sum`).
  - The problem statement.
  - One or two illustrative input/output examples that **must not be exact duplicates of any test case in `tests/<rel>.json`**. They are for the human to grok the shape; they are not test data.
- A single function `def solve(...)` whose body is `pass`.

Allowed:
- Helper functions or simple data classes (e.g., `ListNode`, `TreeNode`) defined ABOVE `solve`, only when the problem genuinely requires custom structures or input parsing.
- Imports from the Python standard library.

Forbidden:
- Test data, expected outputs, hidden cases.
- A real implementation in `solve` — its body is always `pass`.
- Third-party imports.

See `questions/example/two_sum.py` for the canonical example. The minimal shape lives at `templates/question.py.template`.

## Test file schema (`tests/<rel>.json`)

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

The minimal shape lives at `templates/tests.json.template`.

## Case coverage rules

Every test file must include, at minimum:

1. **A baseline case** — the simplest representative input.
2. **An edge case** — empty input, single element, minimum/maximum bounds, or whatever degenerate shape is meaningful for the problem. Skip only if the problem genuinely has no such edge.
3. **A tricky case** — distinguishes a correct solution from a plausible naive heuristic (duplicates, negative numbers, off-by-one boundaries, ordering quirks, etc.).

Three cases is the floor, not a target. Most problems benefit from five to eight.

## Validation contract

Every slash command that writes or modifies a question/tests pair MUST validate before declaring done:

1. **Schema** — `tests/<rel>.json` parses as JSON and matches the schema above (required fields present, types correct, enums respected).
2. **Importability** — `questions/<rel>.py` imports cleanly and defines a callable `solve`.
3. **Reference solution agreement** — the agent generates a reference solution in its own context (in chat, in a Python tool call, in scratch memory), runs it against every case, and confirms `actual == expected` for all of them.

The reference solution is **never written to disk**. It exists only long enough to validate the cases.

If validation fails, the command MUST roll back: either delete the partially-written files or restore the previous file contents. Do not ship broken pairs. Report the failure to the user with enough context to fix it (which case failed, what the reference returned, what was expected).

## Slash command catalog

All slash commands live in `.claude/commands/*.md`. Each command MUST follow the validation contract above when it writes files.

| Command | Args | Behavior |
| --- | --- | --- |
| `/raven-spec` | `<rel>` (path-style or bare slug) | Scaffold `specs/<rel>.md` from `templates/spec.md.template` for the user to edit. Recursively walks all three roots; aborts on slug collision anywhere. Does NOT generate a question. |
| `/raven-new` | `<rel> [<description>]` | Generate a new question + tests pair at the mirrored paths. If `specs/<rel>.md` exists, uses it (and warns if inline `<description>` was also given); otherwise uses inline `<description>`; aborts if neither is present. Validates inline; atomic rollback (and empty-folder cleanup) of the generated pair on failure (spec file is left alone). Aborts on slug collision anywhere in the tree. |
| `/raven-revise` | `<locator> <change description>` | Modify an existing pair (docstring, tests, or both). `<locator>` is a bare slug or path-style. Re-validates. Atomic rollback to previous contents on failure. |
| `/raven-check` | `<locator>` | Re-validate an existing pair without changing it. Useful after manual edits. |
| `/raven-hint` | `<locator>` | Read-only. Tiered hint (nudge → approach → partial code). MUST NOT read any file under `tests/`. |
| `/raven-grade` | `<locator>` | Read-only. Critique the user's `solve` (style, complexity, edge cases). MUST NOT read any file under `tests/`. |

## CLI catalog

The `raven` script is a runner only. It does not author or validate.

| Command | Behavior |
| --- | --- |
| `raven run <locator>` | Import `questions/<rel>.py`, call `solve(*case.args)` for each case, report PASS/FAIL + summary. `<locator>` is a bare slug or path-style. Exits 0 on all-pass, 1 otherwise. |
| `raven list [--difficulty X] [--topic Y]` | Print questions grouped by folder, with slug / difficulty / topics. Filters AND together. Flags rows with missing meta or mirror-rule violations (orphan question or orphan test). |
| `raven show <locator>` | Print the question's module docstring and `meta` block. Deliberately omits `cases`. |

## Don'ts

- Don't write reference solutions to disk under any name (`solutions/`, `_ref/`, etc.).
- Don't fill `solve`'s body. The user solves; agents generate problems.
- Don't add or modify cases without re-validating the pair end-to-end.
- Don't leak test contents in `/raven-hint` or `/raven-grade` output. Both commands MUST NOT read any file under `tests/`.
- Don't put third-party imports in question files.
- Don't commit broken pairs. If you can't get validation to pass, delete the files and explain why to the user.
- Don't reuse a slug. Slugs are unique forever within the repo, regardless of folder.
- Don't break the mirror rule. Question, test, and (if present) spec all share the same `<rel>`.
- Don't modify, archive, or delete `specs/<rel>.md`. That file belongs to the user — they wrote it, they own its lifecycle. `/raven-new`'s rollback only affects the generated `questions/` and `tests/` files (and any folders it created under those roots).
