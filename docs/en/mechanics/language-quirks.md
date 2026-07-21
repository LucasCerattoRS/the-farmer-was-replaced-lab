# Language Quirks & Gotchas

The game's language looks like Python and mostly behaves like it — until it doesn't. Every
item on this page is demonstrated by a real file in
[`farms/basics/experiments/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/basics/experiments),
most of them only a few lines long. They are deliberately tiny: each one exists to prove
exactly one thing about the runtime.

## `import` takes a window name, not a path

This is the quirk that surprises everyone, and it is invisible until you try it.

Your code lives in **windows**, and a window's name *is* its module name. There is no
directory structure to import from, so `import` takes the literal name you typed on the
window's tab:

```python
# import_cycle_a.py — in-game this window is called "ImportZyklus"
def f0():
    import ImportzyklusZubehör
    ImportzyklusZubehör.f1()
f0()
```

Note what that means for this repository: the curated filenames here
(`import_cycle_a.py`, `import_cycle_b.py`) are **not** the names the code imports. The
imports still reference `ImportZyklus` / `ImportzyklusZubehör`, the original window names in
the save. Copy these files into your game and the import breaks unless your windows carry
those exact names — accents and capitalisation included.

The same applies to `leaderboard_run`, whose second argument is a window name. The repo even
keeps a version with the placeholder still in it:

```python
# launcher_v1.py
leaderboard_run(Leaderboards.Fastest_Reset, "NAME_OF_THE_WINDOW_WITH_THE_ABOVE_SCRIPT", 1000)
```

!!! warning "Rename a window, break every import"
    Nothing warns you. Renaming a window silently invalidates every `import` and every
    `leaderboard_run`/`simulate` call that referenced it, and you only find out at runtime.

## Circular imports

Two windows can import each other. `import_cycle_a.py` and `import_cycle_b.py` are the
minimal case — A imports B, calls into it, and B imports A right back:

```python
# A
def f0():
    import ImportzyklusZubehör
    ImportzyklusZubehör.f1()
f0()

# B
def f1():
    import ImportZyklus
    ImportZyklus.f0()
```

Both imports sit **inside** the functions rather than at the top of the file, which is what
keeps the cycle from resolving at load time. Run it and you get mutual recursion across two
files — which lands you squarely on the next quirk.

## Recursion has a stack limit

```python
# stack_overflow.py — the entire file
def stack_overflow():
    stack_overflow()

stack_overflow()
```

Three lines, one purpose: proving the interpreter has a finite call stack and telling you
what hitting it looks like. Worth knowing before you write a recursive maze solver — the DFS
solvers in `farms/mazes/` use an **explicit stack in a list** and an iterative loop instead
of recursion, and this is why.

The one place recursion is genuinely idiomatic here is retry-on-failure, where depth stays
tiny:

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # depth 1–2 in practice
```

## Undefined names fail at runtime, not before

```python
# error_demo.py
while True:
    pet_the_piggy()
    do_a_flip()
    change_hat(Hats.Brown_Hat)
    Make_Error()
```

`Make_Error()` does not exist. Nothing catches it until execution reaches that line — the
three calls before it run normally first. There is no compile step and no linting, so a typo
in a branch you rarely hit will sit there quietly until the one run where it matters.

Practical defence: exercise every branch at least once under
[`simulate()`](simulation.md) before trusting a script with a leaderboard attempt.

## `spawn_drone` at the cap returns `None` — harmlessly

```python
# hat_parade.py
def newHat():
    hats = [Hats.Gold_Hat, Hats.Golden_Cactus_Hat, Hats.Golden_Carrot_Hat,
            Hats.Golden_Sunflower_Hat, Hats.Golden_Tree_Hat]
    while True:
        move(North)
        change_hat(hats[get_pos_x() % 5])

while True:
    spawn_drone(newHat)
    move(East)
```

That outer `while True` never stops asking for drones. Once the cap is reached,
`spawn_drone` simply returns `None` every time and the loop keeps spinning without error.

Harmless here — but the moment you **store** those handles it stops being harmless:

```python
drones = []
for i in range(16):
    drones.append(spawn_drone(worker))   # may append None
...
for d in drones:
    wait_for(d)                          # wait_for(None) breaks
```

Check the return value, or check `num_drones() < max_drones()` first. This is the top entry
in [Drones → pitfalls](drones.md#pitfalls-learned-the-hard-way) for a reason.

## Closures are how you parameterize a drone

A function passed to `spawn_drone` **takes no arguments**. So how do you tell eight drones to
start on eight different columns? You build eight different functions.
`flip_party.py` is the minimal demonstration:

```python
def make_drone(offset):
    def drone_behavior():
        for step in range(offset):
            move(East)
        while True:
            do_a_flip()
    return drone_behavior

for i in range(number_of_drones):
    spawn_drone(make_drone(i))
```

`make_drone(i)` returns a fresh zero-argument function that has captured its own `offset`.
This is not a toy — it is exactly the pattern real farms use:

- `criar_runner(col)` in `carrot_polyculture_32x32.py` (see
  [Tutorial 05](../tutorials/05-polyculture.md))
- `make_runner(col)` in `pumpkin_megafarm_v2.py` and `sunflower_15petals.py`

The alternative, used just as often, is the [spawn position inheritance
trick](drones.md#spawn-position-inheritance): walk the spawner to the right tile first and let
the worker read `get_pos_x()` at startup. Closures win when the parameter isn't a position.

## `clear()` is the panic button

```python
# clear_only.py — the entire file
clear()
```

A one-line window whose only job is to be run manually when a farm has gone wrong. `clear()`
wipes the farm, returns the drone to `(0,0)` and resets the hat — which also means it is the
way out of a stuck dinosaur minigame.

Keeping it as its own window matters: when things are broken you want to click one thing, not
edit code under pressure.

!!! danger "It really does wipe the farm"
    `clear()` destroys a field mid-fusion or mid-sort without asking. So does
    `set_world_size()`, and so does every `Expand` upgrade — see
    [Progression](../guides/progression.md#stage-1-movement-and-soil).

## Quick reference

| Quirk | Demonstrated by |
|---|---|
| `import` uses the window name, not a path | `import_cycle_a.py`, `launcher_v1.py` |
| Circular imports work (imports inside functions) | `import_cycle_a.py` + `import_cycle_b.py` |
| Finite call stack | `stack_overflow.py` |
| Undefined names fail only at runtime | `error_demo.py` |
| `spawn_drone` returns `None` at the cap | `hat_parade.py` |
| Closure factories parameterize workers | `flip_party.py` |
| `clear()` resets farm, position and hat | `clear_only.py` |

See also: [Getting Started](../getting-started.md) for the language basics, and
[Drones](drones.md) for the coordination primitives these quirks most often bite.
