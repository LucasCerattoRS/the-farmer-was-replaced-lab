# Unspecified behaviours

**Generated from `tfwrlang/errors.py` — do not edit by hand.** Run
`python interpreter/gen_unspecified.py` to regenerate.

Each entry below is a point where the official TFWR sources define no outcome. The reference
model refuses to guess there: it raises `Unspecified` (or records the choice it was forced to
make) instead of quietly inheriting CPython's answer. That makes every hole loud.

**Each of these is a [Track 2](../ROADMAP.md#track-2--empirical-research-measure-the-game)
experiment waiting to be run.** Measuring one turns a refusal into a documented number and
removes it from this list.

| # | Topic | What the sources leave open |
|---|---|---|
| 1 | `boolean-short-circuit` | Whether `and`/`or` skip evaluating their second operand. operators.md does not state that short-circuit evaluation happens. The model evaluates left-to-right and skips the second operand, but records the choice here because it is observable when the skipped side has side effects. |
| 2 | `call-stack-limit` | The maximum recursion depth. language-quirks.md says the call stack is finite, but the actual limit is unmeasured (a Track 2 item). The model makes it a parameter and never invents a number. |
| 3 | `default-arg-eval-time` | When a default-argument expression is evaluated (at `def` time or at call time). The docs call `def` an assignment but never pin this down. The model evaluates defaults at call time and records the choice. |
| 4 | `drone-scheduling` | How multiple drones are interleaved. Inter-drone ordering is the least documented part of the game. The model refuses `spawn_drone`/`wait_for` rather than invent a scheduler. |
| 5 | `grow-time` | How long each entity takes to grow. crops.md asserts approximate seconds (~0.5s / ~4s / ~7s ...) that were never measured. The world model refuses to advance growth unless a grow-time model is injected. |
| 6 | `harvest-yield` | How many items a harvest credits. crops.md documents the item *type* per crop (Grass -> Hay, Bush/Tree -> Wood, ...) and the formulas for the two that scale (cactus size^2, pumpkin size^3), but the flat base quantity for the others is never stated. The world model refuses to credit an invented amount and requires a yield model to be injected. |
| 7 | `module-by-window-name` | `import` resolves a module by the game window's name, not a file path. There is no file-system model for that here, so `import` is refused rather than faked. |
| 8 | `pumpkin-death-rate` | The probability a pumpkin dies while growing. crops.md says 'about 1 in 5', unmeasured. The world model requires the rate to be injected. |
| 9 | `sunflower-petals` | The distribution of sunflower petal counts. Assumed 1-15, uniform, unverified. The world model requires the distribution to be injected. |
| 10 | `truthiness` | Truthiness of non-boolean values. operators.md only defines booleans in conditions and explicitly does not promise what a non-boolean means in `if`/`while`/`and`/`or`/`not`. The model refuses non-booleans in boolean context instead of borrowing Python's rules. |
