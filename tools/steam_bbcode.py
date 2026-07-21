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
    lines = md.splitlines()
    in_code = False
    in_list = False
    for line in lines:
        fence = re.match(r"^```", line)
        if fence:
            if in_code:
                out.append("[/code]")
            else:
                out.append("[code]")
            in_code = not in_code
            continue
        if in_code:
            out.append(line)
            continue

        # lists
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("[list]")
                in_list = True
            out.append("[*]" + inline(m.group(1)))
            continue
        elif in_list and line.strip() == "":
            out.append("[/list]")
            in_list = False

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = min(len(m.group(1)), 3)
            out.append(f"[h{level}]{inline(m.group(2))}[/h{level}]")
            continue

        out.append(inline(line))

    if in_list:
        out.append("[/list]")
    if in_code:
        out.append("[/code]")
    return "\n".join(out)


def inline(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)               # images: drop (upload manually on Steam)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[url=\2]\1[/url]", text)  # links
    text = re.sub(r"\*\*([^*]+)\*\*", r"[b]\1[/b]", text)           # bold
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"[i]\1[/i]", text)  # italics
    text = re.sub(r"`([^`]+)`", r"[b]\1[/b]", text)                 # inline code -> bold (Steam has no inline code)
    return text


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
