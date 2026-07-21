# Leaderboard Strategies

Per-board tactics, drawn from the scripts in
[`farms/leaderboards/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/leaderboards).
For what each board *is* — goals, single vs. multi rules, how `leaderboard_run()` behaves —
start at [Leaderboards](../mechanics/leaderboards.md). This page is about how to actually
place well on them.

## Rehearse before you spend a run

The single highest-leverage habit: **never debug inside a real run.** `simulate()` exists
precisely so you don't have to.

```python
run_time = simulate("f1", Unlocks, {Items.Carrot: 10000, Items.Hay: 50}, {"a": 13}, 0, 64)
```

It takes the starting unlocks, the starting items, the starting globals, a `seed` and a
`speedup` — and **returns the time the run took**. That return value is the whole point: it
turns "is this algorithm better?" into a number you can compare.

Two consequences worth internalising:

- **Fix the `seed` and you get a fair A/B.** Maze layouts, pumpkin deaths and petal counts are
  all seeded. Comparing two sorting algorithms on different seeds compares luck; comparing
  them on the same seed compares code.
- **Vary the `seed` and you get variance.** A strategy that wins on seed 0 and dies on seed 7
  is a strategy that will eventually die on the leaderboard. Sweep a handful of seeds before
  you trust a number.

Details and caveats on [Simulation](../mechanics/simulation.md#use-cases); note especially its
[limits](../mechanics/simulation.md#limits).

## The launcher pattern

Keep the launcher and the run in **separate files**.
[`launcher.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/launcher.py)
in this repo is one line, and that is the entire idea:

```python
leaderboard_run(Leaderboards.Fastest_Reset, "leaderboard_run", 1000)
```

The run script never edits itself to change board or speedup; the launcher is the only knob.
That keeps the run file byte-identical between a `simulate()` rehearsal and the real attempt —
so what you measured is what you ran.

!!! warning "Guard your run script against your live save"
    A `Fastest_Reset` script assumes a clean slate. Pointed at a real save it will happily
    `clear()` your farm and start re-buying tech. `leaderboard_run.py` ends with a guard that
    refuses to run unless the tree really is empty:

    ```python
    if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
        slowest_automation()
    else:
        print("You need to call this script")
        print("from a 'leaderboard_run' or 'simulate'")
    ```

    Put this at the bottom of every from-scratch run file you write.

!!! tip "Target a number you will never reach"
    Both `power_collector.py` and `bone_collector.py` are invoked with `1000000000000` as their
    target. That is not a goal — it is "effectively infinite". The board's own goal is what
    stops the clock, so the script simply farms until the run ends. One less edge case to get
    wrong.

## `Fastest_Reset`

The most prestigious board: automate from a single plot back to unlocking the leaderboards.
The reference implementation is
[`leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py),
and its architecture is worth copying wholesale:

| Piece | Job |
|---|---|
| `slowest_automation()` | The script — 32 `unlock_tech()` calls in a fixed order. See [Progression](progression.md#the-canonical-minimum-path). |
| `unlock_tech(tech)` | Farm exactly what `get_cost()` demands, buy, **retry on failure** because prices drift. |
| `farm_item(item, num)` | Dispatch table: each item type routes to its own farming loop. |
| `get_resources_for(item, nb)` | Bulk-buys inputs ahead of time — `nb = max(ws**2, nb)` — so a field is planted in one pass instead of stalling mid-row. |
| `sow_tile(to_harvest, water, entity)` | The workhorse primitive. |

`sow_tile()` deserves the attention. It is **idempotent** — "make this tile be this plant",
whatever state it starts in:

```python
def sow_tile(to_harvest, water, entity):
    if (to_harvest and can_harvest()) or get_entity_type() != entity:
        harvest()
    if get_ground_type() != get_ground(entity):
        till()
    if water and num_unlocked(Unlocks.Watering) > 0 and get_ground_type() == Grounds.Soil:
        while get_water() < 0.5 and num_items(Items.Water) > 0:
            use_item(Items.Water)
    if get_entity_type() != entity:
        plant(entity)
```

Every farming loop in the file is then a two-line body: move, `sow_tile(...)`. No loop needs
to know what the tile was before. Build this primitive first and the rest of a reset run
writes itself.

!!! note "Two copies in this repo"
    [`fastest_reset.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/fastest_reset.py)
    and `leaderboard_run.py` are near-duplicates. `leaderboard_run.py` is the later working
    copy: it adds an explicit walk back to `(0, 0)` before the dinosaur loop (the fixed
    movement pattern only works from the origin) and rewrites the maze search to loop on
    `while get_entity_type() != Entities.Treasure` instead of on hedge detection. Diff them —
    the delta is a tidy case study in the two bugs these runs actually hit.

## `Cactus` — 33,554,432

