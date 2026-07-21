# Tutorial 04 · The Dinosaur Apple Solver

**Goal:** survive as long as possible in the dinosaur minigame, collecting every apple you can.
**Requires:** Dinosaurs unlock, Senses (`measure`), Hats, Dictionaries.

Full mechanics on [Dinosaurs](../mechanics/dinosaurs.md); this page is how
`farms/dinosaur/apple_solver.py` actually plays the game.

## Collecting is implicit

There is no `collect()`. You **walk onto the apple** and it is yours — the only thing you
have to do is ask where the next one is:

```python
def move_and_check_apple(direction):
    if not move(direction):
        return False
    if (get_pos_x(), get_pos_y()) == apple_pos:
        measure_apple()
    return True
```

Two jobs in one primitive, and both matter:

- It re-measures **only when you land on the apple**, so `apple_pos` is always the *current*
  target.
- It returns `False` when `move()` fails — which in this minigame means **you hit your own
  tail**. Every caller propagates that `False` upward instead of continuing blindly.

`measure_apple()` also bumps `squares_occupied`, which is the script's estimate of how much
of the board its tail now fills. That counter is what eventually ends the chase.

## Chasing: one walker, two modes

Movement to a coordinate is a single pair of functions, and they take a flag that swaps the
step function itself:

```python
def move_to_col(target_x_pos, do_measure=True):
    curr_x = get_pos_x()
    direction = West
    if curr_x < target_x_pos:
        direction = East

    for x in range(abs(target_x_pos - curr_x)):
        this_check = move
        if do_measure:
            this_check = move_and_check_apple
        if not this_check(direction):
            return False
    return True
```

`this_check = move` versus `this_check = move_and_check_apple` — functions are values, so
"walk while watching for the apple" and "just walk" are the same code path. The late-game
coverage route passes `do_measure=False` because by then it is not chasing anything, and
skipping the position comparison on every step is free speed.

## Two stages that stay out of each other's way

The board is swept by two alternating stages: **stage 1** works upward along the bottom half,
**stage 2** mirrors it downward from the top. The danger is obvious — the tail one stage
leaves behind is a wall for the other.

The fix is two dictionaries, `offlimit_columns_stage1` and `offlimit_columns_stage2`, that
record *how far up/down a column has already been claimed*. Stage 1 bails out immediately if
the apple sits somewhere it must not go:

```python
apple_pos_x, apple_pos_y = apple_pos
if apple_pos_y == 0 or apple_pos_x in edge_positions or (
    apple_pos_x in offlimit_columns_stage1
    and apple_pos_y <= offlimit_columns_stage1[apple_pos_x]
):
    return transition_to_stage_2()
```

Three bail conditions: the apple is on the boundary row, on an edge column, or inside
territory the *other* stage already claimed.

And when a stage does take an apple, it claims a **pair** of columns for itself:

```python
offlimit_columns_stage2[target_x_pos] = apple_pos_y
offlimit_columns_stage2[target_x_pos + 1] = apple_pos_y
```

That pairing is why the target column is snapped to an odd/even boundary first
(`target_x_pos = apple_pos_x - 1` when the apple's column is even). The board is consumed two
columns at a time, so the two stages interleave cleanly instead of fragmenting it.

## Knowing when to stop chasing

This is the single most important decision in the script:

```python
if squares_occupied > (world_size_minus_one) * 4 - 4:
    break
```

Past that density, chasing an individual apple is how you trap yourself — the tail is long
enough that a detour can seal you into a pocket with no exit. So the script stops optimizing
for apples and starts optimizing for **survival**.

!!! tip "The general lesson"
    A greedy strategy that is correct early is often fatal late. Write the switch-over
    condition *before* you tune the greedy part — it is the thing that decides whether your
    run ends at 60% board coverage or 100%.

## The wavy coverage route

After the switch, the drone walks a fixed serpentine that is aware of what the chase already
consumed:

```python
def move_to_right_col_wavy():
    for x in range(world_size):
        if x % 2:
            target_y = 1
            if x in offlimit_columns_stage1:
                target_y = offlimit_columns_stage1[x] + 1
            while get_pos_y() != target_y:
                move(South)
            move(East)
        else:
            while get_pos_y() != world_size_minus_one:
                move(North)
            move(East)
```

Odd columns descend, even columns climb — but an odd column stops at
`offlimit_columns_stage1[x] + 1` instead of at row 1, because everything below that is
already tail. The dictionaries built during the chase are *reused* as a map of the board.

From there the script runs a plain boustrophedon until a `move()` finally fails, latching the
result so a single failure ends the whole run cleanly:

```python
game_complete = not move_to_row(world_size_minus_one, False)
game_complete = game_complete or not move(East)
game_complete = game_complete or not move_to_row(1, False)
```

`change_hat(Hats.Straw_Hat)` at the very end takes the hat off and returns the drone to
normal farming.

## Want something simpler first?

`farms/dinosaur/bone_snake_solo.py` is the opposite philosophy: instead of routing around its
tail, it treats a blocked move as "harvest this tile and retry". Far less code, far less
throughput — a good warm-up before this one. See
[Dinosaurs](../mechanics/dinosaurs.md#snaketail-behavior-in-a-simpler-farm).

For the competition version of bone farming, see
[Leaderboard Strategies](../guides/leaderboard-strategies.md#dinosaur-33488928-bones).
