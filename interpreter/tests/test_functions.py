"""Functions and calls — cites `language/functions-and-scope.md`.

`def` is an assignment that binds a function value; calls pass positional args, defaults fill the
rest, and `return` hands a value back (or `None` by falling off the end).
"""

import pytest

from tfwrlang.interp import Function
from tfwrlang.errors import TfwrRuntimeError
from conftest import run


def test_def_binds_a_function_value():
    # functions-and-scope.md: `def f():` reads as `f = <function>` — the name holds a value you
    # can pass around, which is what makes higher-order use (and spawn_drone) work.
    interp = run("def f():\n    return 1\n")
    assert isinstance(interp.global_env.get("f"), Function)


def test_return_value_and_implicit_none():
    interp = run(
        "def g():\n"
        "    return 42\n"
        "def h():\n"
        "    pass\n"  # no return -> None
        "a = g()\n"
        "b = h()\n"
    )
    assert interp.global_env.get("a") == 42.0
    assert interp.global_env.get("b") is None


def test_default_arguments_fill_missing_positionals():
    interp = run(
        "def f(a, b=10):\n"
        "    return a + b\n"
        "x = f(1)\n"
        "y = f(1, 2)\n"
    )
    assert interp.global_env.get("x") == 11.0
    assert interp.global_env.get("y") == 3.0


def test_too_few_arguments_is_a_runtime_error():
    with pytest.raises(TfwrRuntimeError, match="takes"):
        run("def f(a, b):\n    return a\nf(1)\n")


def test_too_many_arguments_is_a_runtime_error():
    with pytest.raises(TfwrRuntimeError, match="takes"):
        run("def f(a):\n    return a\nf(1, 2)\n")


def test_recursion_returns_the_expected_value():
    interp = run(
        "def fib(n):\n"
        "    if n < 2:\n"
        "        return n\n"
        "    return fib(n - 1) + fib(n - 2)\n"
        "r = fib(10)\n"
    )
    assert interp.global_env.get("r") == 55.0
