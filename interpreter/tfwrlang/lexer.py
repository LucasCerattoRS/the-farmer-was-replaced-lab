"""Tokenizer for the TFWR language subset.

Produces the token stream the parser consumes, including the synthetic `NEWLINE`, `INDENT` and
`DEDENT` tokens that turn indentation into structure — the way the official `scripting/` docs
describe blocks. Indentation columns expand tabs to the next multiple of 8 (CPython's rule); the
curated corpus indents with tabs throughout.

Brackets `()[]{}` suppress newline/indentation handling, so a list or dict literal may span
several physical lines (the `dinLoop` list in `fastest_reset.py` does exactly this).
"""

import re

from .errors import TfwrSyntaxError

# Multi-character operators must be tried before their single-character prefixes.
_MULTI_OPS = ("**", "//", "==", "!=", "<=", ">=", "+=", "-=", "*=", "/=", "%=")
_SINGLE_OPS = set("+-*/%<>=()[]{},:.")
_OPEN = {"(": ")", "[": "]", "{": "}"}
_CLOSE = {")", "]", "}"}

_NAME_RE = re.compile(r"[^\W\d]\w*", re.UNICODE)
_NUM_RE = re.compile(r"\d+\.\d*|\.\d+|\d+")


class Tok:
    __slots__ = ("type", "value", "line", "col")

    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Tok({self.type!r}, {self.value!r}, line={self.line})"


def _indent_width(prefix):
    """Column width of a leading-whitespace string, tabs expanded to multiples of 8."""
    col = 0
    for ch in prefix:
        if ch == "\t":
            col += 8 - (col % 8)
        else:
            col += 1
    return col


def tokenize(src):
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    lines = src.split("\n")
    tokens = []
    indents = [0]
    depth = 0  # bracket nesting; >0 means we are continuing a logical line

    for li, line in enumerate(lines, start=1):
        if depth == 0:
            # Start of a logical line: handle indentation.
            j = 0
            while j < len(line) and line[j] in " \t":
                j += 1
            rest = line[j:]
            if rest == "" or rest.startswith("#"):
                continue  # blank or comment-only line: no tokens, no indent change
            col = _indent_width(line[:j])
            if col > indents[-1]:
                indents.append(col)
                tokens.append(Tok("INDENT", "", li, j))
            while col < indents[-1]:
                indents.pop()
                tokens.append(Tok("DEDENT", "", li, j))
            if col != indents[-1]:
                raise TfwrSyntaxError("unindent does not match any outer indentation level", li, col)
            k = j
        else:
            k = 0

        produced_here = False
        while k < len(line):
            ch = line[k]
            if ch in " \t":
                k += 1
                continue
            if ch == "#":
                break  # comment runs to end of line

            # strings
            if ch in ("'", '"'):
                value, k = _scan_string(line, k, li)
                tokens.append(Tok("STRING", value, li, k))
                produced_here = True
                continue

            # numbers
            m = _NUM_RE.match(line, k)
            if m and (ch.isdigit() or (ch == "." and m.group().find(".") == 0 and len(m.group()) > 1)):
                tokens.append(Tok("NUMBER", m.group(), li, k))
                k = m.end()
                produced_here = True
                continue

            # names / keywords
            m = _NAME_RE.match(line, k)
            if m:
                tokens.append(Tok("NAME", m.group(), li, k))
                k = m.end()
                produced_here = True
                continue

            # multi-char operators
            two = line[k:k + 2]
            if two in _MULTI_OPS:
                tokens.append(Tok("OP", two, li, k))
                k += 2
                produced_here = True
                continue

            # single-char operators / punctuation
            if ch in _SINGLE_OPS:
                if ch in _OPEN:
                    depth += 1
                elif ch in _CLOSE:
                    depth = max(0, depth - 1)
                tokens.append(Tok("OP", ch, li, k))
                k += 1
                produced_here = True
                continue

            raise TfwrSyntaxError(f"unexpected character {ch!r}", li, k)

        # End of physical line. Emit NEWLINE only when the logical line is complete
        # (i.e. no open brackets) and it actually produced tokens.
        if depth == 0 and produced_here:
            tokens.append(Tok("NEWLINE", "", li, len(line)))

    # End of file: close any open block, then mark the end.
    last_line = len(lines)
    if tokens and tokens[-1].type not in ("NEWLINE", "DEDENT"):
        tokens.append(Tok("NEWLINE", "", last_line, 0))
    while len(indents) > 1:
        indents.pop()
        tokens.append(Tok("DEDENT", "", last_line, 0))
    tokens.append(Tok("ENDMARKER", "", last_line, 0))
    return tokens


_ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", "'": "'", '"': '"', "0": "\0"}


def _scan_string(line, k, li):
    quote = line[k]
    k += 1
    out = []
    while k < len(line):
        ch = line[k]
        if ch == "\\" and k + 1 < len(line):
            nxt = line[k + 1]
            out.append(_ESCAPES.get(nxt, "\\" + nxt))
            k += 2
            continue
        if ch == quote:
            return "".join(out), k + 1
        out.append(ch)
        k += 1
    raise TfwrSyntaxError("unterminated string literal", li, k)
