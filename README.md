# The Farmer Was Replaced — Lab

[![Deploy docs](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/actions/workflows/pages.yml/badge.svg)](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**📖 [Read the docs →](https://lucascerattors.github.io/the-farmer-was-replaced-lab/)** · 🇧🇷 [Leia em português](README.pt-BR.md)

An unofficial **study lab** for [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/) —
the game where you program a farming drone in a Python-like language.

This repository is two things at once:

- A **documentation site** (English + Brazilian Portuguese) covering every system in the
  game: crops, drones, polyculture, cactus sorting, mazes, dinosaurs, leaderboards and
  simulation — plus a progression roadmap and step-by-step tutorials.
- A **curated collection of 42 working scripts**, imported straight from an end-game save
  (billions farmed, all techs unlocked, leaderboard runs) and kept in sync with it.

Everything documented on the site is backed by code that actually ran.

## What's in here

| Folder | What's inside |
|---|---|
| `docs/` | The MkDocs Material site — `docs/en/` and `docs/pt/`, 17 pages each |
| `farms/basics/` | Plant helpers, first farms, tiny experiments (error handling, import cycles) |
| `farms/crops/` | Pumpkin megafarms, sunflower genetics, polycultures, three cactus sorting algorithms |
| `farms/mazes/` | Gold farming: wall-followers, iterative DFS, BFS with up to 25 drones |
| `farms/dinosaur/` | Apple minigame solver and snake-pattern bone farming |
| `farms/leaderboards/` | Competition-grade runs, including a full automated reset |
| `farms/lib/` | The game's own `__builtins__.py` API stub, for IDE autocomplete |
| `tools/` | Save sync and Markdown → Steam BBCode conversion |

Annotated index of every script: [`farms/README.md`](farms/README.md).

## Building the docs locally

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install mkdocs-material mkdocs-static-i18n
.venv/Scripts/mkdocs.exe serve
```

Then open <http://127.0.0.1:8000>. CI builds with `--strict` and anchor validation on, so a
broken link or a dangling `#anchor` fails the build rather than shipping quietly.

## Tools

**`tools/sync_save.ps1`** — imports the game's save files into this repo's curated layout.
Dry-run by default; reports `NEW / CHANGED / OK / UNMAPPED` and only copies with `-Apply`.
The filename mapping lives in `tools/sync_map.json`.

```powershell
.\tools\sync_save.ps1            # dry-run
.\tools\sync_save.ps1 -Apply     # actually copy
```

**`tools/steam_bbcode.py`** — converts a tutorial page into Steam guide BBCode.

```bash
python tools/steam_bbcode.py docs/en/tutorials/01-multi-drone.md | clip
```

## Where the game keeps your code (Windows)

```text
%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<save-name>\
```

Each in-game code window is a `.py` file there, alongside `__builtins__.py` (the API stub the
game generates) and `save.json`.

## License & disclaimer

Code and documentation in this repository are [MIT licensed](LICENSE).

This is an **unofficial fan project**, not affiliated with the game's developer. All game
content, names and mechanics belong to their respective owners.
