"""Generate `interpreter/UNSPECIFIED.md` from `UNSPECIFIED_CATALOG`.

The catalogue in `tfwrlang/errors.py` is the single source of truth for every place the model
refuses to guess. This script renders it to Markdown so the list of open questions is readable
outside the code — each entry is a Track 2 experiment waiting to be run.

Run from the repo root:  python interpreter/gen_unspecified.py
The generated file is committed; CI can re-run this and fail if it drifts (see check below).
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from tfwrlang.errors import UNSPECIFIED_CATALOG  # noqa: E402

OUT = os.path.join(HERE, "UNSPECIFIED.md")

HEADER = """\
# Unspecified behaviours

**Generated from `tfwrlang/errors.py` — do not edit by hand.** Run
`python interpreter/gen_unspecified.py` to regenerate.

Each entry below is a point where the official TFWR sources define no outcome. The reference
model refuses to guess there: it raises `Unspecified` (or records the choice it was forced to
make) instead of quietly inheriting CPython's answer. That makes every hole loud.

**Each of these is a [Track 2](../ROADMAP.md#track-2--empirical-research-measure-the-game)
experiment waiting to be run.** Measuring one turns a refusal into a documented number and
removes it from this list.

| # | Topic | What the sources leave open |
|---|---|---|
"""


def render():
    rows = []
    for i, topic in enumerate(sorted(UNSPECIFIED_CATALOG), start=1):
        text = " ".join(UNSPECIFIED_CATALOG[topic].split())  # collapse whitespace for one cell
        text = text.replace("|", "\\|")
        rows.append(f"| {i} | `{topic}` | {text} |")
    return HEADER + "\n".join(rows) + "\n"


def main():
    content = render()
    check = "--check" in sys.argv
    if check:
        with io.open(OUT, encoding="utf-8") as f:
            current = f.read()
        if current != content:
            print("UNSPECIFIED.md is out of date — run: python interpreter/gen_unspecified.py")
            return 1
        print("UNSPECIFIED.md is up to date.")
        return 0
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"wrote {OUT} ({len(UNSPECIFIED_CATALOG)} topics)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
