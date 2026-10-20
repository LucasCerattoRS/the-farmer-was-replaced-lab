# 02 · `for` and the grid

## What the game unlocked
`for`, `range()`, `get_world_size()`. The farm stopped being a row and became a square, so
`move(North)` alone no longer reaches every tile.

## The idea: one `for` inside another

`for` runs its body **once per element**. It does not test a condition the way `while` does.
`for i in range(3)` runs 3 times, with `i` equal to 0, 1 and 2.

To walk the square, think of a building. The outer `for` (`i`) is the **floor**; the inner one
(`j`) is the **doors** on that floor:

```python
for i in range(get_world_size()):        # one lap per column
    for j in range(get_world_size()):    # one lap per tile in the column
        harvest()
        move(North)
    move(East)                           # column done: go to the next one
```

The rule that clears up the confusion: **the inner `for` runs completely on every lap of the outer
one, and starts again from zero.** For side 3, the inner body runs 3 × 3 = 9 times.

**Indentation** says when each line runs:

- inside `j`: once per tile;
- outside `j` but inside `i`: once per column (here, `move(East)`).

If `move(East)` sat inside `j`, the drone would step sideways on every tile and never build a column.

## To repeat forever: `while` on the outside

```python
while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
            move(North)
        move(East)
```

The `for` walks the farm **once**; `while True` repeats that. The other way round, a `while`
inside the `for` would trap the drone on the first tile. And since `get_world_size()` is read on
every lap, the code stays correct when the farm grows.

## The most common mistake: repeating the pattern twice

You want the carrot, bush, carrot pattern on a 3-tile column. The temptation:

```python
# WRONG
for i in range(get_world_size()):
    for j in range(get_world_size()):
        # ...handling of the 3 tiles A, B and C in here...
    move(East)
```

The body already handles **3 tiles**, and `for j` repeats it 3 times: 9 tiles per column. Worse,
if the body ends without moving, the next lap starts on the tile where the previous one stopped,
and the result comes out shifted.

When the pattern already covers the whole column, **`for i` alone is enough**: one block per tile
and a `move(North)` after each.

!!! info "Current limit"
    This hand-written pattern only works on a **side-3** farm. For any side length the code has
    to know "which tile of the column is this", meaning it has to compare `j` with a number.
    That needs operators (`==`, `%`), which the game has not unlocked at this stage.

## Exercise
1. Make the drone harvest the whole farm and end on the starting tile.
2. Without running it: with side 4, how many times does the `j` body run? And `move(East)`?
3. Run the version with `move(East)` inside `j` and describe the drone's path.

Previous: [Harvest and repeat](01-colher-e-repetir.md) · Next: [Soil and carrots](03-solo-e-cenoura.md).
