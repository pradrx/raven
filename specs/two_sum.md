<!--
specs/two_sum.md

Edit the sections below, then run `/raven-new <slug>` to generate the
question + tests pair from this spec. Raven leaves this file alone
after generation; commit it as an audit trail or gitignore the
directory as you prefer.

Empty sections are fine — the agent falls back to its own judgment.
-->

# two_sum

## Problem
Given an array of integers `nums` and an integer `target`, return the
indices of the two numbers in `nums` that add up to `target`. Return them
as a list `[i, j]` with `i < j`.

Assume exactly one valid pair exists per input, and the same element
cannot be used twice.

## Constraints
- `nums` is a list of integers and may contain negatives, zeros, and duplicates.
- `target` is an integer.
- Exactly one solution is guaranteed — no need to handle the no-solution case.
- Aim for O(n) time; a nested-loop brute force is allowed but not the goal.

## Illustrative examples
- `nums = [1, 4, 7, 11]`, `target = 8` → `[0, 2]` (1 + 7)
- `nums = [10, 5]`, `target = 15` → `[0, 1]`

These are docstring-only. Hidden tests should use different inputs.

## Edge cases to cover
- Duplicate values where both copies form the pair (e.g., `[3, 3]`, target `6`).
- The two summands are not adjacent in the array.
- A value appears twice but only one of its indices participates in the answer.

## Difficulty hint
easy

## Topics hint
arrays, hash-map

## Notes
- Canonical solution: single-pass hash map of `value -> index`, checking for `target - value` on each step.
- Output indices must be 0-based and in ascending order.
