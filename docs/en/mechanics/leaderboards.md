# Leaderboards

The end-game meta-layer: a fixed target for a resource (or, for `Fastest_Reset`, for full
automation), timed and run in isolation from your normal save.

## How `leaderboard_run` works

```python
def leaderboard_run(leaderboard: Leaderboard, file_name: str, speedup: float) -> None
```

Starts a **timed, isolated run** of `file_name` for the given `leaderboard`. `speedup` sets
the starting execution speedup (same scale as `set_execution_speed` — `1` is unboosted,
higher runs faster). It costs 200 ticks to start and returns `None` — the run itself
executes the named file from a clean slate appropriate to that leaderboard, and the timer
that matters for ranking runs independently of your live save.

```python
leaderboard_run(Leaderboards.Fastest_Reset, "full_run", 256)
```

`farms/leaderboards/launcher.py` in this repo is the entire launch script for a
`Fastest_Reset` attempt:

```python
leaderboard_run(Leaderboards.Fastest_Reset, "leaderboard_run", 1000)
```

— it just kicks off `leaderboard_run.py` (the actual automation) at max starting speedup.

## Every board and its goal

Straight from the `Leaderboards` docstrings in `__builtins__.py`:

| Leaderboard | Goal | Mode |
|---|---|---|
| `Fastest_Reset` | *"The most prestigious category. Completely automate the game from a single farm plot to unlocking the leaderboards again."* | — |
| `Cactus` | Farm 33,554,432 cacti | Multiple drones |
| `Cactus_Single` | Farm 131,072 cacti | Single drone, 8×8 farm |
| `Carrots` | Farm 2,000,000,000 carrots | Multiple drones |
| `Carrots_Single` | Farm 100,000,000 carrots | Single drone, 8×8 farm |
| `Dinosaur` | Farm 33,488,928 bones | Multiple drones |
| `Hay` | Farm 2,000,000 hay | Multiple drones |
| `Hay_Single` | Farm 10,000,000 hay | Single drone, 8×8 farm |
| `Maze` | Farm 9,863,168 gold | Multiple drones |
| `Maze_Single` | Farm 616,448 gold | Single drone, 8×8 farm |
| `Pumpkins` | Farm 2,000,000 pumpkins | Multiple drones |
| `Pumpkins_Single` | Farm 1,000,000 pumpkins | Single drone, 8×8 farm |
| `Sunflowers` | Farm 10,000 power | Multiple drones |
| `Sunflowers_Single` | Farm 10,000 power | Single drone, 8×8 farm |
| `Wood` | Farm 10,000,000,000 wood | Multiple drones |
| `Wood_Single` | Farm 500,000,000 wood | Single drone, 8×8 farm |

## Single vs. multi rules

Every category with a `_Single` counterpart runs on a fixed **8×8 farm with exactly one
drone** — no `Megafarm` throughput tricks, no column-splitting. The non-`_Single` version
of the same category runs on your full farm size with the full drone cap, and (except for
`Sunflowers`, where both variants share the same 10,000-power goal) targets a dramatically
higher number to compensate for the extra scale available.

This means single-drone and multi-drone strategies for the *same resource* are genuinely
different programs: a single-drone `Cactus_Single` run can't rely on the barrier-synchronized
row/column sort in [Cactus Sorting](cactus-sorting.md#multi-drone-sorting-with-barriers) —
it has to sort and chain-harvest with one drone on a much smaller board.

## Practical run structure

`farms/leaderboards/leaderboard_run.py` is the reference `Fastest_Reset` automation: it
detects a fresh run (`num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0`)
and, if so, drives `slowest_automation()` — a fixed sequence of `unlock_tech()` calls, each
of which farms whatever items `get_cost()` demands before spending them:

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # retry — get_cost() can drift as prices scale
```

If the file is run outside of `leaderboard_run`/`simulate` context (i.e. those unlock
counts are already non-zero), it prints a guard message instead of doing anything —
`slowest_automation()` assumes a clean slate and would corrupt a live save otherwise.

See also: [Simulation](simulation.md) — the recommended way to rehearse a leaderboard
attempt before spending a real `leaderboard_run()` slot, and
[Leaderboard Strategies](../guides/leaderboard-strategies.md) for per-board tactics drawn
from the scripts in `farms/leaderboards/`.
