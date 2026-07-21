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

- [ ] `language/values-and-variables.md` — types, assignment, truthiness (`variables.md`)
- [ ] `language/operators.md` — arithmetic, comparison, logic, precedence (`operators.md`, 75 lines)
- [ ] `language/control-flow.md` — `if` / `while` / `for` / `break` / `continue`
- [ ] `language/functions-and-scope.md` — `def`, arguments, `global`, closures. Merge
      `functions.md` (90 lines) + `scopes.md` (60 lines); this is where the closure-factory
      pattern finally has a proper home
- [ ] `language/collections.md` — lists, dicts, sets, tuples, and which operations exist
- [ ] `language/modules-and-imports.md` — the corrected import story, module caching, side
      effects, `__name__`, cycles. Supersedes the quirks-page section
- [ ] Wire into nav (EN + PT `nav_translations`), and point `language-quirks.md` at it —
      quirks stays as the *surprising* subset, not the reference

## Track 2 — Empirical research (measure the game)

The part nobody else has done systematically. `get_tick_count()` is free to call and
`simulate()` returns elapsed time, so the game is instrumentable.

- [ ] Build `farms/research/` with measurement scripts, each printing a clean table
- [ ] **Tick cost per operation** — `move`, `harvest`, `plant`, `till`, `swap`, `measure`,
      `use_item`, `spawn_drone`. The stub documents some; verify all and find the undocumented
- [ ] **Grow times per entity** vs. the "~0.5s / ~4s / ~7s" figures the docs currently assert
- [ ] **Pumpkin death rate** — the site claims "about 1 in 5"; measure it over a large N
- [ ] **Sunflower petal distribution** — is 15 uniform across the range?
- [ ] **Cactus chain-harvest payout** vs. field sortedness
- [ ] `mechanics/measured-numbers.md` publishing results with method, sample size and the
      script that produced each one. Where a measurement contradicts a current page, fix the page

> Track 2 needs the game running to collect data. The scripts can be written and reviewed
> first, then run in a batch.

## Track 3 — About the game

One page. Short, fully cited, honest about the gaps.

- [ ] `about/the-game.md` — Timon Herzog, Metaroot, Unity, full shipped credits, release
      history, the CC0 documentation decision and what it enables. Explicitly notes that the
      interpreter implementation is not public, so this repo documents behaviour, not internals

## Track 4 — Contribute back

The official PT translation is partly machine-translated by the dev's own admission
(`Languages/README.md`), and this repo just produced a careful PT translation of ~1500 lines
of the same subject matter.

- [ ] Read the official `PT/docs` against `EN/docs` and log concrete errors
- [ ] Check terminology consistency both ways — align our site with the official terms where
      theirs is better, fix theirs where ours is
- [ ] Open a PR on `Timiodon/TFWR-Translations` (their README asks for the name to credit)
- [ ] Note the outcome here

---

## Done

- Site published, bilingual EN + pt-BR, 42 pages, CI green with `--strict` + anchor validation
- 42 curated scripts, all referenced from the docs
- Root README (EN + pt-BR), 6 tutorials, language-quirks page
