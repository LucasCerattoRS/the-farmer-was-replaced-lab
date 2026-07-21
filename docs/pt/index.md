# The Farmer Was Replaced — Lab

Um **laboratório de estudo** não-oficial sobre [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/) — o jogo em que você programa um drone agrícola numa linguagem parecida com Python.

Este site reúne tudo que foi aprendido ao longo de uma campanha inteira até o end-game (bilhões de recursos, tecnologias todas destravadas, runs de leaderboard):

- **[Primeiros Passos](getting-started.md)** — o que é o jogo e como a linguagem dele funciona.
- **[Linguagem](language/values-and-variables.md)** — a referência sistemática do subconjunto de Python do jogo: valores, operadores, controle de fluxo, funções e escopo, coleções, módulos.
- **[Mecânicas](mechanics/crops.md)** — mergulho em cada sistema: culturas, drones, policultura, ordenação de cactos, labirintos, dinossauros, leaderboards e simulação.
- **[Guias](guides/progression.md)** — um roteiro de progressão do primeiro tufo de grama até runs de Fastest Reset.
- **[Tutoriais](tutorials/index.md)** — passo a passo, prontos para virar guia da Steam.
- **[Referência da API](api/reference.md)** — cada função e constante embutida, documentada.
- **[Números Medidos](mechanics/measured-numbers.md)** — a tabela completa de custos em ticks, e quais números deste site têm fonte vs. ainda não foram medidos.
- **[Sobre o Jogo](about/the-game.md)** — quem construiu, o histórico de lançamento, e a decisão de licenciar a doc em CC0 que torna este projeto possível.

Toda estratégia aqui é respaldada por **código real, que funciona**, na pasta [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms) do repositório — curada direto de um save de end-game.

!!! note "Projeto de fã, não-oficial"
    Este projeto não tem vínculo com a desenvolvedora do jogo. Todo o conteúdo do jogo pertence aos seus respectivos donos.

## Tour rápido pela coleção de código

| Pasta | O que tem dentro |
|---|---|
| `farms/basics/` | Helpers de plantio, primeiras farms, experimentos pequenos (tratamento de erro, ciclos de import) |
| `farms/crops/` | Megafarms de abóbora, genética de girassol, policulturas, três algoritmos de ordenação de cactos |
| `farms/mazes/` | Farming de ouro: wall-followers, DFS iterativo, BFS com até 25 drones |
| `farms/dinosaur/` | Solver do minigame da maçã e farming de ossos em padrão de cobra |
| `farms/leaderboards/` | Runs de nível competitivo, incluindo um reset totalmente automatizado |
| `farms/research/` | Instrumentos de medição: custos em ticks, tempos de crescimento, taxa de morte da abóbora, distribuição de pétalas, cadeia de cactos |
| `farms/lib/` | O próprio stub `__builtins__.py` do jogo, para autocomplete na IDE |
