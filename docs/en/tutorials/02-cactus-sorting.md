# Tutorial 02 · Cactus Sorting (chain harvest = size²)

**Goal:** harvest an entire cactus field in one click's worth of time.
**Requires:** Cactus unlock, Senses (`measure`), swap.

## Why sort at all?

A cactus harvested alone gives `size²` cacti — but if **every neighbor to the North and
East is ≥ its size and every neighbor South/West is ≤** (i.e. the whole field is sorted
both ways), harvesting *one* cactus chain-harvests **all of them**. A sorted 32×32 field
pays out hundreds of thousands per harvest.

## The primitive: `swap(direction)`

`measure()` returns the cactus size under the drone; `measure(North)` measures the
neighbor. `swap(North)` exchanges them. That's all you need — the rest is a sorting
algorithm on a 2-D grid.

## Three algorithms, three trade-offs (all in this repo)

### 1. Insertion sort per line — `farms/crops/cactus_insertion_sort.py`
March East; while the cactus behind you is bigger, swap backwards. Simple, few wasted
moves on nearly-sorted fields.

### 2. Cocktail / shaker sort — `farms/crops/cactus_shaker_sort.py`
Bubble in both directions with a `last_swap` bound that shrinks the walked range every
pass. This is the algorithm behind the leaderboard run in
`farms/leaderboards/cactus_cocktail_sort.py` (goal: 33,554,432 cacti).

```python
def shake_row(y):
    last = get_world_size() - 1
    while last > 0:
        new_last = 0
        for x in range(last):
            if measure() > measure(East):
                swap(East)
                new_last = x
            move(East)
        last = new_last
        # walk back West doing the same with the '<' comparison
```

### 3. "Vacuum theory" — `farms/crops/cactus_vacuum_sort.py`
Empty tiles are treated as size **−1**, so holes get pushed to one corner and freshly
planted cacti always enter from the sorted side. Best for continuous farming where you
replant while sorting.

## Multi-drone sorting

Rows can be sorted in parallel (one drone per row band), but column passes touch shared
tiles — synchronize with `wait_for()` between phases:
sort all rows → barrier → sort all columns → repeat until no swaps anywhere.

## Harvest rule of thumb

Don't harvest at every opportunity. Let the field fill and sort completely, then harvest
once — yield scales with size², so patience literally compounds.
