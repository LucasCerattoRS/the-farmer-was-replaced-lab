"""Scope rules — cites `language/functions-and-scope.md` and `language/control-flow.md`.

The single most surprising fact for anyone coming from a brace language: loops and branches do
*not* introduce a scope, only functions do. The closure-factory pattern the site teaches rests
entirely on functions capturing their defining environment.
"""

import pytest

from tfwrlang.errors import TfwrNameError
from conftest import run


def test_for_loop_does_not_create_a_scope():
    # control-flow.md / functions-and-scope.md: a `for` does not open a scope, so the loop
    # variable outlives the loop and holds its last value.
    interp = run("for i in range(3):\n    pass\n")
    assert interp.global_env.get("i") == 2.0


def test_while_and_if_do_not_create_a_scope():
    # A name first assigned inside `if`/`while` is visible afterwards — no block scope.
    interp = run(
        "if True:\n"
        "    inside_if = 1\n"
        "n = 0\n"
        "while n < 1:\n"
        "    inside_while = 2\n"
        "    n = n + 1\n"
    )
    assert interp.global_env.get("inside_if") == 1.0
    assert interp.global_env.get("inside_while") == 2.0


def test_function_does_create_a_scope():
    # functions-and-scope.md: a name assigned in a function is local and does not leak out.
    with pytest.raises(TfwrNameError):
        run("def f():\n    local = 1\nf()\nx = local\n")


def test_closure_captures_defining_environment():
    # functions-and-scope.md — the closure-factory pattern: the inner function reads `n` from
    # the environment where it was defined, and keeps reading it after `make` returns.
    interp = run(
        "def make(n):\n"
        "    def add(x):\n"
        "        return x + n\n"
        "    return add\n"
        "add5 = make(5)\n"
        "add10 = make(10)\n"
        "a = add5(1)\n"
        "b = add10(1)\n"
    )
    assert interp.global_env.get("a") == 6.0
    assert interp.global_env.get("b") == 11.0  # each closure kept its own `n`


def test_global_writes_reach_the_module_scope():
    # functions-and-scope.md: without `global`, an assignment inside a function is local; with
    # it, the write lands in the module scope.
    interp = run(
        "count = 0\n"
        "def bump():\n"
        "    global count\n"
        "    count = count + 1\n"
        "bump()\n"
        "bump()\n"
    )
    assert interp.global_env.get("count") == 2.0


def test_assignment_without_global_stays_local():
    interp = run(
        "count = 0\n"
        "def bump():\n"
        "    count = 99\n"  # a fresh local, shadowing the module name
        "bump()\n"
    )
    assert interp.global_env.get("count") == 0.0
