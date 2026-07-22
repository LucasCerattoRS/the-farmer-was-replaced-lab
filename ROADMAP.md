# Roadmap

Working document. The site covers *how to play well*; this is the plan to make it cover
*how the thing actually works*, from the fundamentals up — without turning into a taxonomy of
everything.

Tick items as they land. Keep the ground rules below — they are the reason this repo is worth
more than a wiki.

---

## Ground rules

1. **Every claim needs a source.** One of: the shipped official docs (CC0), the `builtins.py`
   stub, a script in `farms/` that actually ran, or a measurement we took ourselves. If none
   of those apply, the honest move is to say "not documented" and stop.
2. **Never explain a mechanism you haven't verified.** A plausible explanation that turns out
   wrong is worse than no explanation — it is the failure mode that already bit this repo
   (see Track 0).
3. **Cite where a fact came from** when it isn't obvious. Especially for measured numbers.
4. **Derived, not copied.** The official docs are CC0 so copying is *legal*, but the value we
   add is synthesis, cross-linking and the code evidence. Restating their text adds nothing.
5. **Both languages stay in sync**, and `mkdocs build --strict` (with anchor validation) must
   pass before any commit.

## Primary sources

| Source | Where | Notes |
|---|---|---|
| Official in-game docs | `…\steamapps\common\The Farmer Was Replaced\TheFarmerWasReplaced_Data\StreamingAssets\Languages\` | **CC0 1.0** (public domain). 47 `.md` per language × 14 languages, incl. `PT`. 1210 lines in EN. |
| Canonical API stub | same folder, `builtins.py` | **2321 lines, 51 defs** — nearly double the save-generated `farms/lib/__builtins__.py` (1307 lines, 44 defs) |
| Dev's translation repo | <https://github.com/Timiodon/TFWR-Translations> | Public, accepts PRs |
| Credits | `EN/docs/credits.md` | Timon Herzog (programming, game design, art), Floris Demandt (music/SFX), published by Metaroot |

**Not available, do not fake it:** there is no published devlog, postmortem or technical
article about the interpreter's implementation. The engine is Unity and the language is a
custom interpreter — beyond that, internals are not public. Document *semantics*, not guesses
about implementation.

---

## Track 0 — Corrections (do first; these are published and wrong)

- [x] **`mechanics/language-quirks.md` — the import-cycle explanation was wrong.** It claimed
      cycles work "because the imports sit inside the functions, which keeps the cycle from
      resolving at load time." The official `scripting/import.md` shows top-level `import a` /
      `import b` cycles work fine, and gives the real mechanism: the second file gets a
      reference to the *half-loaded* module and reads it later, once it's complete. The actual
      failure case is `from x import *` in a cycle, which snapshots an empty namespace.
      Rewritten from the official explanation. (EN + PT)
- [x] **Same page was missing `if __name__ == "__main__":`** entirely — the game supports it and
      its own docs call it good practice, because a bare `import` *executes the file* (harvesting
      included) the first time. Added to the import section. (EN + PT)
- [x] **`api/reference.md` was built from the smaller stub.** Added the 5 collection methods
      absent from the save stub (`append`, `insert`, `pop`, `remove`, `add`) with tick costs
      from the canonical `builtins.py`, and repointed the provenance line at that 51-def file.
      (EN + PT)
- [x] **`spawn_drone` was documented as taking no arguments — false.** The canonical
      `builtins.py` documents `spawn_drone(task, *args)` and its example passes one
      (`spawn_drone(harvest_column, i)`). The save stub the curated scripts use declares
      `spawn_drone(function)` with no extra params, which is why every farm here parameterizes
      through closures / position inheritance. Corrected the claim everywhere it appeared:
      `drones.md`, `language-quirks.md`, `tutorials/05-polyculture.md`, `api/reference.md`
      (EN + PT). Same failure mode as the import bug — found during the API audit above.

## Track 1 — Language reference (the "fundamentals" layer)

New section, derived from the official `scripting/` docs (766 lines) plus what the scripts in
`farms/` actually demonstrate. The site currently has no systematic language coverage at all.

- [x] `language/values-and-variables.md` — types, assignment, truthiness (`variables.md`)
- [x] `language/operators.md` — arithmetic, comparison, logic, precedence (`operators.md`, 75 lines)
- [x] `language/control-flow.md` — `if` / `while` / `for` / `break` / `continue`
- [x] `language/functions-and-scope.md` — `def`, arguments, `global`, closures. Merge
      `functions.md` (90 lines) + `scopes.md` (60 lines); this is where the closure-factory
      pattern finally has a proper home
- [x] `language/collections.md` — lists, dicts, sets, tuples, and which operations exist
- [x] `language/modules-and-imports.md` — the corrected import story, module caching, side
      effects, `__name__`, cycles. Supersedes the quirks-page section
- [x] Wire into nav (EN + PT `nav_translations`), and point `language-quirks.md` at it —
      quirks stays as the *surprising* subset, not the reference

## Track 2 — Empirical research (measure the game)

The part nobody else has done systematically. `get_tick_count()` is free to call and
`simulate()` returns elapsed time, so the game is instrumentable.

- [x] Build `farms/research/` with measurement scripts, each printing a clean table —
      `tick_costs.py`, `grow_times.py`, `pumpkin_death_rate.py`, `sunflower_petals.py`,
      `cactus_chain.py` (commit `396b974`). **Written and reviewed, not yet run in game**
- [ ] **Tick cost per operation** — `move`, `harvest`, `plant`, `till`, `swap`, `measure`,
      `use_item`, `spawn_drone`. The stub documents some; verify all and find the undocumented
- [ ] **Grow times per entity** vs. the "~0.5s / ~4s / ~7s" figures the docs currently assert
- [ ] **Pumpkin death rate** — the site claims "about 1 in 5"; measure it over a large N
- [ ] **Sunflower petal distribution** — is 15 uniform across the range?
- [ ] **Cactus chain-harvest payout** vs. field sortedness
- [ ] `mechanics/measured-numbers.md` publishing results with method, sample size and the
      script that produced each one. Where a measurement contradicts a current page, fix the page
      — **page shipped in `396b974` with the ✅ sourced tick-cost table complete; every measured
      number is still ⏳ and stays empty until the batch run**

> Track 2 needs the game running to collect data. The scripts can be written and reviewed
> first, then run in a batch.

## Track 3 — About the game

One page. Short, fully cited, honest about the gaps.

- [x] `about/the-game.md` — Timon Herzog, Metaroot, Unity, full shipped credits, release
      history, the CC0 documentation decision and what it enables. Explicitly notes that the
      interpreter implementation is not public, so this repo documents behaviour, not internals

## Track 4 — Contribute back

The official PT translation is partly machine-translated by the dev's own admission
(`Languages/README.md`), and this repo just produced a careful PT translation of ~1500 lines
of the same subject matter.

- [x] Read the official `PT/docs` against `EN/docs` and log concrete errors — full audit in
      [`tools/translation-audit.md`](tools/translation-audit.md). Mechanical checks (placeholders,
      `@Key` structure, numbers, code spans) came back **clean**; scope covered all 16
      `PT/docs/scripting/` files + all 14 `Strings/*.txt`, skipping `docs/unlocks/` (README says
      those change). Two concrete errors found.
- [x] Check terminology consistency both ways — done in the audit. No changes to this site were
      required; our English-kept `set`/`dict` are actually closer to the upstream guideline than
      the official "Conjuntos"/"Dicionários".
- [x] Open a PR on `Timiodon/TFWR-Translations` (their README asks for the name to credit) —
      **[#32](https://github.com/Timiodon/TFWR-Translations/pull/32)**: untranslate the
      `"Variables"` unlock name in `operators.md`, fix misplaced backticks in `tuples.md`.
      Credited to Lucas Ceratto (@LucasCerattoRS).
- [x] Note the outcome here — PR open and mergeable (+2/−2, 2 files).

## Track 5 — Reference interpreter (executable semantics)

Track 1 wrote down what the language does, in prose. This track makes that prose **runnable**:
a small tree-walking interpreter for the TFWR subset, in Python, in `interpreter/`.

**What it is not.** It is *not* a reimplementation of the game's interpreter, and must never be
described as one anywhere on the site — those internals are not public (see *Primary sources*).
It is a **model of the documented behaviour**: the same claims the `language/` pages make in
words, in a form that can be executed and tested.

Ground rule 2 applies here with full force, and the design enforces it mechanically: **where the
official sources are silent, the model raises `Unspecified` instead of quietly inheriting
CPython's answer.** That inverts the usual risk — every hole becomes loud instead of invisible.
Each `Unspecified` it raises is a Track 2 experiment waiting to be run, which is the main reason
this track earns its place beyond the exercise of writing it.

**Where the code lives:** `interpreter/` at the repo root, a sibling of `farms/` and `tools/` —
**not** inside `farms/`. That folder is the curated save mirror driven by
`tools/sync_map.json`; keeping authored code out of it protects the sync invariant.

### 5a — Front end

- [ ] `interpreter/tfwrlang/lexer.py` — tokens plus `NEWLINE` / `INDENT` / `DEDENT`;
      indentation-delimited blocks, as the official `scripting/` docs describe them
- [ ] `interpreter/tfwrlang/nodes.py` — one node type per construct the `language/` pages
      document, and nothing else. (Named `nodes`, not `ast`, to avoid shadowing the stdlib
      module inside the package.)
- [ ] `interpreter/tfwrlang/parser.py` — recursive descent; the precedence table comes from
      `language/operators.md`, which is itself derived from the official `operators.md`
- [ ] **Milestone — parse the whole corpus:** all 42 curated scripts in `farms/` plus the 5 in
      `farms/research/`, zero errors. The corpus already exists, it is real end-game code, and
      it makes "does the grammar match the language?" an objective question
- [ ] Every parse failure gets triaged and logged as one of: **(a)** a gap in the `language/`
      pages → fix the page; **(b)** the script uses something outside the documented subset →
      note it as a finding. Both outcomes are worth more than a clean run

### 5b — Evaluator, pure core (no game)

- [ ] `interpreter/tfwrlang/interp.py` — values and truthiness, operators, `if` / `while` /
      `for` / `break` / `continue`, `def` / call / `return`, scope + `global` + closures,
      lists / dicts / sets / tuples
- [ ] `interpreter/tfwrlang/errors.py` — `Unspecified`, and a registry recording every hole hit
- [ ] A test per behaviour the Track 1 pages already assert, each citing the page it comes from:
    - loops and branches do **not** create a scope — `i` is still `2` after `for i in range(3)`
    - closures capture, which is what makes the closure-factory pattern work
    - the call stack is finite → a depth limit that raises. The real limit is **⏳ unmeasured**:
      make it a parameter, do not invent a number
    - `while True:` exits only on `break`; with no game delay to slow it, an iteration budget
      guards the test suite
- [ ] `interpreter/UNSPECIFIED.md`, generated from the registry — the feed of new Track 2 items

### 5c — World model and built-ins

- [ ] `interpreter/tfwrlang/world.py` — an N×N **torus** grid (the wrap is documented, and it is
      the top pitfall on `drones.md`), ground / entity / water state, inventory, tick counter
- [ ] `interpreter/tfwrlang/builtins.py` — `get_pos_x` / `get_pos_y` / `get_world_size` /
      `move` / `can_move` / `get_entity_type` / `get_ground_type` / `can_harvest` / `harvest` /
      `plant` / `till` / `measure` / `num_items` / `get_tick_count` / `quick_print`, each
      charging the tick cost from the ✅ sourced table on `mechanics/measured-numbers.md`
- [ ] Grow times, pumpkin death rate and petal distribution stay **⏳** — those are precisely the
      Track 2 numbers. Model them as injected parameters that default to raising `Unspecified`
- [ ] Drones (`spawn_drone`, `wait_for`, `has_finished`) **last, and only if the scheduling
      semantics can be sourced.** Inter-drone ordering is the least documented thing in the game;
      if it can't be sourced, a documented refusal *is* the deliverable

### 5d — Wire it back into the site

- [ ] `language/reference-interpreter.md` (EN + PT) — what the model covers, what it refuses and
      why, how to run it. Leads with the "not a reimplementation" disclaimer
- [ ] Nav entry under *Language*, plus `Reference Interpreter: Interpretador de Referência` in
      `nav_translations`
- [ ] Point `mechanics/measured-numbers.md` at the generated `UNSPECIFIED.md` as a second source
      of ⏳ items, alongside `farms/research/`
- [ ] `interpreter/README.md` — how to run the tests; disclaimer in the first paragraph
- [ ] CI: add a `test` job to `.github/workflows/pages.yml` running `pytest` on Python 3.12
      (matching the existing build job), and make `build` depend on it — a red model must not
      deploy. `pytest` is a new dev dependency; the `.venv` currently only has mkdocs-material

### Scope guard — deliberately out of scope

No bytecode VM, no optimizer, no compiler back end: tree-walking is the point. No attempt to
match the game's real timing beyond the documented tick costs, and no reproduction of its error
message wording. This does not become a headless way to play the game — a curated script running
end to end is a bonus, never a requirement.

---

## Done

- Site published, bilingual EN + pt-BR, 42 pages, CI green with `--strict` + anchor validation
- 42 curated scripts, all referenced from the docs
- Root README (EN + pt-BR), 6 tutorials, language-quirks page
- **Track 1 — Language reference:** 6 new pages (values & variables, operators, control flow,
  functions & scope, collections, modules & imports), EN + pt-BR, wired into nav under a new
  *Language* section; quirks page repointed at it as the surprising subset. Build green.
- **Track 3 — About the game:** `about/the-game.md`, EN + pt-BR (commit `396b974`)
- **Track 2 — measurement kit:** 5 scripts in `farms/research/` and
  `mechanics/measured-numbers.md` with the full ✅ tick-cost table transcribed from the canonical
  `builtins.py` (commit `396b974`). The ⏳ half of the page waits on an in-game batch run
- **Track 4 — contribute back:** full PT localisation audit in `tools/translation-audit.md`
  (came back clean bar two errors); PR [#32](https://github.com/Timiodon/TFWR-Translations/pull/32)
  opened on `Timiodon/TFWR-Translations`
