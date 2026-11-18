#!/usr/bin/env python3
"""Convert a tutorial written in Markdown into Steam guide BBCode.

Usage:  python tools/steam_bbcode.py docs/en/tutorials/01-multi-drone.md [out.txt]
If no output path is given, prints to stdout (pipe to clip: ... | clip).
"""
import re
import sys
from pathlib import Path


def convert(md: str) -> str:
    out = []
    in_code = False
    lista = None        # None, "list" ou "olist"
    in_quote = False    # dentro de uma admonição (!!! tip "Título")
    recuo_cerca = 0

    def fecha_lista():
        nonlocal lista
        if lista:
            out.append(f"[/{lista}]")
            lista = None

    def fecha_quote():
        nonlocal in_quote
        if in_quote:
            out.append("[/quote]")
            in_quote = False

    for line in md.splitlines():
        if in_quote and not in_code and line.strip() and not line.startswith((" ", "\t")):
            fecha_lista()
            fecha_quote()
        if in_quote:
            line = line[4:] if line.startswith("    ") else line.lstrip("\t")

        # Cerca de código: só fecha com ``` no mesmo recuo (ou menor) da abertura;
        # ``` recuado dentro do bloco é conteúdo. Bloco recuado pertence ao item da lista.
        m = re.match(r"^(\s*)```", line)
        if m and (not in_code or len(m.group(1)) <= recuo_cerca):
            if not in_code:
                recuo_cerca = len(m.group(1))
                if recuo_cerca == 0:
                    fecha_lista()
            out.append("[/code]" if in_code else "[code]")
            in_code = not in_code
            continue
        if in_code:
            out.append(line)
            continue

        # admonitions (MkDocs): !!! tip "Título"  ->  [quote=Título]
        m = re.match(r'^(?:!!!|\?\?\?\+?)\s+(\w+)(?:\s+"([^"]*)")?\s*$', line)
        if m:
            fecha_lista()
            fecha_quote()
            titulo = m.group(2) if m.group(2) is not None else m.group(1).capitalize()
            out.append(f"[quote={titulo}]" if titulo else "[quote]")
            in_quote = True
            continue

        # listas
        m = re.match(r"^\s*(?:([-*])|\d+[.)])\s+(.*)$", line)
        if m:
            tipo = "list" if m.group(1) else "olist"
            if lista != tipo:
                fecha_lista()
                out.append(f"[{tipo}]")
                lista = tipo
            out.append("[*]" + inline(m.group(2)))
            continue
        if lista and line.strip() == "":
            fecha_lista()

        # títulos
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            fecha_lista()
            level = min(len(m.group(1)), 3)
            out.append(f"[h{level}]{inline(m.group(2))}[/h{level}]")
            continue

        out.append(inline(line))

    if in_code:
        out.append("[/code]")
    fecha_lista()
    fecha_quote()
    return "\n".join(out)


def inline(text: str) -> str:
    # Código inline primeiro, guardado à parte: `a*b*c` não pode virar itálico.
    codigos = []

    def guarda(m):
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    text = re.sub(r"`([^`]+)`", guarda, text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)               # images: drop (upload manually on Steam)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[url=\2]\1[/url]", text)  # links
    text = re.sub(r"\*\*([^*]+)\*\*", r"[b]\1[/b]", text)           # bold
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"[i]\1[/i]", text)  # italics
    # inline code -> bold (Steam has no inline code)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"[b]{codigos[int(m.group(1))]}[/b]", text)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    bb = convert(src.read_text(encoding="utf-8"))
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(bb, encoding="utf-8")
        print(f"Wrote {sys.argv[2]}")
    else:
        print(bb)


if __name__ == "__main__":
    main()
