"""Os scripts do repositório têm que bater com as assinaturas do stub oficial."""

import os
import re

import validar_stub as v

RAIZ = v.RAIZ
ESPERADO = v.ESPERADO


def test_validador_pega_funcao_que_nao_existe_no_stub():
    erros = v.validar_fonte("buy(Items.Hay, 5)\n", "x.py", v.carregar_stub())
    assert [m for _, m in erros] == ["buy() não é do stub nem foi definido no script"]


def test_validador_pega_aridade_e_membro_inexistente():
    stub = v.carregar_stub()
    assert v.validar_fonte("move()\n", "x.py", stub)
    assert v.validar_fonte("plant(Entities.Nada)\n", "x.py", stub)
    assert not v.validar_fonte("move(North)\nplant(Entities.Bush)\nuse_item(Items.Water)\n", "x.py", stub)


def test_todos_os_scripts_batem_com_o_stub():
    achados = set()
    stub = v.carregar_stub()
    for caminho in v.arquivos_padrao():
        rel = os.path.relpath(caminho, RAIZ).replace(os.sep, "/")
        for _, msg in v.validar_fonte(open(caminho, encoding="utf-8").read(), rel, stub):
            achados.add((rel, msg))
    assert achados == ESPERADO


def test_indice_farms_readme_cobre_todos_os_scripts():
    texto = open(os.path.join(RAIZ, "farms", "README.md"), encoding="utf-8").read()
    faltando = []
    for d, _, fs in os.walk(os.path.join(RAIZ, "farms")):
        pasta = os.path.basename(d)
        if pasta == "lib":
            continue
        for f in fs:
            if not f.endswith(".py"):
                continue
            versao = re.search(r"_(v\d+)\.py$", f)
            if f in texto or f"{pasta}/*" in texto or (versao and f"_{versao.group(1)}.py" in texto):
                continue
            faltando.append(f"{pasta}/{f}")
    assert not faltando, faltando


def test_trilha_aponta_para_scripts_que_existem():
    texto = open(os.path.join(RAIZ, "farms", "TRILHA.md"), encoding="utf-8").read()
    caminhos = re.findall(r"`((?:jornada/codigo|basics|crops|mazes|dinosaur|leaderboards)/[\w/.-]+\.py)`", texto)
    assert len(set(caminhos)) >= 11
    for c in set(caminhos):
        base = "" if c.startswith("jornada") else "farms"
        assert os.path.exists(os.path.join(RAIZ, base, c)), c


def test_comando_documentado_do_validador_sai_com_zero():
    # README manda rodar `python tools/validar_stub.py`; o erro do error_demo.py é proposital.
    assert v.main([]) == 0
    assert v.main([os.path.join(RAIZ, "farms", "basics", "experiments", "error_demo.py")]) == 1


def test_comandos_dos_docs_apontam_para_arquivos_que_existem():
    achados = 0
    ruins = []
    mds = [os.path.join(RAIZ, f) for f in ("README.md", "README.pt-BR.md")]
    for base in ("docs", "interpreter", "farms", "jornada"):
        for d, _, fs in os.walk(os.path.join(RAIZ, base)):
            mds += [os.path.join(d, f) for f in fs if f.endswith(".md")]
    for md in mds:
        texto = open(md, encoding="utf-8").read()
        for bloco in re.findall(r"```(?:bash|sh|shell|powershell|text)\n(.*?)```", texto, re.S):
            for cmd in re.findall(r"^\s*(?:\$ )?(?:python3?|\.\\?|sh|bash)\s+(\S+\.(?:py|ps1|sh))", bloco, re.M):
                achados += 1
                if not os.path.exists(os.path.join(RAIZ, cmd.replace("\\", "/"))):
                    ruins.append(f"{os.path.relpath(md, RAIZ)}: {cmd}")
    assert achados >= 8
    assert not ruins, ruins
