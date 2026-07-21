# Polyculture

Companion planting: certain plants yield more (or need less upkeep) when a specific
*other* plant grows next to them. `Unlocks.Polyculture` turns this from a curiosity into a
farming strategy.

## The `get_companion()` mechanic

```python
def get_companion() -> Tuple[Entity, Tuple[int, int]] | None
```

Call `get_companion()` on the plant under the drone. It returns `None` if that plant has
no companion preference right now, or a tuple `(companion_type, (x, y))` — the entity type
it wants, and the exact tile to plant it on. The wanted tile is typically adjacent to the
plant that made the request, but the API only guarantees a `(x, y)` pair, not a fixed
offset — always read the position back rather than assuming a direction.

```python
companion = get_companion()
if companion != None:
    plant_type, (x, y) = companion
    print("Companion:", plant_type, "at", x, ",", y)
```

## The companion mapping pattern

Because the request names a tile that isn't the one you're standing on, a single drone
sweeping a field can't act on a companion request immediately — it has to **remember** it
until the sweep reaches that tile. `farms/crops/carrot_polyculture.py` solves this with two
dictionaries shared across drones:

```python
companion_mapping = {}   # target tile -> entity type it should become
carrot_mapping = {}      # origin tile -> its companion's target tile (for cleanup)

def track_companion(curr_x, curr_y):
    result = get_companion()
    if result == None:
        return False
    target_entity, (target_x, target_y) = result
    if (target_x, target_y) not in companion_mapping:
        companion_mapping[(target_x, target_y)] = target_entity
        carrot_mapping[(curr_x, curr_y)] = (target_x, target_y)
        return True
    return False
```

Every tile the drone visits is checked against `companion_mapping` first (plant what was
requested), then `carrot_mapping` (this tile's own companion needs re-linking after
harvest), and only falls back to planting a fresh `Carrot` if neither applies. Because
`companion_mapping`/`carrot_mapping` are plain globals, **every drone in the fleet reads and
writes the same map** — a companion request logged by drone 3 gets fulfilled whichever
drone's sweep reaches that tile next.

`farms/crops/carrot_polyculture_32x32.py` runs the same idea at 32×32/8-drone scale with a
`pedidos` (requests) list instead of two dicts, plus a dedicated sunflower strip on the
last two columns for Power income alongside the carrot polyculture.

`farms/crops/hay_polyculture.py` and `weird_substance_polyculture.py` apply the identical
mapping pattern to grass and a checkerboard of trees respectively — trees specifically
benefit from *not* being adjacent to each other (see [Crops & Economy](crops.md)), so
their companion tiles double as spacers.

## Yields

The API stub doesn't publish an exact multiplier for the companion bonus — treat it
qualitatively: a companion-satisfied plant yields **more than the same plant grown alone**,
which is why end-game carrot/hay/tree farms bother with the bookkeeping above instead of
running a flat monoculture sweep.

## When polyculture beats monoculture

- **Worth it** once `Polyculture` is unlocked and the field is large enough that the
  per-tile bookkeeping overhead (checking two dictionaries every tile) is cheap relative
  to the throughput of a multi-drone column-split sweep — see [Drones](drones.md).
- **Not worth it** on crops whose yield already scales super-linearly with count, like
  fused pumpkins (n³) or sorted cactus (n² with chain harvest) — the fusion/chain bonus
  dwarfs whatever the companion bonus would add, and the extra bookkeeping only competes
  for drone attention against the pattern that actually drives those yields.
- Companion tracking is inherently **stateful across the whole field**, so it composes
  best with the column-split multi-drone pattern where all workers share one global
  request map, rather than with algorithms (like cactus sorting) that need strict
  per-region isolation between drones.

See also: [Crops & Economy](crops.md) for what each companion-eligible plant does on its
own, and [Drones](drones.md) for the column-split deployment these scripts build on.
