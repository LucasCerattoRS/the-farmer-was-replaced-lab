# Functions & Scope

Functions name a block of code; scope decides which names that block can see. They're on one
page because the interesting patterns — closures, deliberate globals — live exactly where the
two ideas meet.

## Defining and calling

```python
def move_n(n, direction):
    for _ in range(n):
        move(direction)

move_n(10, North)
move_n(2, West)
```

`def name(params):` binds a function to `name`; `()` calls it. Parameters become local
variables holding the arguments. **`def` is an assignment** — the official docs are explicit
that you should read `def f():` as `f = <a new function>`. Like any assignment, it must run
*before* the call: calling a function above its own `def` is a runtime error.

## Return values, and returning several

`return` hands a value back. To return more than one, return a **tuple** and unpack it
([Collections](collections.md#tuples)):

```python
def bounds():
    return get_pos_x(), get_pos_y()

x, y = bounds()
```

## Default arguments

```python
def flip(times = 1):
    for _ in range(times):
        do_a_flip()

flip()      # 1
flip(5)     # 5
```

A parameter with a default can't be followed by one without — same rule as Python.

## Functions are values

A function is just another value, so you can store one, pass it, or return it. This is not a
curiosity — it's the mechanism behind [`spawn_drone(task)`](../mechanics/drones.md), which takes
a function to run, and behind the closure factory below.

```python
def repeat10(action, arg):
    for _ in range(10):
        action(arg)

repeat10(move, North)
repeat10(use_item, Items.Fertilizer)
```

## Closures parameterize a worker

A function defined inside another **captures** the outer function's variables. That's how this
repo hands each drone its own starting column when the task itself takes no argument to spare:

```python
def make_runner(col):
    def run():
        while get_pos_x() < col:
            move(East)
        # ... work this column forever
    return run

for c in range(0, size, cols_per_drone):
    spawn_drone(make_runner(c))
```

`make_runner(c)` returns a fresh zero-argument function that has captured its own `c`. Real
instances: `criar_runner(col)` in `carrot_polyculture_32x32.py`, `make_runner(col)` in
`pumpkin_megafarm.py` and `sunflower_15petals.py`, and the minimal
[`flip_party.py`](../mechanics/language-quirks.md#closures-are-how-you-parameterize-a-drone).
(The current game *also* accepts `spawn_drone(task, *args)`; the scripts here use closures
instead — the quirks page has the full story.)

## Scope: local by default

There is a global scope, and every function call gets its own local scope. Assigning a name
inside a function creates it **locally**, even when a global of the same name exists:

```python
x = 0
def f():
    x = 1      # a NEW local x, unrelated to the global
f()
# global x is still 0
```

That isolation is a feature: a helper can't clobber a global just by reusing a common name.

## The `global` keyword

To *write* the global from inside a function, declare it:

```python
WORLD_SIZE = 0
def setup():
    global WORLD_SIZE
    WORLD_SIZE = get_world_size()
```

This is how the shared config in `cactus_insertion_sort.py` (`global WORLD_SIZE`,
`MAX_DRONES`) and the polyculture wish-maps in `carrot_polyculture.py`
(`global companion_mapping`, `tree_mapping`) get populated once and read everywhere. Use it
sparingly — the official docs warn that leaning on globals is "the first step towards spaghetti
code," and in a multi-drone program a shared global is shared across drones.

## Loops and branches don't create scope

Only *functions* introduce a scope. A `for`/`while`/`if` does not, so names they assign survive:

```python
for i in range(3):
    pass
# i is 2 here
```

Handy for "find the last index that matched," surprising if you expected the loop variable to
vanish.

---

Next: [Collections](collections.md) — the shared, mutable data these functions pass around ·
[Modules & Imports](modules-and-imports.md) — scaling past one file.