[`cactus_cocktail_sort.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/cactus_cocktail_sort.py)
saturates the drone cap in **two phases**, and the barrier between them is the whole trick:

```python
while num_items(Items.Cactus) < 33554432:
    for i in range(max_drones()-1):
        spawn_drone(pro_cactus_vertical)
        move(East)
    pro_cactus_vertical()
    move_to(0, get_pos_y())
    while num_drones() > 1:
        pass                      # ← barrier: every column finished

    for i in range(max_drones()-1):
        spawn_drone(pro_cactus_gorizontal)
        move(North)
    pro_cactus_gorizontal()
    while num_drones() > 1:
        pass                      # ← barrier: every row finished
    harvest()
```

Why the barrier is mandatory: sorting columns and then rows only produces a globally sorted
field if **every** column finishes before **any** row starts. A drone that begins its row pass
early reads half-sorted data and permanently corrupts the ordering. See
[multi-drone sorting with barriers](../mechanics/cactus-sorting.md#multi-drone-sorting-with-barriers).

And note the payoff line: a **single `harvest()`** at the end. The
[chain-harvest rule](../mechanics/cactus-sorting.md#the-chain-harvest-rule) cascades through the
whole sorted field, so one call collects everything. Sorting *is* the farming.

## `Sunflowers` — 10,000 Power

[`power_collector.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/power_collector.py)
uses a **cascading spawn** instead of a central spawner loop. Each drone derives its own
identity from `num_drones()` and spawns the next one:

```python
def drone_worker():
    current_drone_id = num_drones()

    if current_drone_id != 1 and get_pos_x() != initial_world_size - 1:
        move(East)
    if current_drone_id != max_drones() and get_pos_x() != initial_world_size - 1:
        spawn_drone(drone_worker)

    while num_items(Items.Power) < target_quantity:
        if can_harvest():
            harvest()
        prepare_soil_and_plant(Entities.Sunflower)
        apply_fertilizer_and_water(False, False, True)
        move(North)
```

The recursion self-limits on two conditions — `max_drones()` reached, or the east edge hit —
so the field fills exactly once with no arithmetic to get wrong. It leans on
[spawn position inheritance](../mechanics/drones.md#spawn-position-inheritance): the child
starts where the parent stands, so "move east, then spawn" lays drones out one per column.

!!! tip "`Sunflowers` and `Sunflowers_Single` share a goal"
    Both want 10,000 Power — the only board pair that doesn't scale the target for the
    multi-drone version. That makes the *single* variant the genuinely harder placement, and it
    is where the 15-petal 5× bonus stops being a nice-to-have: see
    [sunflowers & petals](../mechanics/crops.md#sunflowers-power-petals) and
    `crops/sunflower_15petals.py`.

## `Dinosaur` — 33,488,928 bones

[`bone_collector.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/bone_collector.py)
is the most intricate script in the collection. Two things make it work:

**It feeds itself.** Apples cost cactus, so the run tops up its own input before each attempt
rather than assuming a stocked inventory:

```python
required_cacti = apple_cost[Items.Cactus] * (initial_world_size * initial_world_size)
if num_items(Items.Cactus) < required_cacti:
    collect_cactus_solo(required_cacti)
```

**It re-plans as the tail grows.** `stage1()` heads for the next apple (located with
`measure()`); `stage2()` falls back to a serpentine sweep. A running `offset` widens the
safety margin as `length` grows, and the script switches from targeted pursuit to pure
serpentine once the tail is long enough that chasing apples risks self-collision:

```python
if length > (threshold - 8) + (offset * (initial_world_size - 2)):
    offset += 1
if offset < initial_world_size / 16:
    stage1()
else:
    stage2()
```

`change_hat(Hats.Dinosaur_Hat)` enters the minigame; the run ends when `move()` returns
`False` — you hit your own tail — which the code latches into `close`. Mechanics on
[Dinosaurs](../mechanics/dinosaurs.md#apple-mechanics-and-measure).

## `Maze` — 9,863,168 gold

No dedicated leaderboard script here, but the end-game solvers in
[`farms/mazes/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/mazes)
are the material —
[`gold_25drones.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/mazes/gold_25drones.py)
is closest to a board run, with 25 drones on a 5×5 grid of mazes.

The strategic point is economic, not algorithmic: gold comes from *completed* mazes, so
throughput of small mazes beats depth on large ones, and re-rolling a bad layout is usually
cheaper than solving it. Read
[re-roll economics](../mechanics/mazes.md#re-roll-economics) and
[why many small mazes win](../mechanics/mazes.md#scaling-many-small-mazes-beat-one-big-one)
before optimising your solver — a better wall-follower on the right maze size beats a perfect
BFS on the wrong one.

## The `_Single` boards are different programs

Every `_Single` category runs on a fixed **8×8 farm with exactly one drone**. None of the
patterns above survive that: no cascading spawn, no barriers, no column split. You are writing
a genuinely different program that has to sort *and* chain-harvest, or route *and* collect,
serially on a small board. Budget for that rather than trying to degrade a multi-drone script
into it — see [single vs. multi rules](../mechanics/leaderboards.md#single-vs-multi-rules).

## Checklist before an attempt

1. Run it under `simulate()` on a **fixed seed**, then on several seeds.
2. Confirm the run file has a guard so it cannot touch your live save.
3. Confirm the launcher is a separate one-liner and the run file is unchanged since you measured it.
4. Set the target to something unreachable and let the board's goal end the run.
5. Check drone joins: every `spawn_drone()` wave needs a matching `while num_drones() > 1: pass`
   (or `wait_for()`) before the next phase.

See also: [Progression](progression.md) for getting the tree unlocked in the first place, and
[Drones](../mechanics/drones.md#pitfalls-learned-the-hard-way) for the coordination bugs that
cost the most runs.
