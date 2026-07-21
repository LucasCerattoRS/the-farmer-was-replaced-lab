# About the Game

*The Farmer Was Replaced* is a programming game: you write code in a Python-like language to
drive a farming drone, and the research tree hands you language features — loops, variables,
functions, lists — as unlockables. This page is the short, fully-cited account of who built it
and what is (and isn't) publicly known about how it works.

> Everything here is sourced from files the game ships on disk or from its Steam store page.
> Where something isn't published, this page says so rather than guessing — see
> [Sources](#sources).

## Who made it

The game is essentially a **solo project**. The shipped `credits.md` lists one person for
programming, game design *and* art:

| Role | Person |
|---|---|
| Programming, Game Design and Art | **Timon Herzog** |
| Music and Sound Effects | **Floris Demandt** |
| Key Art | **Stephanie Stutz** |
| Published by | **Metaroot** — Andri Weidmann, Flurin Weidmann, Nathalie Weidmann |

Steam lists the developer as **Timon Herzog** and the publisher as **Metaroot** and
**Timon Herzog**.

## Release history

| Milestone | Date |
|---|---|
| Early Access release | **10 February 2023** |
| 1.0 full release | **10 October 2025** |

Both dates are as stated on the [Steam store page](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)
(app ID `2060160`) — the game spent roughly two and a half years in Early Access.

## Engine and language

The game is built in **Unity**. That is visible directly in the install directory, which has the
standard Unity layout: `UnityPlayer.dll`, `UnityCrashHandler64.exe`, a `MonoBleedingEdge/`
runtime folder, and a `TheFarmerWasReplaced_Data/` folder with `StreamingAssets/`.

The in-game language is a **custom interpreter** for a Python subset — not CPython embedded. It
has its own semantics that this site documents in the [Language](../language/values-and-variables.md)
section: every number is a float, modules are *windows* rather than files, and infinite loops are
safe because the runtime puts a delay between iterations.

!!! warning "What is *not* public"
    There is **no published devlog, postmortem or technical article** about how the interpreter
    is implemented. Beyond "Unity, custom interpreter," the internals are not documented anywhere
    public.

    This is why this repo documents **behaviour, not implementation**. Every mechanism described
    across the site is traced to the shipped docs, the `builtins.py` stub, or a script that
    actually ran — never to a guess about what the interpreter does under the hood. A plausible
    explanation that turns out wrong is worse than no explanation, and that failure mode has
    already bitten this repo once.

## The CC0 documentation decision

The most unusual thing the developer did, from a documentation standpoint: **the game ships its
entire in-game documentation on disk, in the public domain.**

```
…\steamapps\common\The Farmer Was Replaced\
  TheFarmerWasReplaced_Data\StreamingAssets\Languages\
```

- The `LICENSE` in that folder is **CC0 1.0 Universal** — a public-domain dedication.
- It contains **47 markdown files per language across 14 languages**, including Portuguese, plus
  a canonical `builtins.py` API stub (51 definitions).
- The `Languages/README.md` explains the layout and invites corrections, and the developer
  maintains a **public translation repo that accepts pull requests**:
  <https://github.com/Timiodon/TFWR-Translations>.

What that enables is exactly this project. Because the docs are CC0, they can legally be quoted,
translated, reorganised and built upon — so this site can derive a
[language reference](../language/values-and-variables.md) and an
[API reference](../api/reference.md) from a primary source instead of guessing from play. The
developer also admits in that README that some translations are machine-generated and asks for
fixes, which is an open door for contributing back.

!!! note "Derived, not copied"
    CC0 makes copying legal, but restating the official text adds nothing. The value this repo
    adds is synthesis, cross-linking, and the code evidence in
    [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms).

## Full credits

Reproduced from the shipped `EN/docs/credits.md` (CC0).

**Programming, Game Design and Art** — Timon Herzog
**Music and Sound Effects** — Floris Demandt
**Key Art** — Stephanie Stutz

**Published by Metaroot** — Andri Weidmann · Flurin Weidmann · Nathalie Weidmann

**Allcorrect** — Maria Pavlova (Russian) · Evgeniia Ushakova (Russian) · Melanie Chen (Chinese) ·
Siyoon Ji (Korean) · Mina Horiba-Maguire (Japanese) · Danil Belousov (Account Manager) ·
Elizaveta Shevchenko (Team Lead) · Yulia Tregubova (Project Manager)

**Community Translation Contributors** — HoshiyomiLusia · Liuxun · Davide Altamura ·
Milan Tuma · Ivan Bondar · Jimmy Sheep · Taigo Nakajima · НУІ

**Discord Moderators** — MrBlobfish · Josh Markey · danielrab · Jeff Siebold aka Noon Knight

**Special Thanks** — Jonas Bornhöft · ThatMerlinGuy · Zoroark Zwart · Ramón Buchenberger ·
Swiss Game Hub

## Sources

| Claim | Source |
|---|---|
| Credits, roles, translator and moderator names | `…\Languages\EN\docs\credits.md` (shipped, CC0) |
| Docs are public domain | `…\Languages\LICENSE` — CC0 1.0 Universal |
| 47 docs × 14 languages, canonical `builtins.py` | The `Languages\` folder itself |
| Translation repo accepts PRs; some translations are machine-made | `…\Languages\README.md` |
| Engine is Unity | Install dir: `UnityPlayer.dll`, `UnityCrashHandler64.exe`, `MonoBleedingEdge/` |
| Release dates, developer, publisher | [Steam store page](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/), app `2060160` |
| Interpreter internals | **Not published.** No devlog or postmortem exists. |

---

!!! note "Unofficial fan project"
    This site is not affiliated with the developer or publisher. All game content belongs to its
    respective owners.
