# Interpretador: verbo `get_water()`

- **SHA base:** `b857e2fcaf4c1c4b108817493b052ae41778790a` (origin/main)
- **Branch:** `claude/task-j2d4xa`
- **Antes de editar:** `get_water` não existia em `interpreter/tfwrlang/builtins.py` (confirmado por leitura do arquivo).
  A branch WIP `claude/kit-pesquisa-offline` não foi lida nem alterada.

## O que mudou
- `builtins.py`: `get_water()` devolve `float(world.tile().water)` e cobra **1 tick**.
- `tests/test_world.py`: `test_get_water_reads_current_tile_follows_position_and_costs_one_tick` — verifica o tile atual,
  a mudança após `move(East)` e o custo (1 tick no sensor; 200 + 1 após o move).

## Fontes usadas
- `docs/en/api/reference.md`: `get_water()` → `float`, nível de água 0–1 sob o drone.
- `docs/en/mechanics/measured-numbers.md`: `get_water()` está no grupo de 1 tick.

## Comandos e resultados
- `python -m pytest interpreter/tests -q` → 57 passed
- `python interpreter/parse_corpus.py` → "Milestone 5a: OK"; 45/46 parseiam, o resto é o holdout já conhecido (`farms/mazes/maze_gold_dfs.py`, slicing)
- `python interpreter/gen_unspecified.py --check` → "UNSPECIFIED.md is up to date" (rc=0)

## Limites
- Nenhuma fonte versionada define como a água de um tile muda (`use_item(Items.Water)`, evaporação, efeito no crescimento).
  Todo tile começa em `0.0` e só muda se o teste/o chamador atribuir `tile.water`. Nada disso foi inventado.
- `use_item` continua ausente. Documentação do site não alterada (a referência já lista o verbo).
- Sem acesso ao jogo real.

## Próximo passo
- Decidir, com medição, como modelar `use_item(Items.Water)` e a dinâmica da água (provável novo item em `UNSPECIFIED`).
