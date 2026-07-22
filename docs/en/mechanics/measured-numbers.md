# Measured Numbers

Most of this site describes *how* the game behaves. This page is about **what the numbers
actually are** — and it is deliberate about the difference between a number that came from a
primary source and a number somebody assumed.

Two statuses appear below:

| Status | Meaning |
|---|---|
| ✅ **Sourced** | Taken from the canonical `builtins.py` the game ships. Trustworthy now. |
| ⏳ **Pending** | A claim the site currently makes that has **never been measured**. The script that will measure it exists in [`farms/research/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/research); the number lands here after an in-game batch run. |

> Nothing on this page is estimated. If a number isn't measured yet, it says ⏳ and stays empty
> rather than getting a plausible-looking guess — the repo's
> [ground rules](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/ROADMAP.md)
> exist because a confident wrong answer already got published here once.

## ✅ Tick costs, complete

Every cost below is transcribed from the **canonical `builtins.py`** shipped with the official
CC0 docs (51 definitions) — not the smaller save-generated stub. This is the first place on the
site where the full cost table appears in one piece.

**Free — 0 ticks**

| Function | Note |
|---|---|
| `get_tick_count()` | The measuring instrument itself is free, so a `t1 - t0` difference is exact. |
| `get_time()` | See the [stub disagreement](#the-two-stubs-disagree-about-get_time) below. |
| `quick_print(*x)` | The reason to prefer it over `print` inside loops. |

**1 tick — sensing, inventory and cheap built-ins**

`can_harvest()` · `can_move(dir)` · `get_pos_x()` · `get_pos_y()` · `get_world_size()` ·
`get_entity_type()` · `get_ground_type()` · `get_water()` · `num_items(item)` ·
`get_companion()` · `measure(dir)` · `has_finished(drone)` · `max_drones()` · `num_drones()` ·
`get_cost(thing)` · `num_unlocked(thing)` · `random()` · `abs(x)` · `len(x)` · `str(x)` ·
`range(...)` · `list.append(x)` · `set.add(x)`

**200 ticks — always, no cheap path**

`till()` · `clear()` · `change_hat(hat)` · `set_execution_speed(s)` · `set_world_size(n)` ·
`simulate(...)` · `leaderboard_run(...)`

**200 ticks on success, 1 tick otherwise** — the two-price group. This is why a guarded
`if can_move(d): move(d)` is not automatically cheaper than a bare `move(d)` that fails.

| Function | Costs 200 when… |
|---|---|
| `harvest()` | an entity was actually removed |
| `plant(entity)` | the planting succeeded |
| `swap(direction)` | the swap succeeded |
| `use_item(item, n)` | an item was actually used |
| `move(direction)` | the drone actually moved |
| `spawn_drone(task)` | a drone was actually spawned (`1` at the cap) |
| `unlock(unlock)` | the purchase succeeded |

**Variable cost**

| Function | Cost |
|---|---|
| `list.insert(i, x)` | `1 + len(list) - i` ticks |
| `list.pop(i)` / `dict.pop(key)` | `1` tick with no index, or for a dict |
| `set.remove(x)` | `1` tick |
| `wait_for(drone)` | `1 +` the ticks remaining in that drone's task |

**Measured in seconds, not ticks**

`print(*x)` · `do_a_flip()` · `pet_the_piggy()` — each costs **1 second**. That's why
`quick_print` exists.

See [API Reference](../api/reference.md#collections-lists-dicts-sets) for the collection methods
in signature form.

## The two stubs disagree about `get_time()`

A concrete inconsistency worth knowing, found while assembling the table above:

| Source | Claimed cost of `get_time()` |
|---|---|
| Canonical `builtins.py` (shipped with the official docs, 2321 lines) | **0 ticks** |
| Save-generated `farms/lib/__builtins__.py` (1307 lines) | **1 tick** |

The canonical stub is the authority — it is the larger, official artifact, and the same file is
right about the five collection methods the save stub omits entirely. This page therefore lists
`get_time()` as free, and `tick_costs.py` measures it explicitly to settle the point in practice.

Practically it barely matters — but it does mean a timing loop built on `get_time()` doesn't
perturb the tick budget it's measuring, which is convenient for
[`grow_times.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/research/grow_times.py).

## The measurement kit

