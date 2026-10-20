# 04 · Mixing plants

## What the game unlocked
Nothing new. Here you combine `for`, `till`, `plant` and `can_harvest` to grow **two plants in the
same column**: carrots on the ends and bush in the middle, or the reverse.

## The idea
Carrots spend Hay and Wood; bush yields Wood. Mixing keeps Wood coming while you plant carrots.
The pattern is a **3-tile column**: A, B and C.

The point that confuses people: the 3-tile pattern **is** the whole column. So `for i` (one lap per
column) is enough, and each tile gets its own block of code.

## Phase 1: prepare and plant (carrot, bush, carrot)

```python
for i in range(get_world_size()):
    till()                      # tile A: till
    plant(Entities.Carrot)
    move(North)

    plant(Entities.Bush)        # tile B: bush grows on grass, no till
    move(North)

    till()                      # tile C: till
    plant(Entities.Carrot)
    move(North)                 # 3 steps: the map wraps, back to A

    move(East)                  # column done
```

Tracing one column (side 3, the border wraps):

| Step | Tile | Does |
|---|---|---|
| 1 | A | `till`, carrot, move |
| 2 | B | bush, move |
| 3 | C | `till`, carrot, move and wrap back to A |
| 4 | A | `move(East)` goes to the next column |

## Phase 2: harvest and replant the same thing

```python
while True:
    for i in range(get_world_size()):
        if can_harvest():       # tile A
            harvest()
            plant(Entities.Carrot)
        move(North)

        if can_harvest():       # tile B
            harvest()
            plant(Entities.Bush)
        move(North)

        if can_harvest():       # tile C
            harvest()
            plant(Entities.Carrot)
        move(North)

        move(East)
```

Three rules hold this up:

1. **Each tile is handled once per lap.**
2. **`move` stays outside the `if`**, as in milestone 01.
3. **Each block replants what the tile had.** The code does not "discover" the pattern: it repeats
   it by position, which is why the pattern holds.

For the reverse (bush on the ends, carrot in the middle), swap the three blocks: bush on A and C,
`till` and carrot on B.

## Common mistakes

- **Repeating the pattern in a `for j`.** That gives 9 tiles per column and shifts everything (see milestone 02).
- **`till()` on a tile that is already soil.** It undoes the soil (see milestone 03).
- **Running phase 1 on an already tilled farm.** Same problem. Run `clear()` first: ✅ it removes
  everything, moves the drone to (0,0) and turns the soil back into grass.
- **Harvesting without testing.** Each tile needs its own `if can_harvest()`.

## Limit: only works on side 3
The 3-tile pattern is written by hand. On a bigger side it drifts. For any size, the code has to
know which tile of the column it is on, which requires comparing numbers. ⏳ Once the game unlocks
operators, the idea is `if j == 0: … elif j == 1: … else: …`, or `j % 3`.

## Exercise
1. Build the version with bush on the ends and carrots in the middle.
2. Run phase 2 for 1 minute and note the Wood before and after. ⏳ The yield of the mix against
   pure bush **has not been measured yet**.
3. Explain, without running, what happens if phase 1 uses `till()` on all three tiles.

Previous: [Soil and carrots](03-solo-e-cenoura.md).
