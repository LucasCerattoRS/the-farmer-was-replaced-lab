# Tutorial 03 · Maze Gold Farming

**Goal:** industrial-scale gold. **Requires:** Mazes unlock, Weird Substance, ideally Megafarm.

## How mazes work

1. Plant a **bush** and use `Items.Weird_Substance` on it → the bush becomes a maze of
   hedges with a **treasure** inside. The treasure pays `gold = maze side length`.
2. Inside a maze, `can_move(dir)` tells you whether a hedge blocks you — that's your wall sensor.
3. `measure()` on the treasure tile region returns the treasure's `(x, y)` — you know
   *where* to go, just not *how*.
4. Re-applying Weird Substance to a solved treasure **re-rolls it into a new maze**, so one
   plot can be farmed repeatedly before cashing out.

## Level 1: wall-follower (zero memory)

The classic right-hand rule — always try to turn clockwise from your last heading:

```python
def solve():
    d = East
    while get_entity_type() != Entities.Treasure:
        d = next_ccw(d)          # start by trying to turn one way
        while not can_move(d):
            d = next_cw(d)       # rotate until an opening appears
        move(d)
```

Guaranteed to find the treasure. Slow, but perfect as a first solver.
Repo: `farms/mazes/treasure_wall_follower.py` (8 drones, one maze each).

## Level 2: iterative DFS with a path stack

Remember where you came from; only explore unvisited branches; backtrack by popping the
stack. Several drones can run the same maze with **different direction orderings** (keyed
on `drone_id % 2/3/5`) so they fan out instead of following each other.
Repo: `farms/mazes/maze_gold_dfs.py`.

## Level 3: map-first BFS (`measure()`-guided)

Map every cell's openings once, then compute the shortest path to the measured treasure
position and walk it directly. With a 4×4 grid of 8×8 mazes and 16 drones this is the
`farms/mazes/maze_gold_16drones_bfs.py` strategy — and the backbone of the
`Maze` leaderboard (9,863,168 gold).

## Scaling economics

- Maze cost scales with the Weird Substance dose; re-rolling a solved maze ~45 times
  before harvesting (see `farms/mazes/gold_25drones.py`) multiplies gold per plot.
- 25 drones on a 5×5 grid of mazes beats 1 drone on a giant maze: solve time grows
  super-linearly with maze size, so **many small mazes win**.
