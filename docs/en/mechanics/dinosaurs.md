# Dinosaurs

Equipping `Hats.Dinosaur_Hat` — *"Equip it to start the dinosaur game"* — turns the drone
into the head of a snake-like creature: as it moves, it drags a tail of `Entities.Dinosaur`
segments behind it, filling every tile it has already passed over.

## The minigame

- `change_hat(Hats.Dinosaur_Hat)` starts the run.
- `Entities.Dinosaur` — *"A piece of the tail of the dinosaur hat. When wearing the
  dinosaur hat, the tail is dragged behind the drone filling previously moved tiles."*
  Average grow time ~0.2s, grows on Grassland or Soil.
- The tail occupies tiles behind the drone, so a `move()` that would step onto your own
  tail **fails** — that failure is how every script in this repo detects "the run ended" or
  "I need to clear a tile."
- `change_hat(Hats.Straw_Hat)` (or any other hat) ends the minigame and reverts the drone
  to normal farming.

## Apple mechanics and `measure()`

`Entities.Apple` — *"Dinosaurs love them apparently."* An apple spawns somewhere on the
board; reaching its tile and collecting it is the objective loop of the minigame (longer
tail = more squares "occupied" = more value from the run).

The general `measure()` docstring lists Sunflower (petals), Maze (treasure position),
Cactus (size) and Dinosaur ("the number corresponding to the type") as the entities it has
special behavior for. In practice, `farms/dinosaur/apple_solver.py` calls bare `measure()`
while the minigame is running and treats the result as the **current apple's `(x, y)`
position**:

```python
apple_pos = measure()
...
def measure_apple():
    global apple_pos, squares_occupied
    apple_pos = measure()
    squares_occupied += 1
```

This is confirmed by the script's behavior rather than the general docstring — if you're
writing your own solver, verify with a `print(measure())` at game start rather than
assuming the position tuple format is documented elsewhere.

## `apple_solver.py`'s two-stage "wavy" route

The solver runs in two alternating stages that sweep the board from opposite corners:

- **Stage 1** sweeps from the bottom (`apple_pos_y == 0` is a boundary condition) upward,
  chasing the apple's column while marking `offlimit_columns_stage2` so the *other* stage
  won't re-cross tiles this stage has already claimed with the tail.
- **Stage 2** mirrors it from the top down, marking `offlimit_columns_stage1`.
- Both stages hand off to each other (`transition_to_stage_1/2`) whenever the apple moves
  out of the current stage's reachable region, or the tail is about to trap the drone.

Once the board is dense enough that continuing to chase individual apples risks a dead end
(`squares_occupied > (world_size_minus_one) * 4 - 4` in the script), it abandons apple
chasing entirely and switches to a **fixed "wavy" coverage route**
(`move_to_right_col_wavy`) that guarantees covering the remaining board without
self-trapping, tracking `game_complete` (a failed `move()`) as the natural end condition.

## Snake/tail behavior in a simpler farm

`farms/dinosaur/bone_snake_solo.py` takes the opposite approach: instead of routing around
its own tail, it treats a blocked `move()` as "clear this tile and retry":

```python
def limpar_e_mover(direcao):
    if not move(direcao):
        if can_harvest():
            harvest()
        move(direcao)
```

A single drone zig-zags a 32×32 field (serpentine: up on even columns, down on odd),
harvesting tail segments (bones) as it goes and clearing any tile that blocks it before
retrying the move. Far simpler than the two-stage apple solver, and single-drone — the
tradeoff is throughput: it's a "solo, reliable" bone farm rather than a maximized one.

## Bone yields

`Items.Bone` — *"The bones of an ancient creature."* The `Dinosaur` leaderboard's goal is
**33,488,928 bones** (multi-drone) — see [Leaderboards](leaderboards.md). The exact payout
formula isn't published in the API stub; `farms/leaderboards/fastest_reset.py` estimates
the apple cost needed to reach a bone target using a world-size- and
`Unlocks.Dinosaurs`-level-dependent formula internally (`farm_bones`), which is a
script-side approximation for automation purposes, not a documented game constant — treat
it as "yield scales with world size and the `Dinosaurs` unlock level," not as an exact
number to rely on.

See also: [Leaderboards](leaderboards.md) for the `Dinosaur` board goal, and
[Leaderboard Strategies](../guides/leaderboard-strategies.md) for how `bone_collector.py`
adapts the snake pattern for a competition run.
