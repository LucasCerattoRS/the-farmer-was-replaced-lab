# Simulation

`Unlocks.Simulation` — *"Unlocks simulation functions for testing and optimization."*
`simulate()` runs a headless, disposable instance of a file with a chosen starting state,
and hands back only the timing result — the tool for testing a strategy without touching
your live save or spending a real `leaderboard_run()` attempt.

## Signature

```python
def simulate(
    filename: str,
    sim_unlocks: Dict[Unlocks, float] | Iterable[Unlocks] | type[Unlocks],
    sim_items: Dict[Item, float],
    sim_globals: Dict[str, Any],
    seed: float,
    speedup: float,
) -> float
```

Costs 200 ticks to start; returns the elapsed **time it took to run the simulation**
(a `float`, same units as `get_time()`).

## Parameters

| Parameter | Type | Meaning |
|---|---|---|
| `filename` | `str` | The file to run, exactly as `leaderboard_run` takes one. |
| `sim_unlocks` | dict of `Unlocks -> level`, an iterable of `Unlocks`, or the whole `Unlocks` class | The starting unlock state. A dict lets you set specific levels (e.g. `{Unlocks.Speed: 3}`); an iterable/plain class grants unlocks at their base level. |
| `sim_items` | `Dict[Item, float]` | Starting inventory — maps each item to a starting quantity. |
| `sim_globals` | `Dict[str, Any]` | Starting values for global variables in `filename`'s scope — lets you inject state the script expects without editing the file itself. |
| `seed` | number | The random seed. **Must be a positive integer.** Controls every `random()` call inside the simulation, making pumpkin fusion outcomes, cactus growth timing, sunflower petal rolls, etc. reproducible run to run. |
| `speedup` | number | Starting execution speedup, same scale as `set_execution_speed`. |

## Example call

Straight from the API stub:

```python
filename = "f1"
sim_unlocks = Unlocks
sim_items = {Items.Carrot: 10000, Items.Hay: 50}
sim_globals = {"a": 13}
seed = 0
speedup = 64
run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
```

## Use cases

- **Strategy A/B testing.** Run the same target script twice with two different
  `sim_globals` (e.g. different column widths for a drone deployment, or different water
  thresholds) and compare the returned times directly — no need to reset a real farm
  between attempts.
- **Seed hunting.** Because `seed` is a required, explicit parameter, you can iterate over
  candidate seeds and keep the ones that produce favorable random outcomes early
  (a lucky pumpkin fusion streak, an early 15-petal sunflower per
  [Crops & Economy](crops.md#sunflowers-power-petals)) before committing to that seed on a
  real run.
- **Leaderboard rehearsal.** Since `simulate()` shares its `filename`/state-injection shape
  with `leaderboard_run()`, it's the natural way to rehearse a leaderboard script — feed it
  the same starting unlocks/items a real attempt would have, and read back the timing
  before spending a live run. See [Leaderboards](leaderboards.md#how-leaderboard_run-works).

## Limits

- `seed` must be a positive integer — there's no "unseeded" mode; every simulation is
  reproducible by construction.
- The simulation is bounded to whatever `filename` actually does — it's not a generic
  what-if sandbox, it *executes* the target script under the given starting conditions and
  reports only the elapsed time, not a trace of intermediate state. If you need
  intermediate visibility, instrument the target script itself (e.g. via `sim_globals` or
  `quick_print`) rather than relying on `simulate()`'s return value alone.
- Requires `Unlocks.Simulation`, gating this tool to a late-game stage — see the
  [Progression guide](../guides/progression.md).

See also: [Leaderboards](leaderboards.md) and
[Leaderboard Strategies](../guides/leaderboard-strategies.md) for concrete scripts worth
rehearsing with `simulate()` before a real attempt.
