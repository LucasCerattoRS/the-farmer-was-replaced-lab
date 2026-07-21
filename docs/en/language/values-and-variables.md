# Values & Variables

The in-game language is a subset of Python with the batteries removed: the syntax is Python's,
but you only get the pieces the research tree has unlocked. This section documents that subset
from the ground up. Start here — it's what a value is, how names hold them, and the two things
that quietly surprise people (numbers are all floats; collections are shared by reference).

> Derived from the game's official `scripting/` docs (CC0) and cross-checked against the scripts
> in [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms).

## Everything numeric is a float

There is exactly one number type and it is floating point. `2`, `5`, `-125` are all floats.
The official operators doc states it outright, and it changes how you write code:

- `/` always yields a float: `5 / 2` is `2.5`, never `2`. When you want the floored integer —
  a list index, a column number — reach for `//` (`5 // 2` is `2`).
- Loop counters, coordinates and indices are floats that happen to hold whole values.
  `range()` and list indexing accept them because the value is whole, not because a separate
  `int` type exists.

The non-numeric values you'll meet: booleans (`True` / `False`), the constant enums
(`Entities.Pumpkin`, `Items.Hay`, `North` — catalogued in the [API reference](../api/reference.md)),
the occasional string (almost always a window name for `import` / `leaderboard_run`), and the
[collections](collections.md).

## Assignment binds a name to a value

`=` stores the value on its right under the name on its left:

```python
a = 5
b = can_harvest()      # stores whatever the call returned
```

`=` assigns; `==` compares and returns a bool. Confusing the two is the classic first bug, and
the official docs call it out by name.

Augmented assignment updates a name from its own current value — the engine of every hand-rolled
counter:

```python
i = 0
while i < a:
    do_a_flip()
    i += 1             # exactly i = i + 1
```

All of `+= -= *= /= %=` exist. Assignment operators require the **Variables** unlock.

## A name is declared by assigning to it

There is no separate declaration keyword. The first assignment creates the name. Reading a name
that was never assigned is a **runtime** error — there's no compile step to catch it ahead of
time, which is its own [gotcha](../mechanics/language-quirks.md#undefined-names-fail-at-runtime-not-before).
*Which* scope a name lives in — one function, or the whole program — is the subject of
[Functions & Scope](functions-and-scope.md).

## Reference semantics bite with collections

Numbers and booleans are copied on assignment. **Lists, dicts and sets are not** — assigning one
to a new name gives you a second name for the *same* object:

```python
a = [1, 2]
b = a
b.pop()
# a and b are BOTH [1]
```

This isn't a trap to avoid, it's the model to understand: it's exactly what makes a list shared
between drones actually shared. The full treatment is on [Collections](collections.md); tuples
opt out by being immutable.

## Comments, and the tooltip trick

`#` starts a comment that runs to end of line. One special case is worth memorising: **a comment
on the line directly above a `def` becomes that function's hover tooltip in-game.** Free,
built-in documentation for your own helpers.

```python
# Sweep one column top-to-bottom, harvesting.
def sweep_column():
    ...
```

## Seeing values: print vs quick_print

`print(x)` writes a smoke puff into the air above the drone *and* a line to the Output window;
it costs ~1s. `quick_print(x)` skips the air and only writes to Output — use it when dumping many
values in a loop. Together with breakpoints and step-by-step mode, these are the whole debugger.

---

Next: [Operators](operators.md) — how these values combine · [Control Flow](control-flow.md) —
how execution branches and loops.
