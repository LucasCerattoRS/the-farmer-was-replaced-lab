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

Vem mais por aí: solver da maçã do dinossauro, otimização de policultura, caça a seeds com `simulate()`.
