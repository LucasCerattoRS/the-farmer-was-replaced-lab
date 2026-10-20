# 03 · Soil and carrots

## What the game unlocked
`till()` and `plant(Entities.Carrot)`.

## The idea
Carrots only grow on **tilled soil**. You till a tile with `till()`. Planting costs items: **1 Hay
and 1 Wood** per carrot, deducted when `plant` runs.

- 📖 Growth time: between 4.8 and 7.2 seconds.
- ✅ An empty tile is grass; after `till()` it becomes soil.

## The trap: `till()` toggles

```python
till()   # grass -> soil
till()   # soil  -> grass  (undone!)
```

Calling `till()` on a tile that is already soil **turns it back into grass**. Harvesting the carrot
leaves the soil tilled, so the tile does not need `till()` again. The classic mistake is tilling on
every harvest:

```python
# WRONG: on lap 2 the tile is already soil, till undoes it, plant fails
if can_harvest():
    harvest()
    till()
    plant(Entities.Carrot)
```

Symptom: the tile keeps alternating between grass and carrot.

## The fix: two phases

```python
# Phase 1: till and plant, once per tile
for i in range(get_world_size()):
    for j in range(get_world_size()):
        till()
        plant(Entities.Carrot)
        move(North)
    move(East)

# Phase 2: harvest and replant, no till
while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
                plant(Entities.Carrot)
            move(North)
        move(East)
```

!!! warning "Running phase 1 twice breaks it"
    Because `till()` toggles, a second run turns the already tilled tiles back into grass. ✅
    `clear()` removes everything, moves the drone to (0,0) and turns the soil back into grass; use
    it to start over.

## "Why is the harvest uneven?"

You run phase 2 and the drone harvests tile 1, skips tiles 2 and 3, and on the next lap picks up
the ones it missed. It is not a code bug. ✅ Each carrot draws its own time between 4.8 and 7.2 s,
so some are not ready when the drone passes, and it moves on anyway. `move` outside the `if` does
exactly that.

⏳ You can make the drone wait on the tile with `while True` and `break`, trading the mismatch for
idle time. We have not measured which pays more.

## Economy
Wood comes from bush; Hay comes from harvested grass. Carrots spend both. Turning the whole farm
into carrots cuts the production of what they consume, so a **mix** (carrots on the middle tiles
and bush on the corners, or the reverse) keeps Wood coming in. ⏳ Which proportion pays most has
not been measured.

## Exercise
1. Reproduce the mistake (`till()` inside the `if`), watch the tile alternate, then fix it.
2. Build a carrot, bush, carrot column on side 3. Hint: the pattern fits in a single `for i`.
3. Measure: note the Wood before and after 1 minute of phase 2. What was the yield?

Previous: [`for` and the grid](02-for-e-a-grade.md) · Next: [Mixing plants](04-misturando-plantas.md).
