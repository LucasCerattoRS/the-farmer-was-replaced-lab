# Control Flow

Branching and looping — the shape of every farm loop. All four constructs (`if`, `while`,
`for`, and the `break`/`continue` pair) behave as in Python, with one game-specific twist:
**infinite loops are fine.**

## `if` / `elif` / `else`

Run a block only when a condition is `True`; the docs describe `if` as "a `while` loop that
doesn't loop." `elif` is sugar for a nested `else: if`.

```python
if can_harvest():
    harvest()
elif get_entity_type() == None:
    plant(Entities.Carrot)
else:
    move(North)
```

## `while` — and why infinite loops are safe here

The `while` loop repeats its body while the condition holds. Unlike a normal Python runtime,
**an infinite loop will not freeze the game**: there's a delay between iterations, so
`while True:` just runs until you press Execute again. That is not a bug to avoid — it's the
standard top-level shape of a persistent worker:

```python
while True:
    if can_harvest():
        harvest()
    plant(Entities.Grass)
    move(North)
```

The spawner loops in `farms/` are all `while True: ... spawn_drone(...)`, and
[`hat_parade.py`](../mechanics/language-quirks.md#spawn_drone-at-the-cap-returns-none-harmlessly)
leans on exactly this to keep asking for drones forever.

## `for` and `range`

The `for` loop iterates a sequence, binding a variable to each element. A **range** is the
usual fixed-count sequence; lists, tuples, dicts and sets are all iterable too (see
[Collections](collections.md)).

```python
for i in range(get_world_size()):
    harvest()
    move(North)
```

`range(stop)`, `range(start, stop)` and `range(start, stop, step)` all exist. Bounding a sweep
by `range(get_world_size())` instead of by a movement check is the single most important habit
in multi-drone code — the world is a torus, so `while can_move(...)` walks straight into the
next drone's stripe. That pitfall is spelled out on [Drones](../mechanics/drones.md#pitfalls-learned-the-hard-way).

## `break` and `continue`

`break` exits the innermost loop immediately; `continue` skips to that loop's next iteration.
Both act on the **innermost** loop only.

```python
while True:
    if can_harvest():
        break          # stop waiting, move on
```

A `while not can_harvest(): pass` says the same thing — the official docs give exactly that
equivalence.

## Loops don't create a scope

A variable assigned inside a `for` or `while` is still visible after the loop — branches and
loops do **not** introduce their own scope. After `for i in range(3): pass`, `i` is `2`. This
matters enough that it lives on [Functions & Scope](functions-and-scope.md#loops-and-branches-dont-create-scope),
where scope is covered properly.

## No recursion for deep traversals

`for`/`while` are iterative by nature, which is deliberate here: the call stack is finite
(the [stack-limit gotcha](../mechanics/language-quirks.md#recursion-has-a-stack-limit)), so the
maze solvers in `farms/mazes/` run their depth-first search with an **explicit stack in a list**
and a `while` loop rather than recursion.

---

Next: [Functions & Scope](functions-and-scope.md) — naming blocks of this and controlling what
they can see.
