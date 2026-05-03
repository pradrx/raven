<!--
specs/valid_parens.md

Edit the sections below, then run `/raven-new <slug>` to generate the
question + tests pair from this spec. Raven leaves this file alone
after generation; commit it as an audit trail or gitignore the
directory as you prefer.

Empty sections are fine — the agent falls back to its own judgment.
-->

# valid_parens

## Problem
Given a string `s` containing only the bracket characters `(`, `)`, `{`,
`}`, `[`, `]`, return `True` if the brackets are balanced and `False`
otherwise.

A string is balanced when every opening bracket is closed by the same
type of bracket, brackets close in LIFO order, and every opener has a
matching closer. The empty string is balanced.

## Constraints
- Input is a string, possibly empty.
- The string contains only the six bracket characters listed — no
  whitespace, letters, digits, or other punctuation.
- Length is unbounded for the purposes of this exercise. Aim for O(n)
  time and O(n) space.

## Illustrative examples
- `s = "(){}"` → `True`
- `s = "(]"` → `False`
- `s = "(("` → `False`

## Edge cases to cover
- Empty string (balanced).
- Correctly nested mixed types, e.g., `"{[()]}"`.
- Interleaved but non-nested, e.g., `"([)]"` → `False`.
- A closer appearing before any opener, e.g., `")("`.
- Trailing unmatched closer, e.g., `"{[]}]"`.
- Unclosed opener(s), e.g., `"((("`.

## Difficulty hint
easy

## Topics hint
stack, strings

## Notes
- Canonical solution uses an explicit stack with a closer-to-opener map.
- A counter-only approach (just counting `(` vs `)`) is insufficient
  with mixed bracket types — tests should rule that shortcut out
  (e.g., `"([)]"` must fail).
