"""Conversor Markdown -> BBCode da Steam (tools/steam_bbcode.py)."""
import glob
import os

from steam_bbcode import convert, inline

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_inline_basico():
    assert inline("**a** e *b* e `c`") == "[b]a[/b] e [i]b[/i] e [b]c[/b]"
    assert inline("[site](https://x.y)") == "[url=https://x.y]site[/url]"
    assert inline("antes ![img](a.png) depois") == "antes  depois"


def test_codigo_inline_nao_vira_italico_nem_link():
    assert inline("`a*b*c`") == "[b]a*b*c[/b]"
    assert inline("`x ** 2` e `[i](j)`") == "[b]x ** 2[/b] e [b][i](j)[/b]"


def test_titulos_e_bloco_de_codigo():
    md = "# T\n#### Sub\n```python\nx = *a*\n```"
    assert convert(md) == "[h1]T[/h1]\n[h3]Sub[/h3]\n[code]\nx = *a*\n[/code]"


def test_lista_com_marcador_e_numerada():
    md = "- a\n- b\n\n1. um\n2. dois\n"
    assert convert(md) == "[list]\n[*]a\n[*]b\n[/list]\n\n[olist]\n[*]um\n[*]dois\n[/olist]"


def test_lista_fecha_antes_de_titulo_colado():
    assert convert("- a\n## T") == "[list]\n[*]a\n[/list]\n[h2]T[/h2]"


def test_troca_de_tipo_de_lista_fecha_a_anterior():
    assert convert("- a\n1. b") == "[list]\n[*]a\n[/list]\n[olist]\n[*]b\n[/olist]"


def test_admonicao_vira_quote_sem_recuo():
    md = '!!! tip "A lição"\n    linha *um*\n    linha dois\n\nfora'
    assert convert(md) == "[quote=A lição]\nlinha [i]um[/i]\nlinha dois\n\n[/quote]\nfora"


def test_admonicao_sem_titulo_usa_o_tipo_e_fecha_no_fim():
    assert convert("!!! warning\n    cuidado") == "[quote=Warning]\ncuidado\n[/quote]"
    assert convert('!!! note ""\n    x') == "[quote]\nx\n[/quote]"


def test_codigo_dentro_de_admonicao():
    md = '!!! tip "T"\n    ```\n    x = 1\n      y\n    ```\nfim'
    assert convert(md) == "[quote=T]\n[code]\nx = 1\n  y\n[/code]\n[/quote]\nfim"


def test_tutoriais_reais_nao_deixam_sintaxe_crua():
    """Os tutoriais prometem converter limpo: sem !!!, sem listas numeradas cruas, tags equilibradas."""
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "docs", "*", "tutorials", "0*.md")))
    assert arquivos
    for caminho in arquivos:
        with open(caminho, encoding="utf-8") as f:
            bb = convert(f.read())
        for linha in bb.splitlines():
            assert not linha.startswith(("!!!", "???")), (caminho, linha)
        for tag in ("code", "list", "olist", "quote", "b", "i"):
            abre = bb.count(f"[{tag}]") + (bb.count(f"[{tag}=") if tag == "quote" else 0)
            assert abre == bb.count(f"[/{tag}]"), (caminho, tag)


def test_cerca_recuada_dentro_do_bloco_e_conteudo():
    md = "```python\n    ```\nprint(1)\n```"
    assert convert(md) == "[code]\n    ```\nprint(1)\n[/code]"


def test_bloco_de_codigo_recuado_fica_no_item_da_lista():
    md = "- a\n  ```py\n  x\n  ```\n- b"
    assert convert(md) == "[list]\n[*]a\n[code]\n  x\n[/code]\n[*]b\n[/list]"
