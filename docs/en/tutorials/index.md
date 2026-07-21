# Tutorials

Step-by-step walkthroughs written to be **copy-paste ready for Steam guides**.
Each one is self-contained, uses real code from this repository, and avoids
site-specific formatting so it converts cleanly to BBCode:

```text
python tools/steam_bbcode.py docs/en/tutorials/01-multi-drone.md | clip
```

| # | Tutorial | You will learn |
|---|---|---|
| 01 | [Multi-Drone Farming](01-multi-drone.md) | The column-split pattern that multiplies any farm's throughput |
| 02 | [Cactus Sorting](02-cactus-sorting.md) | Chain harvesting via swap-sorts: insertion, shaker and "vacuum" |
| 03 | [Maze Gold Farming](03-maze-gold.md) | Wall-followers, DFS and `measure()`-guided treasure hunting |
| 04 | [The Dinosaur Apple Solver](04-dinosaur-apple.md) | Two-stage apple chasing, and knowing when to stop chasing |
| 05 | [Polyculture Optimization](05-polyculture.md) | A shared request queue across 8 drones — and the two bugs it had to fix |
| 06 | [Seed Hunting with `simulate()`](06-seed-hunting.md) | Turning `simulate()` into a fitness function you can optimize |

Not covered here but worth reading directly: the language's sharp edges are collected on
[Language Quirks & Gotchas](../mechanics/language-quirks.md).
