# Cactus Sorting

Cacti are the game's clearest "algorithms matter" moment: the same field of grown cacti
pays out orders of magnitude more if you sort it first.

## The chain-harvest rule

A cactus has a size `0`–`9`, readable with `measure()` (or `measure(direction)` for a
neighbor). Harvesting a single, unsorted cactus pays `size²`. But if the field —
or a region of it — is sorted so that **every neighbor to the North and East is ≥ its own
size, and every neighbor to the South/West is ≤**, harvesting *any one* cactus in that
sorted block **chain-harvests the entire block** in one action. A fully sorted 32×32 field
pays out as if all 1024 cacti were harvested individually, in the time of one `harvest()`
call.

The primitive that makes sorting possible is `swap(direction)`: it exchanges the entity
under the drone with the neighbor in `direction`, and works even if one side is empty
(`None`). Combined with `measure()`, a cactus field becomes an in-place sortable array on a
2-D grid.

## Three algorithms (all in this repo)

### 1. Insertion sort per line — `cactus_insertion_sort.py`

Sweep each row and column, and whenever the tile behind is bigger than the current one,
`swap()` backward until it's in place — classic insertion sort, applied once per row and
then once per column:

```python
def insertion_sort_row_step():
    while get_pos_x() > 0:
        if measure() < measure(West):
            swap(West)
            move(West)
        else:
            break
```

Simple, and cheap on a **nearly-sorted** field (few swaps needed per pass) — but each row
spawns a fresh drone per pass (`plant_and_sort_all_rows`), then a second batch per column,
so the coordination overhead is real.

### 2. Cocktail / shaker sort — `cactus_shaker_sort.py`

Bubbles in both directions per pass, with a `last_swap` bound that **shrinks the walked
range** on every pass — once a suffix/prefix stops producing swaps, it's excluded from the
next pass:

```python
while x_curr < right:
    if measure() < measure(East):
        swap(East)
        loc_last_swap = x_curr
    move(East)
    x_curr += 1
right = loc_last_swap   # next pass won't walk past here
```

This is the algorithm behind the leaderboard run in
[`farms/leaderboards/cactus_cocktail_sort.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/cactus_cocktail_sort.py)
(`Cactus` board goal: 33,554,432 cacti). Its `pro_swap()` also refuses to swap unless one
side is genuinely out of order *and* the drone isn't at a field edge, avoiding wasted
`swap()` calls at the boundary.

### 3. "Vacuum theory" — `cactus_vacuum_sort.py`

Treats empty tiles as size **−1** instead of skipping them, so every comparison pushes
holes toward one corner just like a normal cactus would be pushed:

```python
def medir_com_vazio(direcao):
    val = measure(direcao) if direcao != None else measure()
    return -1 if val == None else val
```

This means newly-planted (size-0) cacti and empty holes both drift the same direction as
regular sorting proceeds — ideal for **continuous farming**, where the field is replanted
and sorted at the same time rather than sorted once and harvested.

## Complexity comparison

| Algorithm | Best case | Worst case | Best suited for |
|---|---|---|---|
| Insertion sort (per line) | Near-linear on nearly-sorted rows | Quadratic on reverse-sorted rows | Fields that stay mostly sorted between harvests |
| Cocktail / shaker sort | Shrinking-bound passes cut wasted comparisons | Quadratic worst case, same as bubble sort | Leaderboard runs — deterministic, no extra bookkeeping |
| Vacuum ("−1 hole") sort | Same asymptotics as insertion/shaker | Same | Fields that replant continuously instead of batch-refilling |

None of the three scripts publish a formal complexity claim — this table reflects the
walking pattern each one implements (comparison-and-swap on adjacent tiles), which is
fundamentally insertion/bubble-family regardless of variant; the difference is in how much
*wasted* walking each variant avoids.

## Multi-drone sorting with barriers

Rows can be sorted in parallel (one drone per row), but the subsequent column pass touches
tiles every row-drone just wrote to — sort all rows, **synchronize**, then sort all
columns:

```python
drones = []
for _ in range(world_size - 1):
    drones.append(spawn_drone(shake_row))
    move(North)
shake_row()          # this drone sorts the last row itself
wait_for_drones(drones)   # barrier: every row must finish first
```

`sort_all_columns()` in `cactus_cocktail_sort.py`/`cactus_insertion_sort.py` repeats the
same spawn-then-`wait_for` barrier for columns. Skipping the barrier — starting column
sorts before every row is done — reintroduces disorder mid-sort, since a column swap can
undo a row that hasn't been visited yet this pass.

## Harvest rule of thumb

Don't harvest at every opportunity. Let the field fill and sort completely, then harvest
once — yield scales with `size²` and chain length, so patience compounds. See
[Crops & Economy](crops.md#cactus-yield-chain-rule) for the yield formula and
[Drones](drones.md) for the barrier/synchronization primitives used above.