Five scripts in [`farms/research/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/research).
Each one prints a clean table to the Output window and nothing else — they are instruments, not
farms.

| Script | Targets | Method | Default N |
|---|---|---|---|
| `tick_costs.py` | The table above | Wraps each operation in `get_tick_count()` and compares to the documented cost. Sets up a known tile state first, because of the two-price group. | 1 each |
| `grow_times.py` | The `~0.5s / ~4s / ~7s` figures on [Crops](crops.md#the-full-list) | Times `plant()` → `can_harvest()` with `get_time()`, on an isolated tile, water held above 0.9 | 10 per entity |
| `pumpkin_death_rate.py` | "about 1 in 5 pumpkins dies" on [Crops](crops.md#pumpkin-fusion) | One pumpkin at a time on a lone tile (no fusion to corrupt the count); resolves to `Dead_Pumpkin` or `can_harvest()` | 200 |
| `sunflower_petals.py` | Whether the petal roll is uniform | `measure()` on each freshly planted sunflower, binned into a histogram | 300 |
| `cactus_chain.py` | The `size²` rule and the chain-harvest rule | Part 1 isolated cactus vs `size²`; Part 2 scores field sortedness, then compares payout to the summed `size²` ceiling | 8 fields |

!!! note "Why the sample sizes differ"
    `tick_costs.py` needs N=1 because tick costs are deterministic. The rate and distribution
    questions need hundreds of samples before the number means anything — a 20-pumpkin sample
    can easily show "1 in 4" for a true rate of 1 in 5.

## ⏳ Open questions awaiting numbers

These are live claims on this site with no measurement behind them yet.

| Claim | Where it's asserted | Status |
|---|---|---|
| Grass ~0.5s, Bush ~4s, Tree ~7s, Carrot ~6s, Pumpkin ~2s, Sunflower ~5s, Cactus ~1s | [Crops & Economy](crops.md#the-full-list) | ⏳ |
| "About 1 in 5 pumpkins dies on growing up" | [Crops & Economy](crops.md#pumpkin-fusion) | ⏳ |
| Petal counts run 1–15, implicitly uniform | [Crops & Economy](crops.md#sunflowers-power-petals) | ⏳ |
| A lone cactus yields `size²` | [Cactus Sorting](cactus-sorting.md) | ⏳ |
| A sorted field pays out as if fully harvested | [Cactus Sorting](cactus-sorting.md) | ⏳ |
| Trees grow slower adjacent to other trees | [Crops & Economy](crops.md#the-full-list) | ⏳ not yet scripted |
| Fertilizer removes exactly 2s of remaining grow time | [Crops & Economy](crops.md#water-fertilizer) | ⏳ not yet scripted |

**When a measurement contradicts one of those pages, the page gets corrected** and the
correction is logged in the roadmap — same as the Track 0 fixes.

## A second feed of open questions: the reference interpreter

The [Reference Interpreter](../language/reference-interpreter.md) generates its own list of holes.
Wherever the executable model has to consult a number the official sources never gave, it refuses
— and every such refusal is catalogued in
[`interpreter/UNSPECIFIED.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/interpreter/UNSPECIFIED.md).
Some overlap the table above (grow time, pumpkin death, petals); others the model surfaced on its
own — for example **harvest yield quantity**, which the docs give a *type* for but never a base
amount. Treat that file as a second, code-derived source of ⏳ items alongside `farms/research/`.

## Running the batch

The scripts only run **inside the game** — the language is a custom interpreter, so there is no
way to execute them from a shell. The batch is short:

1. Open the game and create a new window per script (the window name is the module name — see
   [Modules & Imports](../language/modules-and-imports.md)).
2. Paste one script in, press **Execute**, and let it finish. `pumpkin_death_rate.py` and
   `sunflower_petals.py` are the slow ones; both print partial results as they go, so they can be
   stopped early and still yield a usable N.
3. Copy the Output window contents.
4. The numbers replace the ⏳ rows above, each with its method, sample size and the script that
   produced it.

!!! warning "These scripts call `clear()` and `set_world_size()`"
    They wipe the farm and resize the world by design, so they start from a known state. **Don't
    run them on a save you care about** — use a scratch save, or accept that the field gets
    reset. `clear()` is documented on [Language Quirks](language-quirks.md#clear-is-the-panic-button).

## Sources

| Fact | Source |
|---|---|
| Every tick cost in the table above | Canonical `builtins.py`, `…\Languages\builtins.py` (shipped, CC0, 2321 lines, 51 defs) |
| The `get_time()` discrepancy | Same file vs. `farms/lib/__builtins__.py` in this repo |
| Measurement methods | The scripts themselves, in `farms/research/` |
