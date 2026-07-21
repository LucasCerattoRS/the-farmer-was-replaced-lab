# Drones

Everything past the early game is a multi-drone throughput problem. This page covers the
primitives (`spawn_drone`, `wait_for`, `has_finished`, `max_drones`) and the two patterns
built on top of them that appear in nearly every script in `farms/`.

## The primitives

| Function | Behavior |
|---|---|
| `spawn_drone(function)` | Spawns a new drone **at the position of the spawning drone**, running `function`. Returns a handle, or `None` if you're already at the drone cap. Costs 200 ticks if a drone was spawned, 1 otherwise. |
| `wait_for(drone)` | Blocks until `drone` finishes, then returns whatever its function returned. 1 tick if already done. |
| `has_finished(drone)` | Non-blocking finished check — `True`/`False`. Use it to poll workers while doing other work. |
| `max_drones()` / `num_drones()` | Cap / currently-active count. |

## Spawn position inheritance

The single most important fact: **a spawned drone starts exactly where its spawner is
standing.** There is no "spawn at (x, y)" call — you get there by *walking the spawner to
the right tile before calling* `spawn_drone`. Every deployment loop in this repo is a
variation of:

```python
for n in range(1, num_workers):
    target_x = n * cols_per_drone
    while get_pos_x() < target_x:
        move(East)
    spawn_drone(worker)
```

Because the worker inherits its spawn tile, it can find its own assigned region purely
from `get_pos_x()` / `get_pos_y()` at startup — no coordinates need to be passed as
arguments (functions passed to `spawn_drone` take no parameters).

## The column-split pattern

The workhorse pattern behind `sunflower_farm.py`, `pumpkin_megafarm.py`,
`carrot_polyculture_32x32.py` and most of `farms/crops/`: split an N-wide field into
`N / cols_per_drone` vertical stripes, one drone per stripe, each drone sweeping its
stripe with a boustrophedon (up-down-up-down) walk so it never needs a diagonal move:

```python
def worker():
    size = get_world_size()
    cols = 4
    x0 = get_pos_x()
    while True:
        for dx in range(cols):
            for _ in range(size):
                if can_harvest():
                    harvest()
                plant(Entities.Sunflower)
                move(North)
            move(East)
```

8 drones × 4 columns covers a 32×32 field with near-linear speedup over a single drone.
See [Tutorial 01 · Multi-Drone Farming](../tutorials/01-multi-drone.md) for the full
walkthrough.

## The boss-drone pattern

Some jobs need exactly **one** drone to own a piece of global state — e.g. deciding when a
fused mega-pumpkin is big enough to harvest. `pumpkin_megafarm.py` and
`pumpkin_megafarm_v2.py` dedicate the drone that stays at `(0,0)` to that check, while
every worker drone only replants dead tiles and never harvests the live mega-pumpkin
itself:

```python
def verificar_mega_abobora():
    # Runs exclusively at (0,0)
    if can_harvest():
        tamanho = measure()
        if tamanho != None and tamanho > ALVO_COLHEITA:
            harvest()
```

The boss loops its own field sweep like any worker, but only *this* drone calls
`measure()`/`harvest()` on the fusion tile — avoiding a race where two drones both decide
to harvest the same mega-pumpkin mid-fusion.

`wait_for()` and `has_finished()` generalize this into synchronization barriers: the
cactus sort scripts spawn one drone per row, `wait_for` all of them, *then* spawn one per
column for the next phase — see [Cactus Sorting](cactus-sorting.md#multi-drone-sorting-with-barriers).

## Pitfalls learned the hard way

1. **`spawn_drone` returns `None` at the drone cap.** Every deployment loop should check
   the return value (or check `num_drones() < max_drones()`) before assuming a worker
   exists — appending `None` to a drone list and later calling `wait_for(None)` breaks.
2. **The world is a torus.** `move()` wraps at the edges instead of failing. A worker
   whose loop bound is off by one, or that loops on `while can_move(...)` instead of a
   fixed `range(size)`, will walk straight into a neighboring drone's stripe and corrupt
   it. Every column-split worker above bounds its inner loops by `get_world_size()`, never
   by a movement-success check.
3. **Water/fertilizer are per-tile.** A drone only affects the tile it's standing on —
   there's no area-of-effect, so coverage math (how many tiles per drone, how often it
   revisits) has to account for water depleting on tiles a drone hasn't passed in a while.
4. **Functions passed to `spawn_drone` take no arguments.** To parameterize a worker (e.g.
   "start at column N"), scripts either read `get_pos_x()` at startup (inheritance trick
   above) or build the function dynamically — see the `make_runner(col)` closures in
   `pumpkin_megafarm_v2.py` and `sunflower_15petals.py`.

## Reference scripts

- [`farms/crops/sunflower_farm.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/crops/sunflower_farm.py) — clean 8-drone column-split, no boss.
- [`farms/crops/pumpkin_megafarm.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/crops/pumpkin_megafarm.py) — boss-drone pattern for fusion harvest.

See also: [Crops & Economy](crops.md) for what these drones are actually farming, and
[Simulation](simulation.md) to rehearse a drone deployment before running it live.
