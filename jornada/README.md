# Jornada — do zero, de novo

Um save novo (`Saves/pygame2`), jogado do início, com diário de cada sessão.
O save end-game antigo (`Saves/pygame`) continua sendo a fonte de `farms/` — não mexer.

- Uma nota por sessão: `AAAA-MM-DD-sessao-NN.md`.
- No fim da sessão: `tools/snapshot_jornada.sh` copia os scripts do save pra `codigo/`
  e o `save.json` (desbloqueios) pra cá. Commit → o `git log -p jornada/` é a história.
- Medição da Track 2 (issue #1) que ficar possível no caminho: anotar na sessão e
  levar o número pro `docs/*/mechanics/measured-numbers.md`.

## Modelo de nota

```markdown
# Sessão NN — AAAA-MM-DD

**Desbloqueado:** …
**O que fiz / código novo:** …
**O que aprendi (ou relembrei):** …
**Dúvida / hipótese pra testar:** …
**Medição feita:** — (ou o número + script usado)
```
