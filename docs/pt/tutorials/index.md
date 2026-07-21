# Tutoriais

Passo a passo escritos pra serem **copiados e colados direto em guias da Steam**.
Cada um é autocontido, usa código real deste repositório e evita formatação específica
do site, então converte limpo pra BBCode:

```text
python tools/steam_bbcode.py docs/pt/tutorials/01-multi-drone.md | clip
```

| # | Tutorial | O que você vai aprender |
|---|---|---|
| 01 | [Farming Multi-Drone](01-multi-drone.md) | O padrão de divisão por colunas que multiplica o throughput de qualquer farm |
| 02 | [Ordenação de Cactos](02-cactus-sorting.md) | Colheita em cadeia via ordenação por swap: insertion, shaker e "vácuo" |
| 03 | [Farmando Ouro em Labirintos](03-maze-gold.md) | Wall-followers, DFS e caça ao tesouro guiada por `measure()` |
| 04 | [O Solver da Maçã do Dinossauro](04-dinosaur-apple.md) | Perseguição de maçã em dois estágios, e saber a hora de parar de perseguir |
| 05 | [Otimização de Policultura](05-polyculture.md) | Uma fila de pedidos compartilhada entre 8 drones — e os dois bugs que ela teve que corrigir |
| 06 | [Caça a Seeds com `simulate()`](06-seed-hunting.md) | Transformando o `simulate()` numa função de fitness que dá pra otimizar |

Não coberto aqui, mas vale a leitura direta: as arestas da linguagem estão reunidas em
[Peculiaridades da Linguagem](../mechanics/language-quirks.md).
