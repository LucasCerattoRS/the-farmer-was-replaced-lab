"""A reference model of the documented TFWR language subset.

**Not** a reimplementation of the game's interpreter — those internals are not public. This is a
model of the *documented behaviour*: the same claims the `language/` pages make in prose, in a
form that can be executed and tested. Where the official sources are silent, it raises
`Unspecified` instead of quietly inheriting CPython's answer.
"""

from .errors import (  # noqa: F401
    NotSupported,
    Registry,
    TfwrError,
    TfwrNameError,
    TfwrRuntimeError,
    TfwrSyntaxError,
    Unspecified,
)
from .lexer import tokenize  # noqa: F401
from .parser import parse  # noqa: F401

__all__ = [
    "parse",
    "tokenize",
    "TfwrError",
    "TfwrSyntaxError",
    "TfwrRuntimeError",
    "TfwrNameError",
    "NotSupported",
    "Unspecified",
    "Registry",
]
