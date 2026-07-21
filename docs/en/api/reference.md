# API Reference

Signatures below are checked against the canonical `builtins.py` the game ships with its
official docs (51 definitions), and cross-referenced with the save-generated `__builtins__.py`
stub [kept in the repo](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/lib/__builtins__.py) for IDE autocomplete.
Functions cost in-game time ("ticks") unless noted otherwise.

## Movement & sensing

| Function | Returns | Summary |
|---|---|---|
| `move(direction)` | `bool` | Move one tile; the world wraps (torus). |
| `can_move(direction)` | `bool` | Whether moving that way is possible (maze walls!). |
| `get_pos_x()` / `get_pos_y()` | `int` | Drone coordinates. |
| `get_world_size()` | `int` | Side length of the (square) grid. |
| `get_entity_type()` | `Entity \| None` | What is under the drone. |
| `get_ground_type()` | `Ground` | `Grounds.Grassland` or `Grounds.Soil`. |
| `get_water()` | `float` | Water level 0–1 under the drone. |
| `measure(direction=None)` | varies | Sunflower → petals; treasure/maze → coordinates; cactus → size; dinosaur → type. |

## Farming

| Function | Returns | Summary |
|---|---|---|
| `harvest()` | `bool` | Harvest the entity under the drone. |
| `can_harvest()` | `bool` | Whether the plant is fully grown. |
| `plant(entity)` | `bool` | Pay the cost and plant under the drone. |
| `till()` | `None` | Toggle Soil ↔ Grassland. |
| `swap(direction)` | `bool` | Swap the entity under the drone with a neighbor — the key to cactus sorting. |
| `use_item(item, n=1)` | `bool` | Use `Items.Water`, `Items.Fertilizer` or `Items.Weird_Substance`. |
| `get_companion()` | `(Entity, (x, y)) \| None` | The plant's polyculture wish: which entity it wants planted where. |

## Economy & research

| Function | Returns | Summary |
|---|---|---|
| `num_items(item)` | `float` | Inventory count. |
| `get_cost(thing, level=None)` | `dict \| None` | Cost of planting/unlocking something. |
| `unlock(unlock)` | `bool` | Buy a node of the research tree from code. |
| `num_unlocked(thing)` | `int` | 1 + upgrade level (or 1/0 for non-upgradables). |

## Drones

| Function | Returns | Summary |
|---|---|---|
| `spawn_drone(task, *args)` | handle | Start another drone running `task`; extra `*args` are copied to it. `None` if at cap. |
| `wait_for(drone)` | value | Block until that drone finishes; returns its return value. |
| `has_finished(drone)` | `bool` | Non-blocking check. |
| `max_drones()` / `num_drones()` | `int` | Drone cap / currently active. |

## Leaderboards & simulation

| Function | Returns | Summary |
|---|---|---|
| `leaderboard_run(leaderboard, file_name, speedup)` | `None` | Start a timed, isolated leaderboard run of a file. |
| `simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)` | `float` | Run a headless simulation, returns elapsed time — perfect for strategy testing. |
| `get_time()` | `float` | Seconds since game start. |
| `get_tick_count()` | `int` | Ticks since execution start (free to call). |

## Utility & fun

| Function | Summary |
|---|---|
| `print(*x)` | Smoke puff above the drone (costs 1s) — `quick_print(*x)` is the free one. |
| `random()` | Float in `[0, 1)`. |
| `len` / `range` / `str` / `min` / `max` / `abs` | The usual suspects (some gated behind **Utilities**). |
| `set_execution_speed(speed)` / `set_world_size(size)` | Debug limiters (world min 3; resizing clears the farm). |
| `clear()` | Wipe the farm, return to (0,0), reset hat. |
| `change_hat(hat)` | Cosmetics — `Hats.Dinosaur_Hat` actually starts the dino minigame. |
| `do_a_flip()` / `pet_the_piggy()` | Essential. |

## Collections (lists, dicts, sets)

Called method-style, exactly as the official docs show them (`elements.append(x)`). Tick costs
are listed because they add up inside tight loops.

| Method | Returns | Cost | Summary |
|---|---|---|---|
| `list.append(x)` | `None` | 1 tick | Add `x` to the end of the list. |
| `list.insert(i, x)` | `None` | `1 + len(list) - i` ticks | Insert `x` at index `i`; later elements shift right. |
| `list.pop(i)` | removed value | `len(list) - i` ticks (1 if `i` omitted) | Remove and return the element at `i`; the last element if `i` is omitted. |
| `list.remove(x)` / `set.remove(x)` | `None` | list: comparisons + shifts; set: 1 tick | Remove the first element equal to `x`. |
| `dict.pop(key)` | removed value | 1 tick | Remove and return the value stored at `key`. |
| `set.add(x)` | `None` | 1 tick | Add `x` to the set. |

## Constant classes

- **`Items`** — `Hay`, `Wood`, `Carrot`, `Pumpkin`, `Cactus`, `Bone`, `Gold`, `Power`,
  `Water`, `Fertilizer` (−2s growth), `Weird_Substance` (turns a bush into a maze), `Piggy`.
- **`Entities`** — `Grass` (~0.5s → Hay), `Bush` (~4s → Wood), `Tree` (~7s, more wood, grows
  slower next to other trees), `Carrot` (~6s), `Pumpkin` (~2s, merges with neighbors, yield n³,
  1/5 die), `Dead_Pumpkin`, `Sunflower` (~5s → Power; 5× bonus at max petals ≥ 10),
  `Cactus` (~1s, sizes 0–9, chain-harvest when sorted, yield n²), `Hedge`, `Treasure`
  (gold = maze side length), `Apple`, `Dinosaur`.
- **`Grounds`** — `Grassland`, `Soil`.
- **`Unlocks`** — the research tree: `Loops`, `Variables`, `Operators`, `Functions`, `Lists`,
  `Dictionaries`, `Senses`, `Speed`, `Expand`, `Grass`, `Trees`, `Carrots`, `Pumpkins`,
  `Watering`, `Fertilizer`, `Sunflowers`, `Cactus`, `Mazes`, `Dinosaurs`, `Polyculture`,
  `Megafarm` (multi-drone), `Import`, `Simulation`, `Leaderboard`, `Auto_Unlock`, `Costs`,
  `Timing`, `Utilities`, `Debug`, `Debug_2`, `Hats`, `Top_Hat`, `The_Farmers_Remains`.
- **`Hats`** — cosmetics incl. trophy and `Golden_*` hats; `Dinosaur_Hat` is gameplay.
- **`Leaderboards`** — per-category boards with fixed goals, e.g. `Cactus` (33,554,432),
  `Cactus_Single` (131,072 on 8×8), `Maze` (9,863,168 gold), `Maze_Single` (616,448),
  `Dinosaur` (33,488,928 bones), `Fastest_Reset` (full automation from zero — the prestige board).
- **`Direction`** — `North`, `East`, `South`, `West` (globals).
