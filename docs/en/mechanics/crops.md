# Crops & Economy

Every plantable entity, straight from [`farms/lib/__builtins__.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/lib/__builtins__.py),
plus the economy notes that fall out of playing them at scale.

## The full list

| Entity | Ground | Avg. grow time | Yields | Notes |
|---|---|---|---|---|
| `Entities.Grass` | Grassland or Soil | ~0.5s | `Items.Hay` | Grows automatically on Grassland; harvesting is optional upkeep. |
| `Entities.Bush` | Grassland or Soil | ~4s | `Items.Wood` | The baseline wood plant; cheaper and faster than `Tree`. |
| `Entities.Tree` | Grassland or Soil | ~7s | `Items.Wood` (more than Bush) | Grows **slower when other trees are adjacent** — space them or accept the penalty (see the `(x + y) % 2` checkerboard in `leaderboard_run.py`'s `farm_trees()`). |
| `Entities.Carrot` | Soil | ~6s | `Items.Carrot` | Flat yield, no fusion — the polyculture companion bonus is what makes it interesting late-game. |
| `Entities.Pumpkin` | Soil | ~2s | `Items.Pumpkin` = n³ | See [pumpkin fusion](#pumpkin-fusion) below. |
| `Entities.Sunflower` | Soil | ~5s | `Items.Power` | See [sunflowers & petals](#sunflowers-power-petals) below. |
| `Entities.Cactus` | Soil | ~1s | `Items.Cactus` = n² | Chain-harvests when the field is sorted — full mechanic on the [Cactus Sorting](cactus-sorting.md) page. |
| `Entities.Dead_Pumpkin` | — | — | none | `can_harvest()` is always `False`; disappears when something new is planted over it. |

## Water & Fertilizer

- `get_water()` returns a `0`–`1` level under the drone; `use_item(Items.Water)` tops it up. Higher water accelerates growth — most end-game farms hold water above `0.5`–`0.75` as a floor.
- `Items.Fertilizer`: `use_item(Items.Fertilizer)` instantly cuts **2 seconds** off the remaining grow time of the plant under the drone. Cheap enough to spam on high-value crops (pumpkins, apples) where every second of grow time is throughput.
- Both are per-tile effects; a drone sweeping a field only waters/fertilizes the tile it's currently standing on.

## Pumpkin fusion

Pumpkins **merge with adjacent fully-grown pumpkins** into a single mega-pumpkin. Harvesting it yields `Items.Pumpkin` equal to **the number of fused pumpkins, cubed** (n³) — this is why megafarms exist: a fully-fused 32×32 field (1024 pumpkins) dwarfs anything a lone drone could farm tile-by-tile.

The catch: **about 1 in 5 pumpkins dies** on growing up, leaving a `Dead_Pumpkin` behind. Dead pumpkins are useless, block fusion, and must be cleared (planting something new over them removes them). Both `farms/crops/pumpkin_megafarm.py` and `pumpkin_megafarm_v2.py` run a **boss drone** that checks the mega-pumpkin's size at `(0,0)` via `measure()` while worker drones do nothing but replant dead tiles — see [Drones](drones.md) for the pattern.

!!! tip "Sizing the harvest"
    `pumpkin_megafarm.py` caps its target at 1,000,000 pumpkins (`ALVO_COLHEITA`) as a conservative trigger rather than waiting for a theoretical full-field fusion — a smaller, reliable harvest beats a giant one that occasionally misfires.

A third variant, `pumpkin_megafarm_v3.py`, is worth reading for contrast: it drops the boss drone entirely and joins its workers with `wait_for()` instead of a busy-wait loop, detecting fusion by comparing two `measure()` readings in `check_pumpkin()`. Sixty-one lines against the original's one hundred and sixty-four.

## Sunflowers, Power & petals

Sunflowers convert into `Items.Power` on harvest — the resource the drone burns automatically for its speed doubling. Each sunflower also has a **petal count**; `measure()` on a sunflower returns it. If you harvest a sunflower **at the maximum petal count, and at least 10 sunflowers exist**, you get a **5× bonus** on that harvest.

`farms/crops/sunflower_15petals.py` exploits this directly: it keeps re-planting and re-measuring every fresh sunflower, killing (harvesting) any that isn't a 15-petal roll, and only lets a 15-petal plant mature — turning every harvest in the field into a 5× payout instead of gambling on the bonus threshold naturally.

## Cactus (yield & chain rule)

Cacti come in **10 sizes (0–9)**. A lone harvest gives `size²` cactus. The real payout is the **chain-harvest rule**: harvesting one cactus recursively harvests every adjacent cactus that is in sorted order relative to it (ascending to the North/East, descending to the South/West). A fully sorted field pays out as if you harvested every cactus in it in one action. Full mechanic, all three sorting algorithms, and multi-drone coordination are covered in [Cactus Sorting](cactus-sorting.md).

## Economy notes

- **Grow time vs. yield density** drives which crop to farm at which stage: grass/hay is nearly free and used to bootstrap everything else; carrots and pumpkins are the mid-game bread-and-butter; cactus and sunflower payoffs only compound once you have the unlocks (`Cactus`, `Polyculture`) and multi-drone throughput to exploit their non-linear yield rules.
- Fusion/chain mechanics (pumpkin n³, cactus n²) mean **patience beats haste**: harvesting early locks in a small, linear yield. Letting a field fill and only harvesting once maximizes the exponent.
- Companion planting (`get_companion()`) changes the calculus further — see [Polyculture](polyculture.md) for when it beats a pure monoculture field.

See also: [Drones](drones.md) for the multi-drone farming pattern used by every crop script above, and [Simulation](simulation.md) for testing yield strategies headlessly before committing a real field.
