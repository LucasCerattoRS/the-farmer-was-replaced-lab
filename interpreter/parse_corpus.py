"""Milestone 5a: parse every curated script in the repo, with zero errors.

The corpus is real end-game code, so "does the grammar match the language?" becomes an objective
question. Every parse failure is triaged — either the `language/` pages have a gap (fix the page)
or the script reaches past the documented subset (a finding).

Run from the repo root:  python interpreter/parse_corpus.py
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from tfwrlang import parse  # noqa: E402
from tfwrlang.errors import NotSupported, TfwrSyntaxError  # noqa: E402


def corpus_files():
    farms = os.path.join(REPO, "farms")
    for dirpath, _, files in os.walk(farms):
        if os.path.join("farms", "lib") in dirpath:
            continue  # lib/ is the game's own stub, not TFWR source we author
        for fn in sorted(files):
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def main():
    ok, syntax_fail, subset_fail = [], [], []
    for path in corpus_files():
        rel = os.path.relpath(path, REPO)
        with io.open(path, encoding="utf-8") as f:
            src = f.read()
        try:
            parse(src, rel)
            ok.append(rel)
        except NotSupported as e:
            subset_fail.append((rel, str(e)))
        except TfwrSyntaxError as e:
            syntax_fail.append((rel, str(e)))

    total = len(ok) + len(syntax_fail) + len(subset_fail)
    print(f"parsed {len(ok)}/{total} scripts cleanly")
    if subset_fail:
        print(f"\n{len(subset_fail)} outside the documented subset (findings):")
        for rel, msg in subset_fail:
            print(f"  - {rel}: {msg}")
    if syntax_fail:
        print(f"\n{len(syntax_fail)} FAILED to parse (triage: grammar gap or doc gap):")
        for rel, msg in syntax_fail:
            print(f"  - {rel}: {msg}")
        return 1
    print("\nMilestone 5a: OK — whole corpus parses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
