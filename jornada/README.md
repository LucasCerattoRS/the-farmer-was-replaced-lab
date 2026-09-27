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

## Objetivo 2 — entender como o jogo foi feito (engenharia reversa)

Em paralelo ao jogar: como o jogo opera por dentro, como foi produzido, mecanismos de
desenvolvimento. Ponto de partida levantado em 2026-09-27:

- **Unity com backend Mono (não IL2CPP)** → a lógica está em DLLs .NET legíveis por
  descompilador (ILSpy / dnSpy / `ilspycmd`), em `TheFarmerWasReplaced_Data/Managed/`:
  - `Core.dll` (340 KB) — provável núcleo (interpretador? mundo?) — **a verificar**
  - `Utils.dll` (267 KB), `NewAssembly.dll` (8 KB), `Assembly-CSharp.dll` (12 KB, quase vazio)
  - `FMODUnity.dll` (áudio FMOD), `com.rlabrecque.steamworks.net.dll` (Steamworks.NET)
- Assets: `resources.assets`, `sharedassets0.assets`, `level0` (AssetRipper / UABEA abrem).
- Docs oficiais CC0 em `StreamingAssets/Languages/` (já usadas no site).

**Regras:** o código descompilado é do Timon (copyright) → fica **só local**, fora do repo
(`~/tfwr-re/`). No repo entram as *nossas* notas e explicações. Toda afirmação sobre
implementação cita classe/método de onde saiu — nada de chute (lição da `language-quirks.md`).
Isso também resolve itens do `UNSPECIFIED.md` / Track 2 lendo a fonte em vez de medir.
