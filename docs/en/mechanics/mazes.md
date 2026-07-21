# Mazes & Gold

Mazes are the game's dedicated gold source: plant a bush, dose it with Weird Substance, and
what grows back is a maze of hedges hiding a treasure.

## Growing a maze

```python
plant(Entities.Bush)
substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
use_item(Items.Weird_Substance, substance)
```

This 3-line building block ([`farms/mazes/make_maze_snippet.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/mazes/make_maze_snippet.py))
appears, verbatim or near-verbatim, at the start of every maze script in the repo. The
Weird Substance dose scales with **field size** and **`Mazes` unlock level** — every level
of the `Mazes` unlock doubles the dose (and, per its own description, the gold inside).
`use_item(Items.Weird_Substance, n)` is the batched form of `use_item`: it spends `n` units
in one call instead of looping `use_item()` calls one at a time.

## Sensing inside the maze

- `can_move(direction)` — the wall sensor. Returns `False` if a `Hedge` blocks that
  direction, `True` if the tile is open (`move()` will succeed there).
- `get_entity_type() == Entities.Treasure` — how every solver recognizes it has arrived.
- `measure()` — on a `Treasure`, returns its `(x, y)` position, and (per the API stub)
  works **from anywhere in the maze**, not just standing on the treasure tile. This is what
  turns "wander until found" into "route directly to a known destination" for the more
  advanced solvers below.

## Re-roll economics

Once a treasure is harvested, re-applying Weird Substance to the same plot **re-rolls it
into a fresh maze** rather than requiring a brand new bush — the field itself doesn't need
to be cleared and replanted between treasures. `farms/mazes/gold_25drones.py` exploits this
directly: each of 25 drones sits on a shared 5×5 maze grid and loops
`harvest → use_item(Weird_Substance, 160) → repeat`, counting re-rolls and only calling the
(more expensive) `harvest()` on the *45th* pass:

```python
if get_entity_type() == Entities.Treasure:
    use_item(Items.Weird_Substance, 160)
    treasure_count += 1
    if treasure_count == 45:
        harvest()
```

The logic: re-rolling is cheap and the gold-per-treasure is fixed by maze side length, so
batching ~45 re-rolls before the (tick-costed) `harvest()` call amortizes harvest overhead
across many treasures instead of paying it every single time.

## Wall-follower vs. DFS vs. BFS

### Wall-follower (zero memory) — `treasure_wall_follower.py`

The right-hand-rule classic: try to turn toward your preferred side; if blocked, rotate
until an opening appears; move; repeat. Guaranteed to find the treasure eventually, no
state beyond current heading. `treasure_hunt_worker()` spawns 8 drones with different
starting directions and turn preferences (4 clockwise, 4 counter-clockwise) so they don't
all trace the same wall.

### Iterative DFS with a path stack — `maze_gold_dfs.py`

Tracks an explicit `path_stack` of `(direction_taken, next_direction_to_try)` so it can
**backtrack** instead of re-wandering: `explore_option_iterative()` pushes a new frame each
time it moves into an unvisited branch, and pops + retraces when a branch dead-ends.
Multiple drones run the same maze with **permuted direction orderings**, keyed off
`drone_id % 2 / 3 / 5`, so parallel drones fan out into different branches instead of
converging on the same path:

```python
if drone_id % 2:
    ALL_DIRECTIONS = ALL_DIRECTIONS[::-1]
if drone_id % 3:
    ALL_DIRECTIONS[0], ALL_DIRECTIONS[1] = ALL_DIRECTIONS[1], ALL_DIRECTIONS[0]
```

### Map-first BFS, `measure()`-guided — `maze_gold_16drones_bfs.py`

Explores once to build a full adjacency map of the maze (`get_moves()` records every
open direction from every visited cell), replays that fixed route repeatedly to farm the
*first* 200 treasures cheaply, then switches to `measure()`-guided routing: given the
`(x, y)` of the current treasure, `path_move()` searches the recorded map for a path there
and walks it directly instead of re-exploring. With a 4×4 grid of 8×8 mazes and 16 drones,
this is the strategy behind the `Maze` leaderboard target (9,863,168 gold).

## Scaling: many small mazes beat one big one

Solve time (wall-follower or DFS) grows **super-linearly** with maze side length, while
gold per treasure only grows linearly with it. That tradeoff favors saturating a farm with
many small, fast-clearing mazes over one giant maze: `gold_25drones.py` runs 25 drones on a
5×5 grid of maze plots rather than 1 drone on a 32×32 maze, and
`maze_gold_16drones_bfs.py` tiles 16 separate 8×8 mazes rather than one 32×32 maze.

See also: [Simulation](simulation.md) for rehearsing a maze strategy's re-roll count/gold
rate before running it live, and [Leaderboards](leaderboards.md) for the exact `Maze` /
`Maze_Single` goals.
