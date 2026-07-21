# Tutorial 01 · Multi-Drone Farming (the column-split pattern)

**Goal:** turn any single-drone farm into an N-drone farm with near-linear speedup.
**Requires:** Megafarm unlock (`spawn_drone`), Functions, Loops.

## The idea

One drone sweeping a 32×32 field walks 1024 tiles per pass. Eight drones, each owning a
**vertical stripe of 4 columns**, walk 128 tiles each — in parallel. Almost every end-game
farm in this repo (pumpkins, sunflowers, cacti, polyculture) is built on this one pattern.

## Step 1 — write the worker as a function of its position

The trick: a spawned drone starts **where the spawner is standing**. So the worker just
reads its own `get_pos_x()` and claims the columns from there.

```python
def worker():
    size = get_world_size()
    cols = 4  # columns per drone
    x0 = get_pos_x()
    while True:
        for dx in range(cols):
            for _ in range(size):
                if can_harvest():
                    harvest()
                if get_water() < 0.5:
                    use_item(Items.Water)
                plant(Entities.Sunflower)
                move(North)
            move(East)
```

## Step 2 — the spawner walks and plants drones

```python
def deploy():
    size = get_world_size()
    drones = []
    while get_pos_x() % 4 != 0:
        move(East)
    for i in range(min(max_drones(), size // 4)):
        d = spawn_drone(worker)
        if d != None:
            drones.append(d)
        for _ in range(4):
            move(East)
    return drones

deploy()
```

## Step 3 — coordination (optional but powerful)

- `wait_for(drone)` — block until a worker returns (e.g. "harvested my stripe once").
- `has_finished(drone)` — poll workers while a **boss drone** does global work.
  The pumpkin megafarm here uses a boss that only checks the mega-pumpkin at (0,0)
  while workers replant dead tiles.

## Pitfalls learned the hard way

1. `spawn_drone` returns `None` at the drone cap — always check before appending.
2. The world is a **torus**: a worker that overshoots its stripe corrupts a neighbor's
   stripe. Keep loops bounded by `size`, never by `while can_move(...)`.
3. Water sharing: neighboring tiles equalize; watering every other tile is nearly as
   good and half the cost.

Full working examples in the repo: `farms/crops/sunflower_farm.py`,
`farms/crops/pumpkin_megafarm.py`, `farms/crops/carrot_polyculture_32x32.py`.
