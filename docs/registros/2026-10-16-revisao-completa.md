# Revisão completa do laboratório

- **Base:** `origin/main` @ `6eec40e` · **Branch:** `claude/farmer-lab-revisao`

## O que mudou
- `tools/validar_stub.py`: confere scripts contra `farms/lib/__builtins__.py` (existência, número de argumentos, membros de `Items`/`Entities`/…).
- **Erro 1:** `farms/mazes/treasure_hunt_8drones_buy.py` chamava `buy()`, que não existe no stub (NameError no jogo). Agora só checa o estoque e devolve `False` se faltar Weird Substance.
- **Erro 2:** `farms/README.md` não listava os 5 scripts de `farms/research/` e descrevia o script acima como "compra".
- `farms/TRILHA.md`: 11 degraus, conceito + 3 exercícios cada.
- `.github/workflows/ci.yml`: testes em pull request (antes só rodava no push em `main`, junto do deploy).

## Testes
- `python -m pytest tests/ interpreter/tests/` → 62 passed (5 novos + 57 existentes). Os 2 testes dos erros falham antes das correções e passam depois.
- `parse_corpus.py` → 45/46 (holdout conhecido: fatiamento); `gen_unspecified.py --check` → em dia; `mkdocs build --strict` → sem erro.

## Pendências / não validado
- Nenhum script rodou no jogo real; a validação é estática (nomes, aridade, membros).
- `error_demo.py` chama `Make_Error()` de propósito (listado como esperado no teste).
- README diz "42 scripts" e "56 testes" (hoje: 46 scripts em `farms/`, 57 testes do interpretador); não corrigido por estar fora do limite de 3 erros.
