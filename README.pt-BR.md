# The Farmer Was Replaced — Lab

[![Deploy docs](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/actions/workflows/pages.yml/badge.svg)](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/actions/workflows/pages.yml)
[![Licença: MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)](LICENSE)

**📖 [Leia a documentação →](https://lucascerattors.github.io/the-farmer-was-replaced-lab/pt/)** · 🇬🇧 [Read in English](README.md)

Um **laboratório de estudo** não-oficial sobre [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/) —
o jogo em que você programa um drone agrícola numa linguagem parecida com Python.

Este repositório é duas coisas ao mesmo tempo:

- Um **site de documentação** (inglês + português do Brasil) cobrindo todo sistema do jogo:
  culturas, drones, policultura, ordenação de cactos, labirintos, dinossauros, leaderboards e
  simulação — mais um roteiro de progressão e tutoriais passo a passo.
- Uma **coleção curada de 42 scripts funcionais**, importados direto de um save de end-game
  (bilhões cultivados, tecnologias todas destravadas, runs de leaderboard) e mantidos em
  sincronia com ele.

Tudo que está documentado no site é respaldado por código que de fato rodou.

## O que tem aqui

| Pasta | O que tem dentro |
|---|---|
| `docs/` | O site MkDocs Material — `docs/en/` e `docs/pt/`, 17 páginas cada |
| `farms/basics/` | Helpers de plantio, primeiras farms, experimentos pequenos (tratamento de erro, ciclos de import) |
| `farms/crops/` | Megafarms de abóbora, genética de girassol, policulturas, três algoritmos de ordenação de cactos |
| `farms/mazes/` | Farming de ouro: wall-followers, DFS iterativo, BFS com até 25 drones |
| `farms/dinosaur/` | Solver do minigame da maçã e farming de ossos em padrão de cobra |
| `farms/leaderboards/` | Runs de nível competitivo, incluindo um reset totalmente automatizado |
| `farms/lib/` | O próprio stub `__builtins__.py` do jogo, para autocomplete na IDE |
| `interpreter/` | Modelo executável da linguagem documentada (lexer, parser, avaliador, mundo) + testes |
| `jornada/` | Diário de um save novo jogado do zero (`Saves/pygame2`) |
| `tools/` | Sincronização do save e conversão de Markdown → BBCode da Steam |

Índice anotado de cada script: [`farms/README.md`](farms/README.md).

## Buildando os docs localmente

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install mkdocs-material mkdocs-static-i18n
.venv/Scripts/mkdocs.exe serve
```

Aí abra <http://127.0.0.1:8000>. O CI builda com `--strict` e validação de âncora ligada,
então link quebrado ou `#âncora` órfã derruba o build em vez de passar batido.

## Ferramentas

**`tools/sync_save.ps1`** — importa os arquivos do save do jogo para o layout curado deste
repo. Dry-run por padrão; reporta `NEW / CHANGED / OK / UNMAPPED` e só copia com `-Apply`.
O mapeamento de nomes fica em `tools/sync_map.json`.

```powershell
.\tools\sync_save.ps1            # dry-run
.\tools\sync_save.ps1 -Apply     # copia de verdade
```

**`tools/steam_bbcode.py`** — converte uma página de tutorial em BBCode de guia da Steam.

```bash
python tools/steam_bbcode.py docs/pt/tutorials/01-multi-drone.md | clip
```

## Estado (out/2026)

- Site no ar via GitHub Pages; **todo push em `main` publica** (`.github/workflows/pages.yml`),
  depois de rodar os testes do interpretador.
- Interpretador de referência (Track 5 do `ROADMAP.md`): 5a–5c prontas, 56 testes verdes.
- Track 2 (medir números do jogo: custo de tick, tempo de crescimento, taxa de morte da abóbora)
  ainda aberta — ver `ROADMAP.md` e a issue #1.

## Como rodar o interpretador e os testes

Python 3.12+, só biblioteca padrão (+ `pytest` para os testes):

```bash
python interpreter/parse_corpus.py          # parseia todos os scripts de farms/
python -m pytest interpreter/tests/         # testes de comportamento
python interpreter/gen_unspecified.py --check  # UNSPECIFIED.md em dia com o catálogo
```

## Tecnologias

Python puro (interpretador e ferramentas), MkDocs Material + `mkdocs-static-i18n` (site
bilíngue), GitHub Actions (teste → build → deploy no Pages), PowerShell (`sync_save.ps1`).

## Pendências

- Track 2 do roadmap: medições empíricas no jogo (preenchem `mechanics/measured-numbers.md`).
- Track 5d: ligar o interpretador de volta às páginas do site.
- `farms/mazes/maze_gold_dfs.py` usa fatiamento (`a[i:j]`), fora do subconjunto documentado —
  o parser recusa de propósito (é um achado registrado, não um bug).
- Revisão de 08/10: comparações encadeadas (`a < b < c`) agora são recusadas com
  `NotSupported` em vez de calcular `(a < b) < c` em silêncio; `a[f()] += 1` passou a avaliar
  o índice uma vez só. Ambos com teste em `interpreter/tests/test_operators.py`.

## Para estudar

1. **Indentação vira token** — `interpreter/tfwrlang/lexer.py:50` (`tokenize`): uma pilha de
   colunas emite `INDENT`/`DEDENT`, igual ao CPython; colchetes abertos suspendem isso
   (linha 55, `depth`), por isso listas podem quebrar linha.
2. **Descida recursiva com precedência** — `interpreter/tfwrlang/parser.py:242` em diante: cada
   nível de precedência é uma função (`parse_or` → `parse_and` → … → `parse_power`); `**` é
   associativo à direita porque `parse_power` chama `parse_unary` no lado direito.
3. **Controle de fluxo por exceção** — `interpreter/tfwrlang/interp.py:25-35`: `break`,
   `continue` e `return` são exceções Python capturadas pelo laço/função mais próximo.
4. **"Falhe alto onde a documentação cala"** — `interpreter/tfwrlang/errors.py:50`
   (`UNSPECIFIED_CATALOG`) e `interp.py:479` (`as_bool`): em vez de herdar a resposta do
   Python, o modelo levanta `Unspecified`, e o catálogo gera `UNSPECIFIED.md` sozinho.

## Onde o jogo guarda seu código (Windows)

```text
%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<nome-do-save>\
```

Cada janela de código do jogo é um arquivo `.py` ali, junto com o `__builtins__.py` (o stub da
API que o jogo gera) e o `save.json`.

## Licença & aviso

Código e documentação deste repositório estão sob a [licença MIT](LICENSE).

Este é um **projeto de fã, não-oficial**, sem vínculo com a desenvolvedora do jogo. Todo o
conteúdo, nomes e mecânicas do jogo pertencem aos seus respectivos donos.
