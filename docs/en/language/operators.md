# Operators

Three families, all lifted from Python, all constrained by the [floats-only rule](values-and-variables.md#everything-numeric-is-a-float).
The official reference lists them; this page adds the precedence, the honest gaps, and the
operators this repo actually leans on.

## Arithmetic: `+ - * / // % **`

Because every number is floating point, division is the one that catches people:

| Operator | Example | Result | Note |
|---|---|---|---|
| `+` `-` `*` | `2 * 3` | `6` | addition, subtraction, multiplication |
| `/` | `5 / 2` | `2.5` | **always a float** |
| `//` | `5 // 2` | `2` | floored division — what you want for indices and columns |
| `%` | `5 % 2` | `1` | remainder; `-2 % 6` folds negatives back into range |
| `**` | `2 ** 10` | `1024` | power; `(-5) ** 3` is `-125` (the parens matter) |

`%` earns its keep across the repo: `hats[get_pos_x() % 5]` cycles hats by column in
`hat_parade.py`, and every multi-drone deployment maps a drone index to a field stripe with
`//` and `%`.

## Comparison: `== != < <= > >=`

Each returns `True` or `False`. `==` and `!=` compare **any** values, enums included —
`get_entity_type() == Entities.Pumpkin` is the backbone of every sense-and-act loop. The four
orderings (`< <= > >=`) are defined on **numbers only**.

## Logic: `not and or`

Standard boolean combination: `not` inverts, `and` is true only if both sides are, `or` is true
if either side is.

!!! warning "Two things the official docs do *not* promise"
    **Short-circuit evaluation is unspecified.** Python skips the right side of `a and b` when
    `a` is false; the game's docs never state that it does the same. Don't write
    `can_move(d) and move(d)` assuming `move` is skipped — treat both sides as evaluated until
    you've confirmed otherwise in-game.

    **Truthiness of non-booleans is unspecified.** Stick to real boolean conditions
    (`n > 0`, `x in s`) rather than relying on `if some_list:` meaning "non-empty".

    When a mechanism isn't documented, this repo's rule is to *not* depend on it — see the
    [project ground rules](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/ROADMAP.md).

## Precedence

The official docs describe the language as a Python subset but don't print a precedence table.
It matches Python's: `**` binds tightest, then unary `-`, then `* / // %`, then `+ -`, then the
comparisons, then `not`, then `and`, then `or`. The docs' own `(-5) ** 3` example shows why you
parenthesize when unsure — without the parens the `-` and `**` fight over `5`.

---

Next: [Control Flow](control-flow.md) — putting conditions to work · back to
[Values & Variables](values-and-variables.md).
