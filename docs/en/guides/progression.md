# Progression (early → end)

The tech tree is the game's real progression axis. Everything else — bigger farms, more
drones, exotic crops — is downstream of what you have unlocked and how fast your drone
runs. This guide is the roadmap: what to buy, in what order, and *why* each step is the
one that unblocks the next.

## How unlocking actually works

Three built-ins do all the work (full signatures on the
[API Reference](../api/reference.md#economy-research)):

- `get_cost(tech)` — a dict mapping `Items.*` to the amount required.
- `unlock(tech)` — attempts the purchase; returns whether it succeeded.
- `num_unlocked(tech)` — how many times you have bought it (`0` means "not yet").

The safe pattern, lifted straight from
[`farms/leaderboards/leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py):

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # prices scale — re-read the cost and try again
```

!!! warning "Why the retry matters"
    `get_cost()` is read **before** you farm, but prices scale as you buy. By the time a long
    farming loop finishes, the quoted cost can be stale and `unlock()` returns falsy. Never
    assume the purchase went through — branch on the return value and recurse.

## Two kinds of unlock

| Kind | Examples | Behaviour |
|---|---|---|
| **Language / tooling** | `Variables`, `Operators`, `Loops`, `Functions`, `Lists`, `Dictionaries`, `Utilities`, `Import`, `Senses`, `Costs`, `Debug`, `Debug_2`, `Timing`, `Simulation`, `Auto_Unlock` | One-time capability. Buying `Functions` lets you write `def`; there is nothing to upgrade. |
| **Content / upgrade** | `Plant`, `Grass`, `Trees`, `Carrots`, `Pumpkins`, `Sunflowers`, `Cactus`, `Dinosaurs`, `Mazes`, `Expand`, `Watering`, `Fertilizer`, `Speed`, `Megafarm`, `Polyculture`, `Leaderboard` | Repeatable. The first purchase unlocks the thing; every purchase after that is an upgrade — usually *"increases the yield and cost"*. |
| **Cosmetic** | `Hats`, `Top_Hat`, `The_Farmers_Remains` | Pure fun. `change_hat()` costs nothing you need. |

That split drives the whole strategy: **language unlocks are prerequisites, content unlocks
are investments.** You buy the former as soon as they appear because they gate what you can
express; you buy the latter when your current bottleneck says so.

## The stages

### Stage 0 — one tile, no movement

You have a single tile of grass and a `while True:` loop. Harvesting grass is free income
and the only income. The whole stage is about buying the language out of its cage —
`Variables`, `Loops`, `Functions`, then `Senses` so the drone can tell what it is standing
on, and `Plant` so it can put something there.

```python
while True:
    if can_harvest():
        harvest()
```

### Stage 1 — movement and soil

`Expand` is the pivotal early unlock: its docstring reads *"Expands the farm land and
unlocks movement."* Until you own it, the drone is a single tile with a program attached.

!!! danger "`Expand` clears the farm"
    Every `Expand` **upgrade** wipes the field. That is fine when it is a scripted step, but
    it means you should never buy `Expand` in the middle of a long fusion or sorting run —
    you will destroy the field you were about to harvest. Scripts that expand
    (see `unlock_tech()` above) re-read `get_world_size()` immediately afterwards.

With movement comes `Carrots` (your first soil crop, needs `till()`) and `Watering`.
Water is a per-tile level from `get_water()`; keeping it above ~0.5 is the cheapest growth
multiplier in the game — see [Water & Fertilizer](../mechanics/crops.md#water-fertilizer).

### Stage 2 — wood and raw speed

`Trees` unlocks the better wood plant, and `Grass` upgrades hay yield. Both feed the
unlock costs of everything later. Interleaved through all of this: **`Speed`**, which is
bought more often than any other tech in a real reset run (five times before the
leaderboard). Speed compounds with every loop you will ever write, so it is rarely wrong.

!!! tip "Trees fight each other"
    Trees grow **slower when adjacent to other trees**. `leaderboard_run.py`'s `farm_trees()`
    plants them on a `(get_pos_x() + get_pos_y()) % 2` checkerboard for exactly this reason —
    see [Crops & Economy](../mechanics/crops.md#the-full-list).

### Stage 3 — pumpkins and fertilizer

`Pumpkins` is the first **non-linear** yield in the game: adjacent mature pumpkins fuse, and
the harvest pays the number of fused pumpkins **cubed**. `Fertilizer` (−2 s of remaining
grow time, per tile) is what makes a big field finish before your patience does — it is
bought four times in the reference reset run.

This is also the first stage where *patience beats haste*: harvesting early locks in a small
linear yield. Full mechanic, including the ~1-in-5 death rate that leaves `Dead_Pumpkin`
blockers, in [Pumpkin fusion](../mechanics/crops.md#pumpkin-fusion).

### Stage 4 — `Megafarm`: the throughput cliff

`Megafarm` — *"Unlocks multiple drones and drone management functions"* — is the single
biggest jump in the game. One drone sweeping a 32×32 field is a serial loop; sixteen drones
splitting it by column is the same loop divided by sixteen.

Everything about spawn-position inheritance, the column-split pattern and the boss-drone
pattern lives in [Drones](../mechanics/drones.md#the-column-split-pattern), and
[Tutorial 01](../tutorials/01-multi-drone.md) walks it end to end. Read the
[pitfalls](../mechanics/drones.md#pitfalls-learned-the-hard-way) before your first multi-drone
farm, not after.

### Stage 5 — the non-linear crops

Now the yield rules start rewarding cleverness instead of scale:

| Unlock | What it really buys you |
|---|---|
| `Cactus` | `size²` per cactus, and the **chain-harvest rule** — a fully sorted field pays out as if harvested all at once. This turns farming into a sorting problem: [Cactus Sorting](../mechanics/cactus-sorting.md#the-chain-harvest-rule). |
| `Sunflowers` | `Items.Power`, the resource that fuels your speed doubling — plus the 15-petal 5× bonus exploited by `sunflower_15petals.py` ([petals](../mechanics/crops.md#sunflowers-power-petals)). |
| `Polyculture` | `get_companion()` — companion planting for a yield bonus. Worth it only once you can route drones by companion; see [when it beats monoculture](../mechanics/polyculture.md#when-polyculture-beats-monoculture). |

### Stage 6 — mazes and dinosaurs

`Mazes` turns Weird Substance into gold via hedge mazes with a treasure at the centre;
`Dinosaurs` turns apples into bones through a snake-style minigame. Both are *re-roll
economies* — the winning move is throughput of small attempts, not perfection on one:

- [Re-roll economics](../mechanics/mazes.md#re-roll-economics) and
  [why many small mazes beat one big one](../mechanics/mazes.md#scaling-many-small-mazes-beat-one-big-one).
- [Bone yields](../mechanics/dinosaurs.md#bone-yields) and the
  [apple/`measure()` mechanic](../mechanics/dinosaurs.md#apple-mechanics-and-measure).

### Stage 7 — `Leaderboard`

*"Join the leaderboard for the fastest reset time."* This is the finish line of a reset run
and the entry ticket to the whole end-game meta-layer —
[Leaderboards](../mechanics/leaderboards.md) and
[Leaderboard Strategies](leaderboard-strategies.md).

## The canonical minimum path

`slowest_automation()` in
[`leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py)
is a working, from-zero path to `Leaderboard` in **32 purchases** across 13 techs. Because
it is a `Fastest_Reset` script it takes the *minimum* route — a useful lower bound on what
progression actually requires:

| Tech | Times bought | Read as |
|---|---|---|
| `Speed` | 5 | Bought more than anything else; compounds with every loop. |
| `Fertilizer` | 4 | Grow time is the bottleneck once fields get big. |
| `Carrots` / `Watering` / `Trees` / `Expand` | 3 each | Land, water and the two staple income crops. |
| `Pumpkins` / `Grass` / `Cactus` / `Dinosaurs` | 2 each | One unlock + one upgrade. |
| `Plant` / `Mazes` / `Leaderboard` | 1 each | Pure gates. |

The order it buys them in (`Speed` → `Plant` → `Carrots` → `Speed` → `Watering` → `Trees` →
`Speed` → `Expand` ×2 → …) is worth reading in full: it alternates **capability** and
**throughput**, never letting either get far ahead of the other.

!!! note "What the minimum path skips"
    `slowest_automation()` never buys `Megafarm`, `Sunflowers`, `Polyculture` or any language
    tech — yet the script itself uses functions, dicts and `global` freely. A `Fastest_Reset`
    run resets the *farming* tree, not your ability to write code. In a normal save you will
    want all of those; in a reset run they are pure cost.

## Where this repo's scripts fit

| Stage | Scripts to read |
|---|---|
| early / mid | `basics/plant_helpers.py`, `basics/pumpkin_solo.py` |
| mid | `crops/sunflower_power_simple.py`, `crops/cactus_basic_22x22.py`, `crops/cactus_bubble_22x22.py` |
| mid / late | `crops/pumpkin_megafarm.py`, `crops/sunflower_farm.py`, the three cactus sorters |
| late | `crops/*_polyculture.py`, `crops/sunflower_15petals.py`, `mazes/treasure_wall_follower.py`, `dinosaur/*` |
| end | `mazes/maze_gold_dfs.py`, `mazes/maze_gold_16drones_bfs.py`, `mazes/gold_25drones.py`, all of `leaderboards/` |

Full annotated index in [`farms/README.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/README.md).

See also: [Simulation](../mechanics/simulation.md#use-cases) — rehearse an unlock order
headlessly with `sim_unlocks` before committing hours to it, and
[Leaderboard Strategies](leaderboard-strategies.md) for what to do once the tree is done.
