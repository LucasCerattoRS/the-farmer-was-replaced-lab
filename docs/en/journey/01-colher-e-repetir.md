# 01 · Harvest and repeat

## What the game unlocked
`while`, `if`/`else`, `can_harvest()`, `harvest()`, `move()` with `North`/`East`/`South`/`West`,
`plant()` with `Entities.Bush`.

## The idea
Your drone only runs what is in the script, and the script runs once and ends. For the farm to
work by itself, the code goes inside a `while True:`, which repeats forever.

Inside it, the question is always the same: **"is the plant on this tile ready?"**

```python
while True:
    if can_harvest():
        harvest()
        plant(Entities.Bush)
    move(North)
```

Read it as: repeat forever; if the plant is ready, harvest and replant; **then** move, whether
you harvested or not.

## Three facts that matter

- ✅ **An empty tile is grass.** `plant(Entities.Bush)` works on it with no soil preparation.
- ✅ **The border wraps around.** Moving `North` on the last row takes you to the first. On a
  side-3 farm, three steps north bring the drone back to where it started.
- 📖 **An infinite loop is safe.** The game puts a delay between repetitions, so `while True`
  does not freeze anything. You stop it by pressing Execute again.

## The most common mistake: `move` inside the `if`

```python
# WRONG
while True:
    if can_harvest():
        harvest()
        plant(Entities.Bush)
        move(North)      # only moves when it harvested
```

If the tile is not ready, the `if` fails, the drone **does not move** and waits. That may be what
you want on a single tile, but on a path with several tiles it gets stuck on the first slow
plant. `move` goes **outside** the `if`: the drone always moves, harvesting only where it can.

## Exercise
1. Make the drone harvest and replant bush along one column, without stopping.
2. Replace `plant` with nothing (just `harvest`) and watch: the tile turns back into grass by itself.
3. ⏳ Open question: on a side-3 farm, does the bush finish growing between one lap and the next?
   Count how many times `can_harvest()` was false and check for yourself.

!!! warning "Harvesting early destroys"
    ✅ Harvesting a plant that is not ready destroys it. That is why `if can_harvest()` is not decoration.

Next: [`for` and the grid](02-for-e-a-grade.md).
