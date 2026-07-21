# Getting Started

## What is The Farmer Was Replaced?

You control a **drone** on a grid farm — but not with your hands. You write programs in a
Python-like language, and the drone executes them: move, plant, water, harvest, unlock new
technology, and eventually command dozens of drones at once. Progression is gated by an
in-game research tree paid with the resources you farm.

The genius of the game: **your code is your save file.** Better algorithms literally mean
faster progress, and the late game becomes a pure optimization playground with global
leaderboards.

## The language

It looks like Python and mostly behaves like it, with a few twists:

- No classes of your own; a curated set of built-ins (see the [API Reference](api/reference.md)).
- Every world-affecting call costs **ticks** — e.g. `harvest()` takes time, `quick_print()` is free.
  Execution speed is a resource you unlock and upgrade.
- Each open code window is a file; files can `import` each other once you unlock **Import**.
- `while True:` loops are the norm — farms run forever.

## Your first farm

```python
while True:
    if can_harvest():
        harvest()
    move(North)
```

This alone farms grass forever on column 0 (the world wraps around at the edges — it is a
torus). From there the game escalates: tilling soil, watering, buying unlocks with
`unlock()`, measuring plants with `measure()`, swapping entities with `swap()`, and spawning
extra drones with `spawn_drone()`.

## Where the game keeps your code (Windows)

```text
%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<save-name>\
```

Each in-game window is a `.py` file there, plus `__builtins__.py` (the API stub the game
generates) and `save.json` (progress). This repository mirrors a real end-game save via
[`tools/sync_save.ps1`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/tools/sync_save.ps1).

## Suggested reading order

1. [Crops & Economy](mechanics/crops.md) — what each plant does and yields.
2. [Progression guide](guides/progression.md) — what to unlock, in which order, and why.
3. [Tutorial 01 · Multi-Drone Farming](tutorials/01-multi-drone.md) — the single biggest throughput jump in the game.
