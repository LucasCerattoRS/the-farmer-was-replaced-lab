# farms/ — curated code collection

Real, working scripts from an end-game save (billions farmed, all techs unlocked).
Imported and kept in sync via [`tools/sync_save.ps1`](../tools/sync_save.ps1);
name mapping lives in [`tools/sync_map.json`](../tools/sync_map.json).
Exact duplicates in the save (leaderboard working copies) were deduplicated.

## basics/
| File | Description | Stage |
|---|---|---|
| `plant_helpers.py` | Reusable `plant_*` helpers for every crop | early/mid |
| `pumpkin_solo.py` | Single-drone 32×32 pumpkin sweep | mid |
| `experiments/*` | Didactic toys: error demo, stack overflow, circular imports, hat parade, flips | — |

## crops/
| File | Description | Stage |
|---|---|---|
| `pumpkin_megafarm.py` / `_v2.py` | 8-drone 32×32 pumpkin fusion with a boss drone checking the mega-pumpkin | mid/late |
| `pumpkin_megafarm_v3.py` | Minimal column-split variant: drones joined with `wait_for()` instead of a busy-wait, fusion detected by comparing two `measure()` ids | mid/late |
| `sunflower_farm.py` | 8-drone Power farming by column stripes | mid/late |
| `sunflower_15petals.py` | Genetic rerolling for the 15-petal 5× bonus | late |
| `sunflower_power_simple.py` | Minimal per-column Power farm | mid |
| `carrot_polyculture.py` / `carrot_polyculture_32x32.py` | Companion-driven carrot farms (`get_companion`) | late |
| `hay_polyculture.py` | Companion-driven hay farm (grass with carrot companions) | late |
| `weird_substance_polyculture.py` | Weird Substance production: plants whatever `get_companion()` asks for — grass, bush, tree or carrot — and harvests the substance that results | late |
| `cactus_insertion_sort.py` | Insertion sort per line | mid/late |
| `cactus_shaker_sort.py` | Bidirectional cocktail sort with shrinking bounds | mid/late |
| `cactus_vacuum_sort.py` | "Vacuum theory": empty tiles as −1, holes pushed aside | mid/late |
| `cactus_bubble_22x22.py` / `cactus_basic_22x22.py` | Earlier 22×22 iterations (with/without swap) | mid |

## mazes/
| File | Description | Stage |
|---|---|---|
| `treasure_wall_follower.py` | Hand-on-wall solver, 8 parallel mazes | late |
| `maze_gold_dfs.py` | Iterative DFS with path stack, per-drone direction permutations | end |
| `maze_gold_16drones_bfs.py` | Map-first BFS routing on a 4×4 grid of mazes | end |
| `gold_25drones.py` / `gold_25drones_alt.py` | 25 drones, 5×5 maze grid, ~45 re-rolls per treasure | end |
| `treasure_hunt_8drones_buy.py` | Wall-follower variant that checks its Weird Substance stock before each maze (the stub has no buy function) | late/end |
| `maze_5x5_25drones.py` | Grid saturated with static drones | late |
| `make_maze_snippet.py` | 3-line building block: bush + Weird Substance | late |

## dinosaur/
| File | Description | Stage |
|---|---|---|
| `apple_solver.py` | Two-stage "wavy" route for the apple minigame | late |
| `bone_snake_solo.py` | Single-drone zig-zag bone farming with tail cleanup | late |

## leaderboards/
| File | Description | Board |
|---|---|---|
| `fastest_reset.py` | Full automation from zero: unlocks the whole tech tree and farms every resource | Fastest_Reset |
| `cactus_cocktail_sort.py` | Competition cocktail sort (goal 33,554,432) | Cactus |
| `power_collector.py` | Cascading drone spawns for sunflower Power | Sunflowers |
| `bone_collector.py` | Serpentine bone collector with staged offsets | Dinosaur |
| `leaderboard_run.py` / `launcher.py` | Run orchestration | — |

## research/
| File | Description |
|---|---|
| `tick_costs.py` | Exact tick cost per operation (difference of two `get_tick_count()` reads) |
| `grow_times.py` | Real growth time per entity, from `plant()` to `can_harvest()` |
| `pumpkin_death_rate.py` | Death rate of single, isolated pumpkins |
| `sunflower_petals.py` | Petal distribution of freshly planted sunflowers |
| `cactus_chain.py` | Chain-harvest payout versus how sorted the field is |

Measurement kit for the Track 2 questions in the [`ROADMAP`](../ROADMAP.md); each script prints a table.

## lib/
`__builtins__.py` — the API stub the game generates. Point your IDE at it for
autocomplete; it is also the source of the [API Reference](../docs/en/api/reference.md).
