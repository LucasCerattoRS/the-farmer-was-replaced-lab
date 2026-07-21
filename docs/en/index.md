# The Farmer Was Replaced — Lab

An unofficial **study lab** for [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/) — the game where you program a farming drone in a Python-like language.

This site collects everything learned across a full playthrough into end-game (billions of resources, all techs unlocked, leaderboard runs):

- **[Getting Started](getting-started.md)** — what the game is and how its language works.
- **[Language](language/values-and-variables.md)** — the systematic reference for the in-game Python subset: values, operators, control flow, functions and scope, collections, modules.
- **[Mechanics](mechanics/crops.md)** — deep dives into every system: crops, drones, polyculture, cactus sorting, mazes, dinosaurs, leaderboards and simulation.
- **[Guides](guides/progression.md)** — a progression roadmap from the first patch of grass to Fastest Reset runs.
- **[Tutorials](tutorials/index.md)** — step-by-step, Steam-guide-ready walkthroughs.
- **[API Reference](api/reference.md)** — every built-in function and constant, documented.
- **[Measured Numbers](mechanics/measured-numbers.md)** — the complete tick-cost table, and which of this site's numbers are sourced vs. still unmeasured.
- **[About the Game](about/the-game.md)** — who built it, the release history, and the CC0 documentation decision that makes this project possible.

All strategies are backed by **real, working code** in the [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms) folder of the repository — curated straight from an end-game save.

!!! note "Unofficial fan project"
    This project is not affiliated with the game's developer. All game content belongs to its respective owners.

## Quick tour of the code collection

| Folder | What's inside |
|---|---|
| `farms/basics/` | Plant helpers, first farms, tiny experiments (error handling, import cycles) |
| `farms/crops/` | Pumpkin megafarms, sunflower genetics, polycultures, three cactus sorting algorithms |
| `farms/mazes/` | Gold farming: wall-followers, iterative DFS, BFS with up to 25 drones |
| `farms/dinosaur/` | Apple minigame solver and snake-pattern bone farming |
| `farms/leaderboards/` | Competition-grade runs, including a full automated reset |
| `farms/research/` | Measurement instruments: tick costs, grow times, pumpkin death rate, petal distribution, cactus chaining |
| `farms/lib/` | The game's own `__builtins__.py` API stub, for IDE autocomplete |
