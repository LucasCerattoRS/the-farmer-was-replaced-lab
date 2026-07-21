# Tutorial 06 · Seed Hunting with `simulate()`

**Goal:** stop guessing whether a change made your farm faster, and start measuring it.
**Requires:** Simulation unlock, Dictionaries.

The API surface is documented on [Simulation](../mechanics/simulation.md). This page is the
*method* — how to turn `simulate()` into a measuring instrument.

## Why this exists

`simulate()` is the only function in the game that hands you back a **number you can
optimize**:

```python
run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
```

Everything else tells you about the world right now. This tells you how long a strategy
*took*. That makes it a fitness function, and a fitness function turns "I think the 4-column
split is better" into an experiment.

## Rule 1 — a fixed seed compares code, a random seed compares luck

Maze layouts, pumpkin deaths and sunflower petal rolls are all driven by `seed`. Run two
algorithms on two different seeds and the faster number might just be the luckier board:

```python
SEED = 12345

a = simulate("shaker_sort",    Unlocks, {}, {}, SEED, 64)
b = simulate("insertion_sort", Unlocks, {}, {}, SEED, 64)

quick_print("shaker:", a, " insertion:", b)
```

Same seed, same starting unlocks, same items — the only difference is the file. Now the
comparison means something.

## Rule 2 — then vary the seed, because one number is not a result

A strategy that wins on seed 12345 and dies on seed 7 will eventually die on the leaderboard.
Sweep a handful and look at the spread, not just the best:

```python
seeds = [1, 2, 3, 5, 8, 13, 21]
total = 0
worst = 0

for s in seeds:
    t = simulate("shaker_sort", Unlocks, {}, {}, s, 64)
    total += t
    if t > worst:
        worst = t
    quick_print("seed", s, "->", t)

quick_print("avg:", total / len(seeds), " worst:", worst)
```

!!! tip "Optimize the worst case, not the average"
    A leaderboard run is a **single** attempt. A strategy with a great average and a terrible
    worst case is a strategy that will hand you that worst case on the run that counted. When
    two candidates have similar averages, take the one with the tighter spread.

## Rule 3 — `sim_globals` parameterizes without editing the file

This is the part people miss. `sim_globals` injects values straight into the target script's
global scope, so you can sweep a parameter **without touching the script between runs**:

```python
best_time = None
best_cols = 0

for cols in [2, 4, 8]:
    t = simulate("sunflower_farm", Unlocks, {}, {"cols_per_drone": cols}, 999, 64)
    quick_print(cols, "cols ->", t)
    if best_time == None or t < best_time:
        best_time = t
        best_cols = cols

quick_print("best:", best_cols, "columns at", best_time)
```

The target script just needs to read `cols_per_drone` as a global instead of hardcoding `4`.
Keeping the file byte-identical across every run is what makes the comparison honest — and
it is the same reason the leaderboard launcher is a separate one-line file, see
[the launcher pattern](../guides/leaderboard-strategies.md#the-launcher-pattern).

## Actual seed hunting

Everything above tunes *your code*. Seed hunting is the other direction: hold the code still
and search for a **favorable board**.

```python
GOOD_ENOUGH = 300.0
found = []

for s in range(1, 200):
    t = simulate("full_run", Unlocks, {}, {}, s, 256)
    if t < GOOD_ENOUGH:
        found.append((s, t))
        quick_print("candidate seed", s, "->", t)
```

Two honest caveats:

- **`seed` must be a positive integer** — there is no unseeded mode. Every simulation is
  reproducible by construction, which is exactly what makes this work.
- **A seed that is lucky for one script is not lucky in general.** You are finding a board
  that suits *this* strategy's assumptions. Change the strategy and the search is void.

## Fitting it into a leaderboard attempt

`simulate()` and `leaderboard_run()` take the same `filename`/state shape on purpose. The
workflow that falls out of that:

1. Write the run script with its live-save guard (see
   [Leaderboard Strategies](../guides/leaderboard-strategies.md#the-launcher-pattern)).
2. `simulate()` it on a fixed seed while you iterate on the algorithm.
3. Sweep seeds to find the worst case, and fix that.
4. Sweep `sim_globals` to tune the parameters you left variable.
5. Only then spend a real `leaderboard_run()`.

Steps 2–4 cost nothing but ticks. Step 5 is the one you get judged on.

## Limits worth knowing before you trust a number

`simulate()` returns **only** the elapsed time — no trace, no intermediate state. If you need
to know *why* a variant was slower, instrument the target script itself with `quick_print`
(which is free) or feed it a flag through `sim_globals`. See
[Simulation → Limits](../mechanics/simulation.md#limits).
