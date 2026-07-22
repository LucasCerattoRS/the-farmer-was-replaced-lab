# Reference Interpreter

!!! warning "This is **not** a reimplementation of the game's interpreter"
    The game's own interpreter is closed — there is no published devlog, postmortem or source for
    it (see [About the Game](../about/the-game.md)). This is a **model of the documented
    behaviour**: the same claims the pages in this *Language* section make in prose, in a form
    that can be *executed and tested*. It is deliberately small, and it must never be described as
    "how the game works internally" — only as "how the documented language behaves."

Every other page here writes down what the language does. This one makes that writing
**runnable**. A small tree-walking interpreter for the documented TFWR subset lives in
[`interpreter/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/interpreter)
— a lexer, a parser, a pure evaluator, and a world model — so the prose has a second life as code
that either agrees with the docs or fails a test.

## Why bother, when the docs already exist

Because prose can hide a guess and code cannot. The design turns that into a mechanical rule:

> **Where the official sources are silent, the model raises `Unspecified` instead of quietly
> inheriting Python's answer.**

That inverts the usual risk. In an ordinary Python port, every undocumented corner would silently
do *whatever CPython does* — and you'd never notice the model had invented an answer. Here each
such corner is **loud**: it stops and names itself. Every `Unspecified` the model can raise is
catalogued in
[`interpreter/UNSPECIFIED.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/interpreter/UNSPECIFIED.md),
and each entry is a [Measured Numbers](../mechanics/measured-numbers.md) experiment waiting to be
run. Measuring one turns a refusal into a documented number.

## What it covers

| Layer | File | What it models |
|---|---|---|
| **Front end** | `lexer.py`, `parser.py`, `nodes.py` | Indentation blocks, the full expression grammar, precedence from [Operators](operators.md) |
| **Evaluator** | `interp.py` | Values, operators, `if`/`while`/`for`, `def`/call/`return`, scope + `global` + closures, collections |
| **World** | `world.py`, `builtins.py` | An N×N **torus** grid, ground/entity/water, inventory, the tick counter, and the documented verbs |

The front end is checked against the whole curated corpus: `parse_corpus.py` parses **45 of 46**
scripts in [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms)
cleanly. The one holdout — `maze_gold_dfs.py` — reverses a list with `ALL_DIRECTIONS[::-1]`, and
slicing appears **nowhere** in the official sources (checked: `lists.md` and the canonical
`builtins.py` list class document indexing and the four mutation methods, never `[start:stop:step]`).
That triaged cleanly into a **documentation gap**: the game supports slicing — the corpus is the
evidence — but the official docs omit it, now written up on
[Collections](collections.md). The model keeps refusing slicing (`NotSupported`) because it tracks
the *officially documented* subset, and that refusal is exactly what surfaced the gap.

## What it refuses, and why

The refusals are the point, not a gap. Each one cites the page that declines to define the
behaviour:

- **Non-boolean truthiness.** [Operators](operators.md) defines booleans in a condition and never
  says what a non-boolean means, so `if 5:` raises `Unspecified('truthiness')` rather than
  guessing that `5` is true.
- **Ordering non-numbers.** `< <= > >=` on non-numbers is a runtime error — operators.md defines
  ordering on numbers only.
- **The four unmeasured game numbers** — grow time, pumpkin death rate, sunflower petal
  distribution, and harvest yield quantity — are *injected* into the world. Their defaults raise
  `Unspecified` the instant they're consulted, so a script cannot silently run on a guessed
  number. Inject a concrete model and the same script runs end to end.
- **Drones.** `spawn_drone` / `wait_for` / `has_finished` raise `Unspecified('drone-scheduling')`.
  Inter-drone ordering is the least documented part of the game ([Drones](../mechanics/drones.md)),
  and it cannot be sourced — so a documented refusal *is* the deliverable, not an invented
  scheduler.

## Running it

Everything runs from the repo root. There is no game required — this is pure Python.

```bash
# 1. Parse the whole curated corpus (front end)
python interpreter/parse_corpus.py

# 2. Run the behaviour tests — one per claim the Language pages assert
pip install pytest
python -m pytest interpreter/tests/

# 3. Regenerate the catalogue of unspecified behaviours from the code
python interpreter/gen_unspecified.py          # writes interpreter/UNSPECIFIED.md
python interpreter/gen_unspecified.py --check   # CI mode: fails if it drifted
```

The test suite is the specification made executable: every test names the page whose claim it
pins down — that loops and branches open no scope, that closures capture, that the two-price tick
rule holds, and that each unmeasured number refuses loudly.

Using the world model directly, with concrete numbers injected so a script can run:

```python
import sys; sys.path.insert(0, "interpreter")
from tfwrlang import world as W
from tfwrlang.builtins import make_world_interpreter

models = W.ModelSet(grow=lambda e, elapsed: True, yield_=lambda e, size: 1.0)
interp, world = make_world_interpreter(world=W.World(size=8, models=models))
interp.run_source("""
for i in range(get_world_size()):
    if can_harvest():
        harvest()
    plant(Entities.Grass)
    move(East)
""")
print(world.ticks, world.num_items("Hay"))
```

## Deliberately out of scope

No bytecode VM, no optimizer, no compiler back end — tree-walking is the point. No attempt to
match the game's real timing beyond the documented tick costs, and no reproduction of its error
message wording. This never becomes a headless way to play the game: a curated script running end
to end is a bonus, never a requirement.

## Sources

| Claim | Source |
|---|---|
| The language subset and its semantics | The pages in this *Language* section, each derived from the official CC0 `scripting/` docs |
| Every tick cost the world charges | The ✅ sourced table on [Measured Numbers](../mechanics/measured-numbers.md) |
| The torus, verbs and constants | [Drones](../mechanics/drones.md), [API Reference](../api/reference.md) |
| What is *not* public about the real interpreter | [About the Game](../about/the-game.md) |
