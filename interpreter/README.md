# `interpreter/` — a reference model of the documented TFWR language

**This is not a reimplementation of the game's interpreter.** The game's interpreter is closed —
there is no published source, devlog or postmortem for it. This is a **model of the documented
behaviour**: the same claims the site's *Language* pages make in prose, in a form that can be
executed and tested. Do not describe it as "how the game works internally" anywhere.

Its guiding rule: **where the official sources are silent, the model raises `Unspecified` instead
of quietly inheriting CPython's answer.** Every hole becomes loud, and every loud hole is a
[Measured Numbers](../docs/en/mechanics/measured-numbers.md) experiment waiting to be run.

See the site page for the full write-up:
[`language/reference-interpreter.md`](../docs/en/language/reference-interpreter.md).

## Layout

```
interpreter/
  tfwrlang/
    lexer.py     tokens + INDENT/DEDENT (indentation blocks)
    nodes.py     one AST node type per documented construct
    parser.py    recursive descent; precedence from language/operators.md
    interp.py    tree-walking evaluator (pure core: no game world)
    errors.py    TfwrError family + the UNSPECIFIED_CATALOG and its Registry
    world.py     N×N torus grid, tiles, inventory, tick counter, injectable ModelSet
    builtins.py  the game verbs, each charging its documented tick cost
  tests/         one test per documented behaviour, each citing its page
  parse_corpus.py    parses every curated script in farms/ (front-end milestone)
  gen_unspecified.py generates UNSPECIFIED.md from the catalogue
  UNSPECIFIED.md     generated — the feed of open questions
```

## Running

From the **repo root**, with Python 3.12+ (pure Python, no game required):

```bash
# Parse the whole curated corpus — 45/46 parse cleanly; the holdout is a logged finding
python interpreter/parse_corpus.py

# Run the behaviour tests
pip install pytest
python -m pytest interpreter/tests/

# Regenerate the catalogue of unspecified behaviours (and check it in CI)
python interpreter/gen_unspecified.py
python interpreter/gen_unspecified.py --check
```

`pytest` is the only dev dependency beyond the standard library.
