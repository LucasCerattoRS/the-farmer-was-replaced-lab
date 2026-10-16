# Comandos documentados que falhavam

- **Base:** `origin/main` @ `e7967d5` · **Branch:** `claude/farmer-lab-comandos-docs`

## O que mudou
- `python tools/validar_stub.py` (citado no README.pt-BR) saía com código 1 por causa do `error_demo.py`, que erra de propósito. O erro esperado agora vive em `tools/validar_stub.py` (`ESPERADO`); na varredura padrão é ignorado e contado na saída, e com arquivo explícito continua valendo.
- Novo teste `test_comando_documentado_do_validador_sai_com_zero` (varredura padrão → 0; `error_demo.py` explícito → 1).
- Novo teste `test_comandos_dos_docs_apontam_para_arquivos_que_existem`: cada `python x.py` / `.\x.ps1` / `sh x.sh` em blocos de código dos `.md` precisa apontar para arquivo existente (mutação com caminho trocado → teste falha).
- CI: passo extra que roda `python tools/validar_stub.py`.

## Testes
- `python -m pytest tests/ interpreter/tests/` → 64 passed. `mkdocs build --strict` → ok. `parse_corpus.py` e `gen_unspecified.py --check` → ok.

## Limites / pendências
- Validação estática: nenhum script foi executado no jogo.
- Não corrigido: README cita "42 scripts"/"56 testes" (hoje 46 / 57+); `.venv/Scripts/...` nos docs é só Windows; `sync_save.py` (Linux) não é citado nos READMEs.

## Revisão (16/10/2026)
- Falso negativo: o regex exigia espaço depois de `.\`, então `.\tools\sync_save.ps1` nunca era checado (mutação com caminho trocado passava). Extrator virou `comandos_em()` e aceita `.\x.ps1` / `./x.sh`; novo `test_extrator_reconhece_python_ps1_e_sh` (falhava antes da correção).
- `python -m pytest tests/ interpreter/tests/` → 65 passed; mutação em `.\tools\sync_save.ps1` no README.md agora falha o teste.
