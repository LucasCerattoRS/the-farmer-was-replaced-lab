"""Control flow — cites `language/control-flow.md`.

`if`/`while`/`for`/`break`/`continue`, plus the depth limit language-quirks.md promises but never
quantifies.
"""

import sys

import pytest

from tfwrlang.errors import TfwrRuntimeError
from conftest import run


def test_while_true_exits_only_on_break():
    # control-flow.md: `while True:` runs until a `break`. The loop budget in `run` guards the
    # suite — if `break` regressed, this would hit the budget and fail loudly instead of hanging.
    interp = run(
        "n = 0\n"
        "while True:\n"
        "    n = n + 1\n"
        "    if n == 5:\n"
        "        break\n"
    )
    assert interp.global_env.get("n") == 5.0


def test_continue_skips_the_rest_of_the_body():
    interp = run(
        "total = 0\n"
        "for i in range(5):\n"
        "    if i == 2:\n"
        "        continue\n"
        "    total = total + i\n"
    )
    assert interp.global_env.get("total") == 0 + 1 + 3 + 4


def test_break_out_of_a_for_loop():
    interp = run(
        "seen = 0\n"
        "for i in range(100):\n"
        "    seen = i\n"
        "    if i == 3:\n"
        "        break\n"
    )
    assert interp.global_env.get("seen") == 3.0


def test_loop_budget_is_a_test_guard_not_a_game_rule():
    # The budget is our safety net, not a documented limit — a genuinely unbounded loop trips it.
    with pytest.raises(TfwrRuntimeError, match="loop iteration budget"):
        run("while True:\n    pass\n", max_loop_iterations=50)


def test_call_stack_is_finite_but_the_limit_is_a_parameter():
    # language-quirks.md says the stack is finite; the real limit is UNMEASURED (a Track 2 item),
    # so the model never invents a number — it exposes `max_call_depth` and only enforces a limit
    # when the caller sets one.
    src = "def rec(n):\n    return rec(n + 1)\nrec(0)\n"
    with pytest.raises(TfwrRuntimeError, match="call stack limit"):
        run(src, max_call_depth=100)


def test_no_depth_limit_by_default_means_no_invented_number():
    # With no limit set, the model does not impose one of its own. The only ceiling left is the
    # *host* interpreter's, which is not the model's claim — so we lift CPython's out of the way
    # to show the model itself refuses to invent a number.
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(100_000)
    try:
        interp = run(
            "def rec(n):\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    return rec(n - 1)\n"
            "d = rec(500)\n"
        )
    finally:
        sys.setrecursionlimit(old)
    assert interp.global_env.get("d") == 0.0
